from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import Chroma
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from flask import Flask, request
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate

app = Flask(__name__)

model = OllamaLLM(model="llama3.2", device="cuda")
embedding = OllamaEmbeddings(model="nomic-embed-text")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=120, length_function=len, is_separator_regex=False
)

folder_path = "db"

raw_prompt = PromptTemplate.from_template("""
    <s>[INST] You are a resume roaster. Come up with most fun (but constructive) roasts for the resume provided below highlighting the weaknesses of the resume so that the user can improve it. [/INST] </s>
    [INST] {input}
        Context: {context}
        Answer:
    [/INST]
                                          """)


chat_history = []


@app.route("/ai", methods=["POST"])
def query():
    print("Post /ai called")
    json_content = request.json
    query = json_content.get("query")
    chat_history.append(HumanMessage(query))
    response = model.invoke(chat_history)
    chat_history.append(AIMessage(response))
    response_answer = {"answer": response}
    return response_answer


@app.route("/pdf", methods=["POST"])
def pdfPost():
    file = request.files["file"]
    filename = file.filename
    savefile = "pdf/" + filename
    file.save(savefile)
    print(f"filename: {filename}")
    loader = PDFPlumberLoader(savefile)
    docs = loader.load_and_split()
    print(f"docs len = {len(docs)}")
    chunks = text_splitter.split_documents(docs)
    print(f"chunks len = {len(chunks)}")
    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )
    vectorstore.persist()
    return {
        "status": "Successfully uploaded",
        "filename": filename,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }


@app.route("/ai_pdf", methods=["POST"])
def query_pdf():
    print("Post /ai_pdf called")
    json_content = request.json
    query = json_content.get("query")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )
    document_chain = create_stuff_documents_chain(model, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)
    result = chain.invoke({"input": query})
    
    return {"result": result["answer"]}


def start_app():
    app.run(debug=True, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    start_app()

# Resume Roaster AI

This project is a Flask-based web application that leverages Langchain's AI capabilities to provide fun and constructive feedback on resumes. It also supports querying information from uploaded PDF documents.

## Features
- Roast resumes with AI-generated feedback.
- Upload and process PDF documents.
- Query information from processed PDF documents using AI.

## Installation

1. **Set up a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**
   ```bash
   python main.py
   ```
   The application will start on `http://127.0.0.1:8080/`.

2. **API Endpoints**
   - `POST /ai`: Send a query to the AI model.
   - `POST /pdf`: Upload a PDF file for processing.
   - `POST /ai_pdf`: Query the processed PDF documents.

## API Endpoints

### `POST /ai`
- **Description**: Sends a textual query to the AI model and receives a response.
- **Request Body**: JSON object with a `query` field.
- **Response**: JSON object containing the AI's response.

### `POST /pdf`
- **Description**: Uploads a PDF file and processes it into chunks for querying.
- **Request**: Multipart form-data with a `file` field.
- **Response**: JSON object with upload status and document details.

### `POST /ai_pdf`
- **Description**: Queries the processed PDF documents using AI.
- **Request Body**: JSON object with a `query` field.
- **Response**: JSON object containing the query result.

## Major Dependencies
- Flask
- Langchain
- Chroma
- PDFPlumber

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any changes.

## License
This project is licensed under the MIT License.

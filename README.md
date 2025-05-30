# PDF Question & Answer Bot

A Django-based REST API that allows users to upload PDF documents and ask questions about their content using Google's Generative AI. The system uses LangChain for document processing and RAG (Retrieval-Augmented Generation) for accurate responses.

## Features

- PDF, DOCX, and TXT file upload support
- Document text extraction and chunking
- Vector-based similarity search using FAISS
- Integration with Google's Generative AI for answering questions
- RESTful API with Swagger documentation

## Prerequisites

- Python 3.10 or higher
- Google Cloud API key for Generative AI
- Windows/Linux/Mac OS

## Installation

1. Clone the repository
```powershell
git clone <repository-url>
cd pdf_Q_nd_A
```

2. Create and activate a virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies
```powershell
pip install -r requirements.txt
```

4. Create a .env file in the project root
```powershell
New-Item .env
```

Add the following to your .env file:
```
GOOGLE_API_KEY=your_api_key_here
DEBUG=True
DJANGO_SECRET_KEY=your_secret_key_here
```

5. Setup the database
```powershell
cd rag
python manage.py migrate
```

6. Create a superuser (optional)
```powershell
python manage.py createsuperuser
```

## Running the Application

1. Start the Django development server
```powershell
python manage.py runserver
```

2. Access the application:
- API Documentation: http://127.0.0.1:8000/swagger/
- Admin Interface: http://127.0.0.1:8000/admin/

## API Endpoints

- `POST /api/upload/`: Upload a document (PDF/DOCX/TXT)
- `POST /api/chat/<document_id>/`: Ask questions about a specific document
- `GET /api/documents/`: List all uploaded documents

## Usage Example

1. Upload a document:
```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@example.pdf"
```

2. Ask a question:
```bash
curl -X POST http://127.0.0.1:8000/api/chat/1/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of this document?"}'
```

## Project Structure

```
pdf_Q_nd_A/
├── rag/                    # Django project directory
│   ├── chat/              # Main application
│   │   ├── models.py      # Database models
│   │   ├── services.py    # Business logic
│   │   ├── views.py       # API views
│   │   └── urls.py        # URL routing
│   └── rag/               # Project settings
├── requirements.txt        # Project dependencies
└── .env                   # Environment variables
```

## Development

- Code Style: PEP 8
- Test Coverage: pytest
- API Documentation: drf-yasg (Swagger/OpenAPI)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

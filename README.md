# Research Assistant AI

An intelligent research assistant that analyzes articles from URLs or PDFs, providing summaries, classifications, sentiment analysis, and critical insights.

## Features

- **Document Ingestion**: Process URLs (web scraping) and PDF files
- **AI-Powered Analysis**:
  - Text summarization using BART transformer
  - Topic classification
  - Sentiment analysis
  - Critical analysis (identifying logical gaps and weaknesses)
- **Smart Recommendations**: Related article suggestions and follow-up questions
- **Clean API**: RESTful API built with FastAPI
- **Simple UI**: Web interface for easy interaction

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download required models (first run will auto-download)
python -c "from src.ml.models import ModelManager; ModelManager()"
```

### Running the Application

```bash
# Start the API server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` for the web UI or `http://localhost:8000/docs` for API documentation.

### Running Tests

```bash
pytest tests/ -v
```

## API Usage

### Analyze URL
```bash
curl -X POST "http://localhost:8000/api/analyze/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

### Analyze PDF
```bash
curl -X POST "http://localhost:8000/api/analyze/pdf" \
  -F "file=@document.pdf"
```

## Project Structure

```
research-assistant/
├── src/
│   ├── ingestion/       # Document processing (URL, PDF)
│   ├── ml/              # ML models and analysis
│   ├── api/             # FastAPI endpoints
│   └── utils/           # Utilities
├── static/              # Frontend assets
├── tests/               # Test suite
├── main.py              # Application entry point
└── requirements.txt     # Dependencies
```

## Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **ML/AI**: HuggingFace Transformers, PyTorch
- **Document Processing**: BeautifulSoup4, PyPDF2, Newspaper3k
- **Frontend**: HTML, CSS, JavaScript

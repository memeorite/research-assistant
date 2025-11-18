# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research Assistant AI is a Python application that analyzes articles from URLs or PDFs using machine learning. It provides AI-powered summaries, topic classification, sentiment analysis, critical analysis (identifying logical gaps and unsupported claims), and generates follow-up questions.

## Technology Stack

- **Backend**: FastAPI (REST API framework)
- **ML/AI**: HuggingFace Transformers with PyTorch
  - Summarization: BART model (facebook/bart-large-cnn)
  - Classification: Zero-shot BART (facebook/bart-large-mnli)
  - Sentiment: DistilBERT (distilbert-base-uncased-finetuned-sst-2-english)
- **Document Processing**: BeautifulSoup4, Newspaper3k, PyPDF2
- **Frontend**: Vanilla JavaScript, HTML, CSS

## Development Commands

### Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start server (development mode with auto-reload)
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=src tests/
```

### Code Quality
```bash
# Format code (if black is installed)
black src/ tests/

# Lint code (if flake8 is installed)
flake8 src/ tests/
```

## Architecture

### Core Modules

1. **src/ingestion/** - Document processing
   - `url_scraper.py`: Fetches and extracts text from URLs using Newspaper3k and BeautifulSoup
   - `pdf_parser.py`: Extracts text from PDF files using PyPDF2

2. **src/ml/** - AI/ML analysis pipeline
   - `models.py`: ML model management and lazy loading (singleton pattern)
   - `analyzer.py`: Core analysis (summarization, classification, sentiment, difficulty assessment)
   - `critic.py`: Critical analysis module that identifies logical gaps, unsupported claims, generates follow-up questions

3. **src/api/** - REST API layer
   - `routes.py`: FastAPI endpoints (`/api/analyze/url`, `/api/analyze/pdf`, `/api/health`)

4. **static/** - Frontend UI
   - Simple, clean web interface with tab-based URL/PDF input

### Data Flow

```
User Input (URL/PDF)
  → Ingestion (url_scraper/pdf_parser)
  → Extract text + metadata
  → ML Analysis (analyzer.py)
    - Summarization
    - Topic classification (14 categories)
    - Sentiment analysis
    - Difficulty assessment
  → Critical Analysis (critic.py)
    - Identify unsupported claims (regex patterns)
    - Detect logical fallacies
    - Generate follow-up questions
    - Suggest related topics
  → Return AnalysisResponse to API
  → Display in UI
```

### Model Loading Strategy

Models use lazy loading (loaded on first use, not at startup) to reduce initialization time. The `ModelManager` class in `src/ml/models.py` manages model caching and GPU/CPU device selection.

## Configuration

Settings are managed via `.env` file and `src/config.py`:
- Server configuration (host, port, debug mode)
- Model selection (can swap models by changing config)
- Processing limits (max text length, file size)

## Key Design Patterns

1. **Separation of Concerns**: Clear boundaries between ingestion, analysis, and API layers
2. **Lazy Loading**: ML models load on-demand to optimize startup
3. **Error Handling**: Comprehensive try/catch with fallbacks (e.g., BeautifulSoup if Newspaper3k fails)
4. **Dependency Injection**: ModelManager singleton pattern for efficient resource usage

## Testing Strategy

- API tests use `TestClient` from FastAPI
- Unit tests for text processing utilities
- Integration tests mock ML models to avoid slow downloads during testing

## Common Tasks

### Adding a New Analysis Feature

1. Add analysis logic to `src/ml/analyzer.py` or `src/ml/critic.py`
2. Update `AnalysisResponse` model in `src/models.py`
3. Update `_analyze_content()` in `src/api/routes.py` to include new field
4. Update frontend display in `static/app.js` and `static/index.html`

### Changing ML Models

1. Update model names in `.env` or `src/config.py`
2. Ensure the new model is compatible with the pipeline type (summarization, zero-shot-classification, or sentiment-analysis)
3. Test thoroughly as different models may have different input/output formats

### Debugging Issues

- Check logs: Application uses Python logging with INFO level by default
- API docs: Visit `/docs` for interactive Swagger UI to test endpoints
- Model loading issues: First run downloads models (can be slow), check internet connection

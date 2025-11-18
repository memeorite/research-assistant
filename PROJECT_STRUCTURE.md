# Project Structure

```
research-assistant/
│
├── main.py                     # Application entry point (FastAPI app)
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── config.py               # Configuration & settings
│   ├── models.py               # Pydantic data models (request/response)
│   │
│   ├── ingestion/              # Document processing
│   │   ├── __init__.py
│   │   ├── url_scraper.py      # Web scraping (BeautifulSoup + Newspaper3k)
│   │   └── pdf_parser.py       # PDF text extraction (PyPDF2)
│   │
│   ├── ml/                     # Machine Learning / AI
│   │   ├── __init__.py
│   │   ├── models.py           # ML model management (lazy loading)
│   │   ├── analyzer.py         # Core analysis (summary, topics, sentiment)
│   │   └── critic.py           # Critical analysis (logical gaps, claims)
│   │
│   ├── api/                    # REST API
│   │   ├── __init__.py
│   │   └── routes.py           # FastAPI endpoints
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── text_processing.py  # Text cleaning & processing
│
├── static/                     # Frontend (Web UI)
│   ├── index.html              # Main HTML page
│   ├── styles.css              # Styling
│   └── app.js                  # JavaScript (API calls, UI updates)
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_api.py             # API endpoint tests
│   └── test_text_processing.py # Utility tests
│
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── .env                        # Environment variables (not in git)
├── .env.example                # Example environment config
├── .gitignore                  # Git ignore rules
│
├── README.md                   # Project overview
├── GETTING_STARTED.md          # Setup & usage guide
├── CLAUDE.md                   # AI assistant context
├── PROJECT_STRUCTURE.md        # This file
│
├── start.bat                   # Quick start (Windows)
└── start.sh                    # Quick start (Linux/Mac)
```

## Module Responsibilities

### Core Application (`main.py`)
- FastAPI app initialization
- CORS middleware
- Static file serving
- Startup/shutdown hooks

### Configuration (`src/config.py`)
- Environment variable management
- Default settings
- Model configuration

### Data Models (`src/models.py`)
- `URLAnalysisRequest`: API request schema
- `AnalysisResponse`: API response schema
- `HealthResponse`: Health check schema

### Ingestion Layer (`src/ingestion/`)
**Purpose:** Extract text from different sources

- `url_scraper.py`:
  - Fetches web pages
  - Extracts article text
  - Falls back between Newspaper3k and BeautifulSoup

- `pdf_parser.py`:
  - Reads PDF files
  - Extracts text from all pages
  - Returns metadata

### ML/AI Layer (`src/ml/`)
**Purpose:** Analyze extracted text with ML models

- `models.py`:
  - Manages HuggingFace transformers
  - Lazy loading (load on first use)
  - GPU/CPU device selection
  - Singleton pattern for efficiency

- `analyzer.py`:
  - Summarization (BART model)
  - Topic classification (zero-shot BART)
  - Sentiment analysis (DistilBERT)
  - Difficulty assessment (heuristic)

- `critic.py`:
  - Identifies unsupported claims (regex patterns)
  - Detects logical fallacies
  - Generates follow-up questions
  - Suggests related topics

### API Layer (`src/api/`)
**Purpose:** Expose functionality via REST API

- `routes.py`:
  - `POST /api/analyze/url`: Analyze article from URL
  - `POST /api/analyze/pdf`: Analyze uploaded PDF
  - `GET /api/health`: Health check
  - Error handling & validation

### Utilities (`src/utils/`)
**Purpose:** Shared helper functions

- `text_processing.py`:
  - Text cleaning
  - Truncation
  - Sentence extraction
  - Word counting

### Frontend (`static/`)
**Purpose:** User interface

- `index.html`: Page structure, forms, results display
- `styles.css`: Modern, clean styling
- `app.js`: Tab switching, API calls, result rendering

### Tests (`tests/`)
**Purpose:** Quality assurance

- `test_api.py`: API endpoint tests
- `test_text_processing.py`: Utility function tests

## Data Flow

```
┌─────────────┐
│   Browser   │
└─────┬───────┘
      │ (1) Submit URL/PDF
      ▼
┌─────────────────┐
│  FastAPI Server │
│   (main.py)     │
└─────┬───────────┘
      │ (2) Route to handler
      ▼
┌─────────────────┐
│  API Routes     │
│  (routes.py)    │
└─────┬───────────┘
      │ (3) Extract text
      ▼
┌─────────────────────┐
│  Ingestion Layer    │
│  url_scraper.py or  │
│  pdf_parser.py      │
└─────┬───────────────┘
      │ (4) Text + metadata
      ▼
┌─────────────────┐
│  ML Analyzer    │
│  (analyzer.py)  │
└─────┬───────────┘
      │ (5) ML results
      ▼
┌─────────────────┐
│ Critical Analyzer│
│  (critic.py)    │
└─────┬───────────┘
      │ (6) Critical insights
      ▼
┌─────────────────┐
│ Build Response  │
│ (AnalysisResp.) │
└─────┬───────────┘
      │ (7) JSON response
      ▼
┌─────────────┐
│   Browser   │
│  Display    │
└─────────────┘
```

## Key Design Decisions

1. **Lazy Model Loading**: Models load on first use to reduce startup time
2. **Separation of Concerns**: Clear boundaries between ingestion, analysis, API
3. **Fallback Strategies**: BeautifulSoup if Newspaper3k fails
4. **Type Safety**: Pydantic models for request/response validation
5. **Modular Architecture**: Easy to swap models or add new features
6. **Clean API**: RESTful design with proper HTTP methods
7. **Simple Frontend**: No framework dependencies, vanilla JS

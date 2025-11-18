# Getting Started with Research Assistant AI

Welcome! This guide will help you set up and run your AI-powered research assistant.

## What This Application Does

Research Assistant AI analyzes articles from URLs or PDFs and provides:

1. **AI-Generated Summary** - Concise summary using BART transformer model
2. **Topic Classification** - Automatically categorizes content into topics
3. **Sentiment Analysis** - Determines positive/negative/neutral sentiment
4. **Critical Analysis** - Identifies logical gaps and unsupported claims
5. **Follow-up Questions** - Suggests thoughtful questions for deeper exploration
6. **Related Topics** - Recommends related areas to research

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- 4GB+ RAM recommended (for ML models)
- Internet connection (first run downloads ML models)

### Step 1: Set Up Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- HuggingFace Transformers (ML models)
- PyTorch (ML backend)
- BeautifulSoup4, Newspaper3k (web scraping)
- PyPDF2 (PDF processing)
- And other utilities

**Note:** First installation may take 5-10 minutes depending on your internet speed.

### Step 3: Configure Environment (Optional)

Copy `.env.example` to `.env` and customize if needed:
```bash
cp .env.example .env
```

Default settings work fine for most users.

## Running the Application

### Option 1: Using Start Scripts

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Using Python Directly

```bash
python main.py
```

### Option 3: Using Uvicorn

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Using the Application

1. **Open your browser** and navigate to:
   - Web UI: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

2. **Analyze a URL:**
   - Click the "URL" tab
   - Enter an article URL (e.g., news article, blog post)
   - Click "Analyze URL"
   - Wait 30-60 seconds for analysis

3. **Analyze a PDF:**
   - Click the "PDF" tab
   - Upload a PDF file (max 10MB)
   - Click "Analyze PDF"
   - Wait 30-60 seconds for analysis

4. **View Results:**
   - Summary and key insights appear below
   - Critical analysis highlights potential issues
   - Follow-up questions help guide further research

## API Usage

You can also use the REST API directly:

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

### Health Check
```bash
curl http://localhost:8000/api/health
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py
```

## Troubleshooting

### Models Not Loading
- **Symptom:** Error about missing models on first run
- **Solution:** Models auto-download on first use. Ensure internet connection and wait for download (can take 5-10 minutes)

### Out of Memory
- **Symptom:** Application crashes or becomes unresponsive
- **Solution:** Close other applications, or reduce `max_text_length` in `.env`

### Slow Analysis
- **Symptom:** Analysis takes >2 minutes
- **Solution:** Normal on CPU. For faster performance, use a GPU-enabled machine

### URL Scraping Fails
- **Symptom:** Error when analyzing certain URLs
- **Solution:** Some websites block scrapers. Try a different article or use PDF upload

### Port Already in Use
- **Symptom:** Error "Address already in use"
- **Solution:** Change `PORT=8000` in `.env` to a different port (e.g., 8001)

## Next Steps

1. **Customize Models:** Edit `.env` to use different HuggingFace models
2. **Add Features:** Extend `src/ml/analyzer.py` or `src/ml/critic.py`
3. **Improve UI:** Modify `static/` files for better UX
4. **Deploy:** Use Docker or cloud platforms (see README.md)

## Support

For issues or questions:
- Check existing documentation in `README.md` and `CLAUDE.md`
- Review API docs at `http://localhost:8000/docs`
- Check error logs in terminal output

Enjoy analyzing articles with AI!

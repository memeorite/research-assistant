"""API routes for the Research Assistant."""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import Dict
import logging

from src.models import URLAnalysisRequest, AnalysisResponse, HealthResponse
from src.ingestion.url_scraper import URLScraper
from src.ingestion.pdf_parser import PDFParser
from src.ml.analyzer import DocumentAnalyzer
from src.ml.critic import CriticalAnalyzer
from src.ml.models import model_manager
from src.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize processors
url_scraper = URLScraper()
pdf_parser = PDFParser()
analyzer = DocumentAnalyzer()
critic = CriticalAnalyzer()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        models_loaded=model_manager.is_ready()
    )


@router.post("/analyze/url", response_model=AnalysisResponse)
async def analyze_url(request: URLAnalysisRequest):
    """
    Analyze content from a URL.

    Args:
        request: URLAnalysisRequest with URL to analyze

    Returns:
        AnalysisResponse with complete analysis

    Raises:
        HTTPException: If URL scraping or analysis fails
    """
    try:
        logger.info(f"Analyzing URL: {request.url}")

        # Scrape URL
        content = url_scraper.scrape(str(request.url))

        # Perform analysis
        return await _analyze_content(content)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to process URL: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error analyzing URL: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/analyze/pdf", response_model=AnalysisResponse)
async def analyze_pdf(file: UploadFile = File(...)):
    """
    Analyze content from a PDF file.

    Args:
        file: Uploaded PDF file

    Returns:
        AnalysisResponse with complete analysis

    Raises:
        HTTPException: If PDF parsing or analysis fails
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are supported"
            )

        logger.info(f"Analyzing PDF: {file.filename}")

        # Read file content
        file_content = await file.read()

        # Check file size
        if len(file_content) > settings.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {settings.max_file_size / 1024 / 1024}MB"
            )

        # Parse PDF
        content = pdf_parser.parse(file_content, file.filename)

        # Perform analysis
        return await _analyze_content(content)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse PDF: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error analyzing PDF: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


async def _analyze_content(content: Dict[str, str]) -> AnalysisResponse:
    """
    Internal helper to analyze document content.

    Args:
        content: Dictionary with 'text', 'title', 'source' keys

    Returns:
        AnalysisResponse with complete analysis
    """
    text = content['text']
    word_count = len(text.split())

    # ML Analysis
    ml_results = analyzer.analyze(text)
    sentiment_label, sentiment_score = ml_results['sentiment']

    # Critical Analysis
    critical_results = critic.analyze(text, ml_results['topics'])

    # Build response
    return AnalysisResponse(
        title=content.get('title', 'Untitled'),
        source=content.get('source', 'Unknown'),
        text_preview=text[:500],
        word_count=word_count,
        summary=ml_results['summary'],
        topics=ml_results['topics'],
        sentiment=sentiment_label,
        sentiment_score=sentiment_score,
        difficulty_level=ml_results['difficulty'],
        critical_analysis=critical_results['critical_summary'],
        logical_gaps=critical_results['logical_gaps'],
        unsupported_claims=critical_results['unsupported_claims'],
        follow_up_questions=critical_results['follow_up_questions'],
        related_topics=critical_results['related_topics']
    )

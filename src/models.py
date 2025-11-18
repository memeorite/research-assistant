"""Data models for API requests and responses."""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class URLAnalysisRequest(BaseModel):
    """Request model for URL analysis."""
    url: HttpUrl
    include_related: bool = True


class AnalysisResponse(BaseModel):
    """Response model for document analysis."""

    # Original Content
    title: Optional[str] = None
    source: str
    text_preview: str = Field(..., description="First 500 characters of text")
    word_count: int

    # AI Analysis
    summary: str
    topics: List[str]
    sentiment: str
    sentiment_score: float = Field(..., ge=0, le=1)
    difficulty_level: str

    # Critical Analysis
    critical_analysis: str
    logical_gaps: List[str]
    unsupported_claims: List[str]

    # Recommendations
    follow_up_questions: List[str]
    related_topics: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Impact of AI on Healthcare",
                "source": "https://example.com/article",
                "text_preview": "Artificial intelligence is transforming...",
                "word_count": 1500,
                "summary": "This article discusses how AI is revolutionizing healthcare...",
                "topics": ["Healthcare", "Technology", "AI"],
                "sentiment": "positive",
                "sentiment_score": 0.85,
                "difficulty_level": "intermediate",
                "critical_analysis": "The article provides strong evidence but lacks...",
                "logical_gaps": ["Missing citation for claim about 50% improvement"],
                "unsupported_claims": ["AI will replace doctors by 2030"],
                "follow_up_questions": ["What are the ethical implications?"],
                "related_topics": ["Machine Learning in Medicine", "Healthcare Data Privacy"]
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    models_loaded: bool

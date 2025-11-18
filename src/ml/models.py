"""ML model management and initialization."""

from transformers import pipeline, Pipeline
from typing import Optional
import logging
import torch

from src.config import settings

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages loading and caching of ML models."""

    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self._summarizer: Optional[Pipeline] = None
        self._classifier: Optional[Pipeline] = None
        self._sentiment: Optional[Pipeline] = None

        logger.info(f"Using device: {'GPU' if self.device == 0 else 'CPU'}")

    @property
    def summarizer(self) -> Pipeline:
        """Lazy load summarization model."""
        if self._summarizer is None:
            logger.info(f"Loading summarization model: {settings.summarization_model}")
            self._summarizer = pipeline(
                "summarization",
                model=settings.summarization_model,
                device=self.device
            )
        return self._summarizer

    @property
    def classifier(self) -> Pipeline:
        """Lazy load zero-shot classification model."""
        if self._classifier is None:
            logger.info(f"Loading classification model: {settings.classification_model}")
            self._classifier = pipeline(
                "zero-shot-classification",
                model=settings.classification_model,
                device=self.device
            )
        return self._classifier

    @property
    def sentiment(self) -> Pipeline:
        """Lazy load sentiment analysis model."""
        if self._sentiment is None:
            logger.info(f"Loading sentiment model: {settings.sentiment_model}")
            self._sentiment = pipeline(
                "sentiment-analysis",
                model=settings.sentiment_model,
                device=self.device
            )
        return self._sentiment

    def is_ready(self) -> bool:
        """Check if models are loaded."""
        return all([
            self._summarizer is not None,
            self._classifier is not None,
            self._sentiment is not None
        ])


# Global model manager instance
model_manager = ModelManager()

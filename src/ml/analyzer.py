"""Core ML analysis functionality."""

from typing import Dict, List, Tuple
import re
import logging

from src.ml.models import model_manager
from src.config import settings

logger = logging.getLogger(__name__)


class DocumentAnalyzer:
    """Analyzes documents using ML models."""

    # Topic categories for classification
    TOPICS = [
        "Technology", "Science", "Healthcare", "Politics", "Economics",
        "Environment", "Education", "Business", "Arts", "Sports",
        "Social Issues", "History", "Philosophy", "Psychology"
    ]

    # Difficulty indicators
    DIFFICULTY_INDICATORS = {
        "beginner": ["simple", "basic", "introduction", "beginner", "overview", "fundamentals"],
        "intermediate": ["analysis", "explores", "examines", "discusses", "considers"],
        "advanced": ["comprehensive", "complex", "sophisticated", "advanced", "technical",
                     "in-depth", "theoretical", "methodology", "paradigm"]
    }

    def __init__(self):
        self.models = model_manager

    def summarize(self, text: str) -> str:
        """
        Generate summary of text.

        Args:
            text: Input text to summarize

        Returns:
            Summary string
        """
        # Truncate if too long
        max_length = settings.max_text_length
        if len(text) > max_length:
            logger.warning(f"Text too long ({len(text)} chars), truncating to {max_length}")
            text = text[:max_length]

        try:
            result = self.models.summarizer(
                text,
                max_length=settings.max_summary_length,
                min_length=settings.min_summary_length,
                do_sample=False
            )
            return result[0]['summary_text']
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            # Fallback to first few sentences
            sentences = text.split('.')[:3]
            return '.'.join(sentences) + '.'

    def classify_topics(self, text: str, top_k: int = 3) -> List[str]:
        """
        Classify text into topics.

        Args:
            text: Input text
            top_k: Number of top topics to return

        Returns:
            List of topic labels
        """
        try:
            # Use first 1000 chars for classification
            text_sample = text[:1000]
            result = self.models.classifier(
                text_sample,
                candidate_labels=self.TOPICS,
                multi_label=True
            )
            return result['labels'][:top_k]
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return ["General"]

    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text.

        Args:
            text: Input text

        Returns:
            Tuple of (sentiment_label, confidence_score)
        """
        try:
            # Use first 512 tokens for sentiment
            text_sample = text[:2000]
            result = self.models.sentiment(text_sample)[0]
            return result['label'].lower(), result['score']
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return "neutral", 0.5

    def assess_difficulty(self, text: str) -> str:
        """
        Assess difficulty level of text.

        Args:
            text: Input text

        Returns:
            Difficulty level: "beginner", "intermediate", or "advanced"
        """
        text_lower = text.lower()

        # Count indicators
        scores = {level: 0 for level in self.DIFFICULTY_INDICATORS}
        for level, indicators in self.DIFFICULTY_INDICATORS.items():
            for indicator in indicators:
                scores[level] += text_lower.count(indicator)

        # Calculate average word length and sentence complexity
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        sentences = text.split('.')
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        # Adjust scores based on text complexity
        if avg_word_length > 6 or avg_sentence_length > 25:
            scores['advanced'] += 3
        elif avg_word_length > 5 or avg_sentence_length > 15:
            scores['intermediate'] += 2
        else:
            scores['beginner'] += 2

        # Return level with highest score
        return max(scores, key=scores.get)

    def analyze(self, text: str) -> Dict:
        """
        Perform complete analysis on text.

        Args:
            text: Input text

        Returns:
            Dictionary with all analysis results
        """
        logger.info(f"Analyzing text ({len(text)} chars)")

        return {
            'summary': self.summarize(text),
            'topics': self.classify_topics(text),
            'sentiment': self.analyze_sentiment(text),
            'difficulty': self.assess_difficulty(text)
        }

"""Text processing utilities."""

import re
from typing import List


def clean_text(text: str) -> str:
    """
    Clean and normalize text.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())

    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:\-\'"()]', '', text)

    return text.strip()


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def extract_sentences(text: str, max_sentences: int = None) -> List[str]:
    """
    Extract sentences from text.

    Args:
        text: Input text
        max_sentences: Maximum number of sentences to return

    Returns:
        List of sentences
    """
    # Simple sentence splitting
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if max_sentences:
        return sentences[:max_sentences]

    return sentences


def count_words(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Input text

    Returns:
        Word count
    """
    return len(text.split())

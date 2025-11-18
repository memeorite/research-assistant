"""Tests for text processing utilities."""

import pytest
from src.utils.text_processing import (
    clean_text,
    truncate_text,
    extract_sentences,
    count_words
)


def test_clean_text():
    """Test text cleaning."""
    text = "Hello   World!  \n  How are   you?"
    cleaned = clean_text(text)
    assert cleaned == "Hello World! How are you?"


def test_truncate_text():
    """Test text truncation."""
    text = "This is a long text that needs truncation"
    truncated = truncate_text(text, 20)
    assert len(truncated) == 20
    assert truncated.endswith("...")


def test_truncate_text_no_truncation():
    """Test text truncation when text is short."""
    text = "Short text"
    truncated = truncate_text(text, 100)
    assert truncated == text


def test_extract_sentences():
    """Test sentence extraction."""
    text = "First sentence. Second sentence! Third sentence?"
    sentences = extract_sentences(text)
    assert len(sentences) == 3
    assert sentences[0] == "First sentence"


def test_extract_sentences_with_limit():
    """Test sentence extraction with limit."""
    text = "First. Second. Third. Fourth."
    sentences = extract_sentences(text, max_sentences=2)
    assert len(sentences) == 2


def test_count_words():
    """Test word counting."""
    text = "This is a test sentence"
    assert count_words(text) == 5

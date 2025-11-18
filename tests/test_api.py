"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "models_loaded" in data


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200


def test_analyze_url_missing_url():
    """Test URL analysis with missing URL."""
    response = client.post("/api/analyze/url", json={})
    assert response.status_code == 422


def test_analyze_url_invalid_url():
    """Test URL analysis with invalid URL."""
    response = client.post(
        "/api/analyze/url",
        json={"url": "not-a-valid-url"}
    )
    assert response.status_code == 422


def test_analyze_pdf_no_file():
    """Test PDF analysis without file."""
    response = client.post("/api/analyze/pdf")
    assert response.status_code == 422


def test_analyze_pdf_wrong_type():
    """Test PDF analysis with wrong file type."""
    response = client.post(
        "/api/analyze/pdf",
        files={"file": ("test.txt", b"not a pdf", "text/plain")}
    )
    assert response.status_code == 400

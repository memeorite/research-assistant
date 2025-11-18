"""Main application entry point."""

import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.api.routes import router
from src.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Research Assistant API",
    description="AI-powered research assistant for analyzing articles from URLs and PDFs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["analysis"])

# Serve static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    logger.warning("Static directory not found, skipping static file serving")


@app.get("/")
async def root():
    """Serve the main UI."""
    try:
        return FileResponse("static/index.html")
    except FileNotFoundError:
        return {
            "message": "Research Assistant API",
            "docs": "/docs",
            "health": "/api/health"
        }


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Starting Research Assistant API")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Using device: GPU" if settings.summarization_model else "CPU")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Research Assistant API")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )

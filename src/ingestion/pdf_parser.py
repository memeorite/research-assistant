"""PDF parsing and text extraction."""

from pypdf import PdfReader
from typing import Dict
import io
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """Extracts text from PDF files."""

    def parse(self, file_content: bytes, filename: str = "document.pdf") -> Dict[str, str]:
        """
        Parse PDF and extract text.

        Args:
            file_content: PDF file content as bytes
            filename: Original filename

        Returns:
            Dictionary containing title, text, and metadata

        Raises:
            ValueError: If PDF parsing fails
        """
        try:
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)

            if len(reader.pages) == 0:
                raise ValueError("PDF has no pages")

            # Extract metadata
            metadata = reader.metadata
            title = metadata.get('/Title', filename) if metadata else filename

            # Extract text from all pages
            text_parts = []
            for page_num, page in enumerate(reader.pages):
                try:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num}: {e}")

            full_text = '\n'.join(text_parts)

            # Clean up text
            full_text = ' '.join(full_text.split())

            if len(full_text) < 100:
                raise ValueError("Insufficient text content extracted from PDF")

            return {
                'title': str(title),
                'text': full_text,
                'authors': metadata.get('/Author', 'Unknown') if metadata else 'Unknown',
                'page_count': len(reader.pages),
                'source': filename
            }

        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

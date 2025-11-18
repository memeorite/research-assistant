"""URL scraping and text extraction."""

import requests
from bs4 import BeautifulSoup
from newspaper import Article
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class URLScraper:
    """Scrapes and extracts text from URLs."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape(self, url: str) -> Dict[str, str]:
        """
        Scrape content from URL.

        Args:
            url: The URL to scrape

        Returns:
            Dictionary containing title, text, and metadata

        Raises:
            ValueError: If URL is invalid or scraping fails
        """
        try:
            # Try newspaper3k first (better for articles)
            article = Article(url)
            article.download()
            article.parse()

            if article.text and len(article.text) > 100:
                return {
                    'title': article.title or 'Untitled',
                    'text': article.text,
                    'authors': ', '.join(article.authors) if article.authors else 'Unknown',
                    'publish_date': str(article.publish_date) if article.publish_date else None,
                    'source': url
                }

        except Exception as e:
            logger.warning(f"Newspaper3k failed for {url}: {e}. Trying BeautifulSoup...")

        # Fallback to BeautifulSoup
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()

            # Get title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else 'Untitled'

            # Try to find main content
            main_content = None
            for tag in ['article', 'main', 'div[class*="content"]', 'div[class*="article"]']:
                main_content = soup.find(tag.split('[')[0])
                if main_content:
                    break

            text_element = main_content if main_content else soup.find('body')
            text = text_element.get_text(separator=' ', strip=True) if text_element else ''

            # Clean up text
            text = ' '.join(text.split())

            if len(text) < 100:
                raise ValueError("Insufficient text content extracted")

            return {
                'title': title_text,
                'text': text,
                'authors': 'Unknown',
                'publish_date': None,
                'source': url
            }

        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse content: {str(e)}")

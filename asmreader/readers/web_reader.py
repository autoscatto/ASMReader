import logging

import requests
from bs4 import BeautifulSoup
from readability import Document
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base import TextReader


class WebReader(TextReader):
    """Reader for web pages that extracts main content using Mozilla's Readability"""

    def __init__(self) -> None:
        # Configure session with retries and timeouts
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )

    def can_handle(self, url: str) -> bool:
        return url.startswith(("http://", "https://"))

    def read(self, url: str) -> str | None:
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            doc = Document(response.text)
            content = doc.summary()

            if not content:
                logging.error(f"No content extracted from {url}")
                return None

            # Parse HTML and extract text
            soup = BeautifulSoup(content, "lxml")

            # Remove unwanted elements
            for element in soup.find_all(["nav", "footer", "script", "style"]):
                element.decompose()

            text = soup.get_text()

            # Clean up whitespace
            return "\n".join(line.strip() for line in text.splitlines() if line.strip())

        except requests.Timeout:
            logging.error(f"Timeout while fetching {url}")
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {str(e)}")
        except Exception as e:
            logging.error(f"Error processing {url}: {str(e)}")

        return None

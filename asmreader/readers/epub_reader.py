import logging

import ebooklib
import magic  # Import python-magic
from bs4 import BeautifulSoup
from ebooklib import epub

from .base import TextReader


class EPUBReader(TextReader):
    """Reader for EPUB files"""

    def can_handle(self, file_path: str) -> bool:
        # Check MIME type using python-magic
        mime_type = magic.from_file(file_path, mime=True)
        return (
            mime_type == "application/epub+zip"
        )  # Verify if the MIME type is 'application/epub+zip'

    def read(self, file_path: str) -> str | None:
        try:
            book = epub.read_epub(file_path)
            text = []

            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), "html.parser")
                    text.append(soup.get_text())

            return "\n".join(text)
        except Exception as e:
            logging.error(f"Error reading EPUB file: {str(e)}")
            return None

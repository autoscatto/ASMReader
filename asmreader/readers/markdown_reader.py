import logging
import re
from pathlib import Path

import magic  # Import python-magic
import markdown

from .base import TextReader


class MarkdownReader(TextReader):
    """Reader for Markdown files"""

    def can_handle(self, file_path: str) -> bool:
        # Check MIME type using python-magic
        mime_type = magic.from_file(file_path, mime=True)
        return mime_type == "text/markdown"  # Verify if the MIME type is 'text/markdown'

    def read(self, file_path: str) -> str | None:
        try:
            with Path(file_path).open(encoding="utf-8") as file:
                md_content = file.read()
                html = markdown.markdown(md_content)
                return "".join(self._strip_html_tags(html))
        except Exception as e:
            logging.error(f"Error reading Markdown file: {str(e)}")
            return None

    def _strip_html_tags(self, html: str) -> str:
        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", html)
        # Clean up excessive whitespace
        return re.sub(r"\s+", " ", text).strip()

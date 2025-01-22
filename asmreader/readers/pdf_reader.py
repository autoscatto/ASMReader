import logging
from pathlib import Path

import magic  # Import python-magic
from pypdf import PdfReader

from .base import TextReader


class PDFReader(TextReader):
    """Reader for PDF files"""

    def can_handle(self, file_path: str) -> bool:
        # Check MIME type using python-magic
        mime_type = magic.from_file(file_path, mime=True)
        return mime_type == "application/pdf"  # Verify if the MIME type is 'application/pdf'

    def read(self, file_path: str) -> str | None:
        try:
            with Path(file_path).open("rb") as file:
                pdf = PdfReader(file)
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logging.error(f"Error reading PDF file: {str(e)}")
            return None

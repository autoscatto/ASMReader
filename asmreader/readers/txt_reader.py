import logging
from pathlib import Path

import magic

from .base import TextReader


class TxtReader(TextReader):
    """Reader for plain text files"""

    def can_handle(self, file_path: str) -> bool:
        mime_type = magic.from_file(file_path, mime=True)
        return mime_type == "text/plain"

    def read(self, file_path: str) -> str | None:
        try:
            with Path(file_path).open(encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            logging.error(f"Error reading text file: {str(e)}")
            return None

    def _is_text_file(self, file_path: str) -> bool:
        with Path(file_path).open("rb") as f:
            header = f.read(4)
        return header.isascii()

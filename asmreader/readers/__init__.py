from .base import TextReader
from .markdown_reader import MarkdownReader
from .pdf_reader import PDFReader
from .txt_reader import TxtReader
from .web_reader import WebReader

__all__ = ["TextReader", "PDFReader", "TxtReader", "WebReader", "MarkdownReader"]

# Registry of all available readers
READERS: list[type[TextReader]] = [
    PDFReader,
    TxtReader,
    WebReader,
    MarkdownReader,
]


def get_reader(file_path: str) -> TextReader | None:
    """Get the appropriate reader for the given file"""
    for reader_class in READERS:
        reader = reader_class()
        if reader.can_handle(file_path):
            return reader
    return None

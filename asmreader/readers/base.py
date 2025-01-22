class TextReader:
    """Base class for text readers."""

    def can_handle(self, file_path: str) -> bool:
        """Check if this reader can handle the given file."""
        return False

    def read(self, file_path: str) -> str | None:
        """Read and return the text content of the file."""
        return None

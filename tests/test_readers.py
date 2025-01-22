import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
import responses  # for mocking HTTP requests

from asmreader.readers import TxtReader, WebReader


# Fixture for temporary text file
@pytest.fixture
def sample_txt_file() -> Generator[Path, None, None]:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Hello, this is a test content.\nSecond line of text.")
    path = Path(f.name)
    yield path
    path.unlink()  # cleanup


def test_txt_reader_can_handle(sample_txt_file: Path) -> None:
    reader = TxtReader()
    assert reader.can_handle(str(sample_txt_file))

    # Create a temporary file with wrong content but .txt extension
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
        f.write(b"\x89PNG\r\n\x1a\n")  # PNG magic numbers
    try:
        assert not reader.can_handle(f.name)
    finally:
        Path(f.name).unlink()


def test_txt_reader_read(sample_txt_file: Path) -> None:
    reader = TxtReader()
    content = reader.read(str(sample_txt_file))
    assert content is not None
    assert "Hello, this is a test content" in content
    assert "Second line of text" in content


def test_web_reader_can_handle() -> None:
    reader = WebReader()
    assert reader.can_handle("https://example.com")
    assert reader.can_handle("http://test.org")
    assert not reader.can_handle("ftp://test.org")
    assert not reader.can_handle("not_a_url")


@responses.activate
def test_web_reader_read() -> None:
    reader = WebReader()
    # Mock a web response
    responses.add(
        responses.GET,
        "https://example.com",
        body="""
        <html>
            <head><title>Test Page</title></head>
            <body>
                <article>
                    <p>Main content here.</p>
                </article>
                <nav>Menu items</nav>
                <footer>Footer content</footer>
            </body>
        </html>
        """,
        status=200,
        content_type="text/html",
    )

    content = reader.read("https://example.com")
    assert content is not None
    assert "Main content here" in content
    assert "Menu items" not in content  # nav should be removed
    assert "Footer content" not in content  # footer should be removed

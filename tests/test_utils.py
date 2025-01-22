import numpy as np

from asmreader.utils import chunk_text, slerp


def test_chunk_text() -> None:
    text = "First sentence. Second sentence! Third sentence? Fourth sentence."
    chunks = chunk_text(text, chunk_size=30)

    assert len(chunks) > 1
    assert all(len(chunk) <= 30 for chunk in chunks)
    assert "First sentence." in chunks[0]

    # Test sentence boundaries
    text = "Short sentence. Very very very very very very long sentence."
    chunks = chunk_text(text, chunk_size=20)
    assert "Short sentence." in chunks[0]
    assert len(chunks) == 2


def test_slerp() -> None:
    v0 = np.array([1.0, 0.0])
    v1 = np.array([0.0, 1.0])

    # Test t=0 returns first vector
    result = slerp(v0, v1, 0.0)
    assert np.allclose(result, v0)

    # Test t=1 returns second vector
    result = slerp(v0, v1, 1.0)
    assert np.allclose(result, v1)

    # Test interpolation
    result = slerp(v0, v1, 0.5)
    assert np.allclose(np.linalg.norm(result), 1.0)  # Result should be normalized

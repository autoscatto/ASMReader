import logging
import re

import numpy as np
from kokoro_onnx import Kokoro
from numpy.typing import NDArray


def slerp(a: NDArray[np.float64], b: NDArray[np.float64], t: float) -> NDArray[np.float64]:
    """
    Perform spherical interpolation (slerp) between two arrays a and b.

    This function interpolates between two normalized arrays a and b using
    spherical linear interpolation. If the angle between a and b is very small,
    it falls back to linear interpolation.

    Args:
        a (np.ndarray): First array (assumed to be normalized).
        b (np.ndarray): Second array (assumed to be normalized).
        t (float): Interpolation parameter in [0, 1].

    Returns:
        np.ndarray: The interpolated array.
    """
    if a.shape != b.shape:
        raise ValueError("Arrays must have the same shape")

    dot = np.sum(a * b, axis=-1, keepdims=True)
    dot = np.clip(dot, -1.0, 1.0)

    theta = np.arccos(dot)
    sin_theta = np.sin(theta)
    epsilon = 1e-6

    # If sin_theta is near zero, fallback to linear interpolation
    if np.any(sin_theta < epsilon):
        return (1 - t) * a + t * b

    sin_t_theta = np.sin(t * theta)
    sin_one_minus_t_theta = np.sin((1 - t) * theta)

    return (sin_one_minus_t_theta / sin_theta) * a + (sin_t_theta / sin_theta) * b  # type: ignore


def prepare_voice(kokoro: Kokoro) -> NDArray[np.float64]:
    """Prepare and blend voices for text-to-speech."""
    nicole = kokoro.get_voice_style("af_nicole")
    # michael: np.ndarray = kokoro.get_voice_style("am_michael")
    adam = kokoro.get_voice_style("am_adam")
    # v1 = slerp(nicole, michael, 0.85)
    v2 = slerp(nicole, adam, 0.85)
    result = slerp(nicole, v2, 0.5)
    logging.info(f"Result of slerp: {result}")
    return result


def chunk_text(text: str, chunk_size: int = 200) -> list[str]:
    """Split text into chunks respecting sentence boundaries."""
    sentence_endings = r"[.!?]+"
    sentences = re.split(f"({sentence_endings}\\s+)", text)

    chunks: list[str] = []
    current_chunk = ""

    for i in range(0, len(sentences), 2):
        sentence = sentences[i] + sentences[i + 1] if i + 1 < len(sentences) else sentences[i]

        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

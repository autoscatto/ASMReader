from unittest.mock import Mock, patch

import numpy as np
import pytest

from asmreader.audio_processor import AudioProcessor


@pytest.fixture
def mock_kokoro() -> Mock:
    kokoro = Mock()
    kokoro.create.return_value = (np.zeros(1000), 44100)  # mock audio data
    return kokoro


def test_audio_processor_initialization(mock_kokoro: Mock) -> None:
    processor = AudioProcessor(kokoro=mock_kokoro, speed=0.7, voice=np.ones(10), output_path=None)
    assert processor.speed == 0.7
    assert processor.is_processing
    assert processor.converter_thread is None


@patch("sounddevice.play")
@patch("sounddevice.wait")
def test_audio_processor_playback(mock_wait: Mock, mock_play: Mock, mock_kokoro: Mock) -> None:
    processor = AudioProcessor(kokoro=mock_kokoro, speed=0.7, voice=np.ones(10))

    chunks = ["Test chunk 1", "Test chunk 2"]
    processor.process_audio_chunks(chunks)

    assert mock_kokoro.create.call_count == 2
    assert mock_play.call_count == 2
    assert mock_wait.call_count == 2

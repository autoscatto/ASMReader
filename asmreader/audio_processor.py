import logging
import threading
from queue import Empty, Queue
from typing import Any

import numpy as np
import sounddevice as sd
from kokoro_onnx import Kokoro
from numpy.typing import NDArray


class AudioProcessor:
    """
    Handles the parallel processing of text chunks into audio.
    Implements a producer-consumer pattern where one thread converts text to speech
    while another handles playback.
    """

    def __init__(
        self,
        kokoro: Kokoro,
        speed: float,
        voice: NDArray[np.float64],
        output_path: str | None = None,
    ) -> None:
        self.kokoro = kokoro
        self.speed = speed
        self.voice = voice
        self.output_path = output_path
        self.audio_queue: Queue[Any] = Queue()  # Buffer for 2 chunks
        self.is_processing: bool = True
        self.converter_thread: threading.Thread | None = None

    def converter_worker(self, chunks: list[str]) -> None:
        """
        Worker thread that converts text chunks to audio.
        Runs in parallel with audio playback.
        """
        for chunk in chunks:
            if not self.is_processing:
                break

            samples, sample_rate = self.kokoro.create(
                chunk, voice=self.voice, speed=self.speed, lang="en-us"
            )
            self.audio_queue.put((samples, sample_rate))

        # Signal end of chunks
        self.audio_queue.put(None)

    def process_audio_chunks(self, chunks: list[str]) -> None:
        """
        Main processing method that starts the converter thread and handles playback.
        Implements the consumer part of the producer-consumer pattern.
        """
        self.converter_thread = threading.Thread(target=self.converter_worker, args=(chunks,))
        self.converter_thread.start()

        while self.is_processing:
            try:
                audio_data = self.audio_queue.get(
                    timeout=0.1
                )  # Use a timeout to avoid blocking indefinitely
                if audio_data is None:
                    break
                samples, sample_rate = audio_data

                if self.output_path:
                    sd.write(self.output_path, samples, sample_rate)
                    logging.info(f"Audio file saved to: {self.output_path}")
                else:
                    sd.play(samples, sample_rate)
                    sd.wait()
            except Empty:
                continue  # If the queue is empty, just continue checking
            except KeyboardInterrupt:
                self.stop()  # Call stop if interrupted
                break

        self.converter_thread.join()

    def stop(self) -> None:
        self.is_processing = False
        if self.converter_thread:
            self.converter_thread.join()

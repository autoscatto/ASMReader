"""Command line interface for ASMReader."""

import importlib.resources
import logging
import sys
from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from pathlib import Path

import numpy as np
from kokoro_onnx import Kokoro
from numpy.typing import NDArray

from .audio_processor import AudioProcessor
from .readers import WebReader, get_reader
from .utils import chunk_text, prepare_voice


def setup_logging(verbose: bool) -> None:
    logging_level = logging.DEBUG if verbose else logging.INFO
    logger = logging.getLogger("asmreader")
    logger.setLevel(logging_level)
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def parse_args(args: Sequence[str] | None = None) -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(description="Generate audio using Kokoro.")
    parser.add_argument("--version", action="version", version="Kokoro Audio Generator v0.1")
    parser.add_argument("--output", type=str, help="Path to save the audio file")
    parser.add_argument("--speed", type=float, default=0.7, help="Audio speed (default: 0.7)")
    parser.add_argument("--file", type=str, help="Input file path (txt, pdf, epub, md)")
    parser.add_argument("--url", type=str, help="URL of web page to read")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args(args)


def process_text(
    text: str,
    kokoro: Kokoro,
    voice: NDArray[np.float64],
    speed: float = 0.7,
    output_path: str | None = None,
) -> None:
    """Process text into speech using the given voice."""
    processor = AudioProcessor(kokoro=kokoro, speed=speed, voice=voice, output_path=output_path)
    processor.process_audio_chunks(list(chunk_text(text)))


def main(args: Sequence[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)
    setup_logging(parsed_args.verbose)
    logger = logging.getLogger("asmreader")

    with importlib.resources.path("asmreader", "") as current_dir:
        current_dir = Path(current_dir)
        onnx_file = current_dir / "kokoro-v0_19.onnx"
        voices_file = current_dir / "voices.bin"

        if not onnx_file.exists() or not voices_file.exists():
            logger.error(
                """Required files do not exist. 
                         Please run 'download_model' to download the necessary files."""
            )
            return 1

        processor = None
        try:
            kokoro = Kokoro(onnx_file, voices_file)
            voice = prepare_voice(kokoro)

            text = None
            if parsed_args.file:
                reader = get_reader(parsed_args.file)
                if reader is None:
                    logger.error("Unsupported file format")
                    return 1
                text = reader.read(parsed_args.file)
            elif parsed_args.url:
                reader = WebReader()
                if not reader.can_handle(parsed_args.url):
                    logger.error("Invalid URL format")
                    return 1
                text = reader.read(parsed_args.url)
            else:
                logger.error("No input source specified. Use --file or --url")
                return 1

            if text is None:
                logger.error("Failed to read input")
                return 1

            processor = AudioProcessor(
                kokoro=kokoro, speed=parsed_args.speed, voice=voice, output_path=parsed_args.output
            )
            processor.process_audio_chunks(list(chunk_text(text)))

            return 0

        except KeyboardInterrupt:
            if processor:
                processor.stop()
            logger.info("Bye!")
            return 0
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            if parsed_args.verbose:
                logger.exception("Detailed error information:")
            return 1


if __name__ == "__main__":
    sys.exit(main())

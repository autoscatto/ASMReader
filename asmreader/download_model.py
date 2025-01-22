import importlib.resources
import logging
from pathlib import Path

import requests
from tqdm import tqdm


def download_file(url: str, destination: Path) -> None:
    if not destination.exists():
        logging.info(f"Downloading {url} to {destination}...")

        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with (
            destination.open("wb") as f,
            tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=str(destination),
            ) as bar,
        ):
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                bar.update(len(data))
    else:
        logging.info(f"{destination} already exists. Skipping download.")


def main() -> None:
    with importlib.resources.path("asmreader", "") as current_dir:
        current_dir = Path(current_dir)

        onnx_file = current_dir / "kokoro-v0_19.onnx"
        voices_file = current_dir / "voices.bin"

        logging.info(f"Files will be downloaded to: {onnx_file} and {voices_file}")
        download_file(
            "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx",
            onnx_file,
        )
        download_file(
            "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.bin",
            voices_file,
        )


if __name__ == "__main__":
    main()

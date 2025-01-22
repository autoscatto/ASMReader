# ASMReader 📧 ✨️

Turn any text into a soothing ASMR-style reading experience. Because sometimes you just want your PDF documentation read in a calming voice.

## Features 🔫

- Converts text from various sources (PDF, TXT, Markdown, Web pages) into speech
- Blends different voices for a unique ASMR experience
- Parallel processing for smooth playback
- Supports chunking for long texts
- Handles web content with readability extraction

## Installation 🚀

You can install ASMReader using `pip`:

```bash
pip install asmreader
```

For users who prefer to use `pipx`, you can install it globally:

```bash
pipx install asmreader
```

If you are using `uv`, you can install it with:

```bash
uv install asmreader
```

After installation, you can run the application using the command:

```bash
asmreader --help
```

## Usage 📣

**Important:** Before using the application, you **MUST** call the `download_model` function to download the necessary files.

```
make run -- --file path/to/your/2501.00536v2.pdf  # Read a local file
make run -- --url "https://en.wikipedia.org/wiki/Gigi_D%27Agostino"  # Read a web page
make run -- --file document.txt --speed 0.8  # Adjust speech speed
make run -- --file document.pdf --output reading.wav  # Save to file instead of playing
```

## Development 🦠

To contribute:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your feature
4. Implement your feature
5. Run tests: `make test`
6. Push and create a Pull Request

### Adding New File Formats 📘

1. Create a new reader in `asmreader/readers/`
2. Inherit from `TextReader`
3. Implement `supported_mime_types()` and `read()`
4. Add to `READERS` in `readers/__init__.py`

Example:
```
class MyNewReader(TextReader):
    def supported_mime_types(self, mime: str) -> bool:
        return mime in ['application/x-my-format']
    
    def read(self, file_path: str) -> str:
        # Your implementation here
        pass
```

## License 📘

MIT - Because sharing is caring, and ASMR should be free.

## Why? 🤊

Because sometimes you need your technical documentation read in a soothing voice while you drift off to sleep, dreaming of well-documented code and properly handled edge cases.

## Known Issues 💣

- Side effects include improved understanding of technical documents
- Not responsible for ASMR addiction

---


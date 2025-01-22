.PHONY: install format lint test clean build publish

install:
	pip install -e ".[dev]"

format:
	black asmreader tests
	ruff check --fix asmreader tests

lint:
	black --check asmreader tests
	ruff check asmreader tests
	mypy asmreader tests

test:
	pytest

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage .mypy_cache/ .ruff_cache/

build: clean
	python -m build

publish: build
	python -m twine upload dist/* 
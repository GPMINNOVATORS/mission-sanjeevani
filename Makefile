.PHONY: install test lint demo
install:
	pip install -e ".[dev]"
test:
	pytest -q
lint:
	ruff check .
demo:
	sanjeevani triage examples/snakebite_report.json
serve:
	sanjeevani serve

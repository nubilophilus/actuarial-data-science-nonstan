PYTHON := .venv/bin/python
PIP := $(PYTHON) -m pip

.PHONY: setup run test clean

setup:
	python3 -m venv .venv
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m src.claims_pipeline

test:
	$(PYTHON) -m pytest -q

clean:
	rm -rf .pytest_cache
	find src -type d -name "__pycache__" -prune -exec rm -rf {} +
	find tests -type d -name "__pycache__" -prune -exec rm -rf {} +


PYTHON ?= python3

.PHONY: setup results test demo

setup:
	$(PYTHON) -m pip install -e ".[dev]"

results:
	$(PYTHON) -m prism.cli results

test:
	$(PYTHON) -m pytest -q

demo:
	streamlit run prism/dashboard.py


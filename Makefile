PYTHON ?= python3

.PHONY: install demo eval lint test api ui

install:
	$(PYTHON) -m pip install -e ".[dev]"

demo:
	$(PYTHON) run_demo.py

eval:
	$(PYTHON) eval/run_experiment.py

lint:
	ruff check .
	black --check .
	mypy kaira

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

api:
	uvicorn kaira.api.server:app --reload

ui:
	$(PYTHON) -m http.server 9000

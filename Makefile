.EXPORT_ALL_VARIABLES:
# Virtual Environment variables
SHELL = /bin/bash
PYTHON_VERSION = 3.13
PY = python3
VENV = .venv
BIN=$(VENV)/bin

export BASH_ENV=$(VENV)/bin/activate

$(VENV): pyproject.toml
	@uv self update || true
	@uv venv --python ${PYTHON_VERSION} --python-fetch automatic --python-preference only-managed --link-mode=copy -q
	@uv sync --all-groups --link-mode=copy

test: $(VENV) ## Run all tests (Legacy + RDF Logic)
	$(BIN)/pytest python/tests/ -v

test-python: $(VENV) ## Alias for python tests
	$(BIN)/pytest python/tests/

test-coverage: $(VENV) ## Run tests with coverage report
	$(BIN)/pytest --cov=python/ --cov-report=term-missing python/tests/

## --- Quality Control ---

lint: $(VENV) ## Linting using ruff (recommended for modern Python)
	uv run ruff check python/

clean: ## Remove venv and cache files
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
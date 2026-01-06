# =============================================================================
# Vedic Astrology Data Generator - Makefile
# =============================================================================
# Common operations for development and usage
# Usage: make <target>
# =============================================================================

.PHONY: help install install-dev install-llm test lint format clean generate analyze

# Default target
help:
	@echo "Vedic Astrology Data Generator"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Installation:"
	@echo "  install        Install package with core dependencies"
	@echo "  install-dev    Install with development dependencies"
	@echo "  install-llm    Install with LLM dependencies"
	@echo "  install-all    Install all dependencies"
	@echo ""
	@echo "Development:"
	@echo "  test           Run tests"
	@echo "  lint           Run linter"
	@echo "  format         Format code"
	@echo "  clean          Clean build artifacts"
	@echo ""
	@echo "Usage:"
	@echo "  generate       Generate Q&A data (templates only)"
	@echo "  generate-pdf   Generate Q&A from PDF (set PDF=path)"
	@echo "  analyze        Analyze existing dataset (set DATA=path)"
	@echo "  filter         Filter existing dataset (set DATA=path)"
	@echo "  augment        Augment existing dataset (set DATA=path)"
	@echo ""
	@echo "Examples:"
	@echo "  make generate"
	@echo "  make generate-pdf PDF=data/raw/jaimini.pdf"
	@echo "  make analyze DATA=data/output/vedic_qa.jsonl"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-llm:
	pip install -e ".[llm]"

install-all:
	pip install -e ".[dev,llm]"

# Development targets
test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ -v --cov=vedic_astro_gen --cov-report=html

lint:
	ruff check src/

format:
	black src/ tests/
	ruff check --fix src/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Usage targets
generate:
	@mkdir -p data/output
	vedic-gen generate --output data/output/vedic_qa.jsonl

generate-pdf:
ifndef PDF
	$(error PDF is not set. Usage: make generate-pdf PDF=path/to/file.pdf)
endif
	@mkdir -p data/output
	vedic-gen generate --pdf $(PDF) --output data/output/vedic_qa.jsonl

generate-llm:
ifndef PDF
	$(error PDF is not set. Usage: make generate-llm PDF=path/to/file.pdf)
endif
ifndef ANTHROPIC_API_KEY
	$(error ANTHROPIC_API_KEY is not set)
endif
	@mkdir -p data/output
	vedic-gen generate --pdf $(PDF) --llm --output data/output/vedic_qa.jsonl

analyze:
ifndef DATA
	$(error DATA is not set. Usage: make analyze DATA=path/to/data.jsonl)
endif
	vedic-gen analyze $(DATA)

filter:
ifndef DATA
	$(error DATA is not set. Usage: make filter DATA=path/to/data.jsonl)
endif
	vedic-gen filter $(DATA) --output data/output/filtered.jsonl

augment:
ifndef DATA
	$(error DATA is not set. Usage: make augment DATA=path/to/data.jsonl)
endif
	vedic-gen augment $(DATA) --output data/output/augmented.jsonl

# Extract from PDF only
extract:
ifndef PDF
	$(error PDF is not set. Usage: make extract PDF=path/to/file.pdf)
endif
	@mkdir -p data/processed
	vedic-gen extract $(PDF) --output data/processed/chunks.json

# List templates
templates:
	vedic-gen templates

# Run all checks
check: lint test
	@echo "All checks passed!"

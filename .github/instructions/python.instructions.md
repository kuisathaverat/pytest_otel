---
applyTo: "*.py"
paths: "*.py"
globs: "*.py"
---

# Python Code Guidelines

## Indentation and Formatting
- Use 4 spaces for indentation
- Maximum line length: 120 characters (ruff enforced)

## Language-Specific Guidelines
- Follow PEP 8 style guidelines
- Use `ruff` for linting and formatting (`--select=E,F,W,I,D,S`)
- Follow pydocstyle conventions for docstrings (exclude test files)
- Use type hints for function parameters and return types
- Use `mypy` for static type checking (`--ignore-missing-imports --no-strict-optional`)
- Use `click` for command-line interfaces
- Use `pytest` for testing
- Use `requests` for HTTP calls
- Use `PyYAML` for YAML parsing
- Use `tenacity` for retry logic

## Security
- Avoid hardcoded secrets or sensitive information (enforced by detect-secrets + semgrep)
- Avoid `shell=True` in subprocess calls; prefer argument lists

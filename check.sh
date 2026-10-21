#!/usr/bin/env bash
# Run the exact checks CI runs — locally, before you push.
# "CI should confirm what you already know, not surprise you."
set -u
echo "==================== ruff check (lint) ======================"
ruff check src/ tests/
echo
echo "==================== ruff format (check only) ==============="
ruff format --check src/ tests/
echo
echo "==================== mypy (type check) ======================"
mypy src/
echo
echo "==================== pytest (+ branch coverage) ============="
pytest tests/ --cov=src --cov-branch --cov-report=term-missing -q
echo
echo "If every section above is clean, your CI pipeline will be green too."

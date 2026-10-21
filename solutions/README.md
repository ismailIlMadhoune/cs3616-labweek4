# Solutions & instructor notes — Week 4 CI/CD lab

Try the lab before reading. `ci.yml` here is the complete pipeline students
build in Part B; copy its `mypy` and `pytest` jobs into
`.github/workflows/ci.yml`.

## Part A — expected output

Clean baseline:

```
ruff check src/ tests/           -> All checks passed!
ruff format --check src/ tests/  -> 3 files already formatted
mypy src/                        -> Success: no issues found in 2 source files
pytest tests/ --cov=src --cov-branch   -> 12 passed, 100% (18 stmts, 12 branch, 0 miss)
```

- **Unused import** (`import os`) → `F401 [*] 'os' imported but unused`; fixed by
  `ruff check src/ --fix`.
- **Wrong return type** (`-> int`) → `error: Incompatible return value type (got
  "float", expected "int") [return-value]`. The test suite does **not** catch this —
  the annotation doesn't change runtime behaviour, which is exactly why static
  type checking earns its place.

## Part B — verification questions

1. **Parallel jobs:** `ruff-check` and `ruff-format` (no `needs:`).
2. **`pytest` status while lint runs:** queued/pending — `needs:` holds it back
   until `mypy` (and transitively the lint jobs) succeed.
3. **Coverage %:** in the `pytest` job log (term-missing report). Optionally
   surface it in the GitHub job summary with a coverage action.

## Part C — expected failure

Adding `import sys` (unused) and pushing:

| Job | Result | Why |
|-----|--------|-----|
| `ruff-check` | ✗ failed | `F401 'sys' imported but unused` |
| `ruff-format` | ✓ passed | the line is valid and correctly formatted |
| `mypy` | ⊘ skipped | `needs: [ruff-check, ...]` failed |
| `pytest` | ⊘ skipped | `needs: [mypy]` never ran |

Skipping downstream jobs is correct: fail-fast avoids spending CI minutes testing
code that already failed a cheaper check.

## Verified

Baseline checks all pass locally (`ruff`, `ruff format --check`, `mypy`, `pytest`
→ 12 passed, 100% branch coverage) with the pinned tool versions in
`requirements.txt`.

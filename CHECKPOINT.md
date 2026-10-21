# CS3616 Week 4 Lab — Checkpoints

## Part A1 — Baseline `bash check.sh`

Environment: macOS (darwin), Python 3.14.3 in `.venv`
Date run: 2026-10-21

| # | Check | Tool / command | Outcome | Evidence |
|---|-------|----------------|---------|----------|
| 1 | Lint | `ruff check src/ tests/` | ✅ PASS | `All checks passed!` |
| 2 | Format | `ruff format --check src/ tests/` | ✅ PASS | `3 files already formatted` |
| 3 | Types | `mypy src/` | ✅ PASS | `Success: no issues found in 2 source files` |
| 4 | Tests | `pytest tests/ --cov=src --cov-branch` | ✅ PASS | `12 passed` |

**Coverage: 100%** (statement *and* branch)

```
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
src/__init__.py       0      0      0      0   100%
src/tax.py           18      0     12      0   100%
-------------------------------------------------------------
TOTAL                18      0     12      0   100%
```

All four gates are green, so the baseline is clean — this is the starting point
for Part B. Any failure from here on is something I introduced, not pre-existing.

---

## Part A2 — Lint violation (unused import), then auto-fix

Added `import os  # unused import` below the module docstring, then `ruff check src/`:

```
F401 [*] `os` imported but unused
  --> src/tax.py:12:8
help: Remove unused import: `os`
Found 1 error.
[*] 1 fixable with `--fix`.
```

The `[*]` marks it safely auto-fixable. `ruff check src/ --fix` →
`Found 1 error (1 fixed, 0 remaining)`, then `ruff check src/` → `All checks passed!`

**Gotcha worth remembering:** `--fix` deleted the import line but left the blank
line behind, so `ruff format --check` then failed with
`unformatted: File would be reformatted --> src/tax.py:12:1`.
Running `ruff format src/` (rewrite mode, no `--check`) cleaned it up.
Lint-fix and format are two separate passes — run `--fix` *then* `format`.

## Part A3 — Type violation no test catches

Changed the return annotation `-> float` to `-> int`. Nothing else.
Same code, three tools, three different answers:

| Tool | Result |
|---|---|
| `pytest tests/ -q` | ❌ **12 passed** — did NOT catch it |
| `ruff check src/` | ❌ `All checks passed!` — did NOT catch it |
| `mypy src/` | ✅ **caught it** |

```
src/tax.py:55: error: Incompatible return value type (got "float", expected "int")  [return-value]
Found 1 error in 1 file (checked 2 source files)
```

**Which did the test suite catch? Neither — that's the point.**

The F401 was invisible to the tests because an unused import changes no
behaviour. The `-> int` lie was invisible because annotations aren't enforced at
runtime: `allowance` starts at `0.0` and accumulates float literals, so it is
always a `float`, and every assertion still held. Only static analysis compared
the *claim* against the *body* — without running the code.

Why this matters for AI-assisted coding: an LLM can emit a function whose
signature and implementation disagree. A green test suite does not prove the
annotation is honest. mypy checks that class of mistake automatically, on
hand-written and generated code alike.

Annotation restored to `-> float`; `src/tax.py` verified byte-identical to the
pristine baseline and all four checks green again.

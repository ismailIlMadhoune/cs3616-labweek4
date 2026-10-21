# CS3616: Week 4 — Code Quality & CI/CD

Open **`instructions/README_Lab_Instructions.html`** in a browser for the full,
step-by-step lab.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows (PowerShell)
python -m pip install -r requirements.txt
bash check.sh                      # confirm the baseline is green
```

## Layout

```
src/tax.py                       # production code (clean, typed, PEP 8) — the GREEN baseline
tests/test_tax.py                # passing suite, 100% branch coverage
ruff.toml                        # ruff lint rules
mypy.ini                         # mypy type-check config
requirements.txt                 # pytest, pytest-cov, ruff, mypy
check.sh                         # run all four checks locally (what CI runs)
.github/workflows/ci.yml         # CI pipeline — STARTER (you complete it in Part B)
solutions/ci.yml                 # reference pipeline
solutions/README.md              # expected output + instructor notes
```

## The three parts (all compulsory)

| Part | Topic | Key commands |
|------|-------|--------------|
| A | Run `ruff` & `mypy` locally; break and fix a lint and a type error | `ruff check`, `ruff format --check`, `mypy src/` |
| B | Author a GitHub Actions pipeline (lint → typecheck → test) | edit `.github/workflows/ci.yml`, `git push` |
| C | Break the pipeline and read the failure; restore green | `git push` + the **Actions** tab |

Unlike the earlier labs, the code and tests are given to you **complete and
green** — this lab is about the quality tooling *around* the code, not the code.

> The tax figures are illustrative teaching examples, not real HMRC rules.

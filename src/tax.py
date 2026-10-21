"""HMRC supplementary-allowance calculator (hypothetical rules, for teaching).

Computes a taxpayer's supplementary allowance in pounds (GBP) based on their
income, age, marital status and disability status.

These figures are ILLUSTRATIVE and do not reflect real HMRC rules — the point
of this lab is to practise code-quality tooling (ruff, mypy) and CI, not tax.
The code below is deliberately clean, PEP 8-compliant and fully type-annotated,
so it gives you a GREEN baseline to start from.
"""

# --- Thresholds (loosely inspired by UK figures) -------------------------
LOW_INCOME_THRESHOLD = 12_570  # UK personal allowance (2024/25)
MID_INCOME_THRESHOLD = 25_000  # upper edge of the partial band
STATE_PENSION_AGE = 66  # UK state pension age


def calculate_allowance(
    income: float,
    age: int,
    has_spouse: bool,
    disabled: bool,
) -> float:
    """Return the total supplementary allowance in GBP.

    Rules (all amounts in GBP):
      * income <= £12,570           -> +£700  (full low-income supplement)
      * £12,570 < income <= £25,000 -> +£300  (partial low-income supplement)
      * age >= 66                   -> +£400  (state-pension-age supplement)
      * has_spouse                  -> +£200  (Marriage Allowance transfer)
      * disabled                    -> +£600  (disability supplement)

    Raises:
      ValueError: if income is negative.
    """
    if income < 0:
        raise ValueError("Income cannot be negative")

    allowance = 0.0

    # Income band — the two bands are mutually exclusive (if / elif).
    if income <= LOW_INCOME_THRESHOLD:
        allowance += 700.0
    elif income <= MID_INCOME_THRESHOLD:
        allowance += 300.0

    # The remaining supplements are INDEPENDENT of each other.
    if age >= STATE_PENSION_AGE:
        allowance += 400.0
    if has_spouse:
        allowance += 200.0
    if disabled:
        allowance += 600.0

    return allowance

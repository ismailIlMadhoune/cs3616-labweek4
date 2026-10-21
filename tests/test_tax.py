"""Unit tests for the HMRC allowance calculator.

This suite already PASSES with 100% statement and branch coverage — this lab is
about code quality and CI, not about writing the tests, so the suite is given to
you complete and green. You'll run it locally and again inside a CI pipeline.

Run just this file:
    pytest tests/test_tax.py -v

With coverage (as CI does):
    pytest tests/ --cov=src --cov-branch --cov-report=term-missing -q
"""

import unittest

from src.tax import calculate_allowance


class TestCalculateAllowance(unittest.TestCase):
    # ---- Single-supplement / happy-path tests -----------------------------

    def test_no_supplements_above_mid_income(self):
        result = calculate_allowance(50_000, 40, False, False)
        self.assertIsNotNone(result)
        self.assertEqual(result, 0.0)
        self.assertIsInstance(result, float)

    def test_full_low_income_supplement(self):
        result = calculate_allowance(10_000, 40, False, False)
        self.assertEqual(result, 700.0)

    def test_mid_income_partial_supplement(self):
        result = calculate_allowance(20_000, 40, False, False)
        self.assertEqual(result, 300.0)

    def test_senior_supplement(self):
        result = calculate_allowance(50_000, 70, False, False)
        self.assertEqual(result, 400.0)

    def test_spouse_offset(self):
        result = calculate_allowance(50_000, 40, True, False)
        self.assertEqual(result, 200.0)

    def test_disability_supplement(self):
        result = calculate_allowance(50_000, 40, False, True)
        self.assertEqual(result, 600.0)

    def test_all_supplements_combined(self):
        result = calculate_allowance(10_000, 70, True, True)
        self.assertAlmostEqual(result, 1_900.0, places=2)

    # ---- Error handling ---------------------------------------------------

    def test_negative_income_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, r"^Income cannot be negative$"):
            calculate_allowance(-500.0, 40, False, False)

    # ---- Boundary tests (give us the final branch coverage) ---------------

    def test_exactly_low_income_threshold_gets_full(self):
        self.assertEqual(calculate_allowance(12_570, 40, False, False), 700.0)

    def test_just_above_low_income_threshold_gets_partial(self):
        self.assertEqual(calculate_allowance(12_571, 40, False, False), 300.0)

    def test_just_above_mid_income_threshold_gets_nothing(self):
        self.assertEqual(calculate_allowance(25_001, 40, False, False), 0.0)

    def test_just_below_state_pension_age_gets_nothing(self):
        self.assertEqual(calculate_allowance(50_000, 65, False, False), 0.0)


if __name__ == "__main__":
    unittest.main()

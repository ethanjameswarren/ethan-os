#!/usr/bin/env python3
"""
Tests for generate_report.py.

Covers: cash-flow reconciliation, debt-payment double counting, biweekly income
conversion, operating vs reserve classification, tracked net worth, missing
projection assumptions, debt goals without baselines, negative bar charts,
dynamic chart height, and metric renaming.
"""

import importlib.util
import sys
from pathlib import Path

# Load the report module
SCRIPT = Path(__file__).resolve().parent / "finance" / "generate_report.py"
spec = importlib.util.spec_from_file_location("generate_report", SCRIPT)
report = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = report
spec.loader.exec_module(report)

PASS = 0
FAIL = 0


def assert_close(actual, expected, msg, tol=0.01):
    global PASS, FAIL
    if actual is None and expected is None:
        PASS += 1
        return
    if actual is None or expected is None:
        FAIL += 1
        print(f"  FAIL: {msg}: expected {expected}, got {actual}")
        return
    if abs(actual - expected) <= tol:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL: {msg}: expected {expected}, got {actual}")


def assert_eq(actual, expected, msg):
    global PASS, FAIL
    if actual == expected:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL: {msg}: expected {expected!r}, got {actual!r}")


def assert_true(value, msg):
    global PASS, FAIL
    if value:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL: {msg}")


def assert_in(needle, haystack, msg):
    global PASS, FAIL
    if needle in haystack:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL: {msg}: {needle!r} not found")


def assert_not_in(needle, haystack, msg):
    global PASS, FAIL
    if needle not in haystack:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL: {msg}: {needle!r} was found but should not be")


# ---------------------------------------------------------------------------
# Fixture: build a FinancialData with controlled data
# ---------------------------------------------------------------------------

def _make_data(**overrides):
    """Create a FinancialData from sample data, optionally overriding fields."""
    # Use a temp dir that won't find any real data
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    data = report.FinancialData(tmp, sample=True)
    for k, v in overrides.items():
        setattr(data, k, v)
    return data


def _make_custom_data(accounts=None, income_sources=None, expenses=None,
                      debts=None, goals=None, snapshots=None, policies=None):
    """Create a FinancialData with fully custom data and recompute."""
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    data = report.FinancialData.__new__(report.FinancialData)
    data.life_dir = tmp
    data.accounts = accounts or []
    data.income_sources = income_sources or []
    data.expenses = expenses or []
    data.debts = debts or []
    data.goals = goals or []
    data.snapshots = snapshots or []
    data.policies = policies or []
    data._compute()
    return data


# ---------------------------------------------------------------------------
# 1. Cash-flow reconciliation & debt-payment double counting
# ---------------------------------------------------------------------------

def test_cash_flow_excludes_debt_payment_expenses():
    """Expenses with category 'Debt Payment' must not be counted in
    monthly_expenses_total (they're already in monthly_debt_payments)."""
    data = _make_custom_data(
        income_sources=[
            {"id": "sal", "net_amount": 5000, "frequency": "monthly", "stability": "high"},
        ],
        expenses=[
            {"id": "rent", "title": "Rent", "category": "Housing", "amount": 1500,
             "frequency": "monthly", "classification": "essential"},
            {"id": "loan-pmt", "title": "Loan Payment", "category": "Debt Payment",
             "amount": 500, "frequency": "monthly", "classification": "committed"},
        ],
        debts=[
            {"id": "loan", "title": "Loan", "debt_type": "personal_loan",
             "current_balance": 10000, "interest_rate_pct": 8, "minimum_payment": 500,
             "status": "active"},
        ],
    )
    # Rent is $1500; the $500 debt-payment expense should be excluded
    assert_close(data.monthly_expenses_total, 1500,
                 "debt-payment expense excluded from expenses total")
    assert_close(data.monthly_debt_payments, 500, "debt minimum counted")
    assert_close(data.avg_budgeted_cash_flow, 5000 - 1500 - 500,
                 "cash flow = income - expenses - debt mins")
    # But it should still appear in the category breakdown
    assert_true("Debt Payment" in data.expense_by_category,
                "Debt Payment category tracked in breakdown")


def test_cash_flow_reconciliation():
    """avg_budgeted_cash_flow = income - non-debt-expenses - debt-minimums."""
    data = _make_custom_data(
        income_sources=[
            {"id": "sal", "net_amount": 6000, "frequency": "monthly"},
        ],
        expenses=[
            {"id": "rent", "title": "Rent", "category": "Housing", "amount": 2000,
             "frequency": "monthly", "classification": "essential"},
            {"id": "food", "title": "Food", "category": "Food", "amount": 600,
             "frequency": "monthly", "classification": "essential"},
        ],
        debts=[
            {"id": "cc", "title": "CC", "debt_type": "credit_card",
             "current_balance": 3000, "interest_rate_pct": 20, "minimum_payment": 100,
             "status": "active"},
        ],
    )
    expected = 6000 - 2600 - 100
    assert_close(data.avg_budgeted_cash_flow, expected, "cash flow reconciliation")
    assert_eq(data.available_monthly_cash_flow, data.avg_budgeted_cash_flow,
              "backward-compatible alias")


# ---------------------------------------------------------------------------
# 2. Biweekly income conversion
# ---------------------------------------------------------------------------

def test_biweekly_income_breakdown():
    """Two-paycheck and three-paycheck month amounts should be correct."""
    net_per_paycheck = 2931.16
    data = _make_custom_data(
        income_sources=[
            {"id": "sal", "net_amount": net_per_paycheck, "frequency": "biweekly",
             "stability": "high"},
        ],
    )
    assert_close(data.two_paycheck_month_income, net_per_paycheck * 2,
                 "2-paycheck month income")
    assert_close(data.three_paycheck_month_income, net_per_paycheck * 3,
                 "3-paycheck month income")
    # Annualized average: net * 26 / 12
    expected_avg = net_per_paycheck * 26 / 12
    assert_close(data.monthly_income_total, expected_avg,
                 "annualized average monthly income", tol=0.02)


def test_biweekly_plus_non_biweekly():
    """Non-biweekly income adds to both 2- and 3-paycheck totals."""
    data = _make_custom_data(
        income_sources=[
            {"id": "sal", "net_amount": 2000, "frequency": "biweekly"},
            {"id": "side", "net_amount": 500, "frequency": "monthly"},
        ],
    )
    assert_close(data.two_paycheck_month_income, 2000 * 2 + 500,
                 "2-paycheck with non-biweekly")
    assert_close(data.three_paycheck_month_income, 2000 * 3 + 500,
                 "3-paycheck with non-biweekly")


# ---------------------------------------------------------------------------
# 3. Operating cash vs emergency reserve
# ---------------------------------------------------------------------------

def test_operating_vs_reserve_cash():
    """Checking accounts are operating cash; savings with goal links are reserves."""
    data = _make_custom_data(
        accounts=[
            {"id": "checking-main", "title": "Checking", "account_type": "checking",
             "balance_snapshots": [{"date": "2026-09-01", "balance": 3000}]},
            {"id": "savings-safety", "title": "Safety Savings", "account_type": "savings",
             "balance_snapshots": [{"date": "2026-09-01", "balance": 8000}]},
        ],
        goals=[
            {"id": "ef", "goal_type": "three_month_safety_reserve",
             "funding_account_id": "savings-safety", "target_amount": 15000,
             "current_amount": 8000, "status": "active"},
        ],
    )
    assert_close(data.operating_cash, 3000, "checking is operating cash")
    assert_close(data.reserve_cash, 8000, "savings with goal link is reserve")
    assert_close(data.liquid_cash, 11000, "total liquid = operating + reserve")


def test_unfunded_savings_is_reserve():
    """Savings accounts default to reserve even without a goal link."""
    data = _make_custom_data(
        accounts=[
            {"id": "sav", "title": "Savings", "account_type": "savings",
             "balance_snapshots": [{"date": "2026-09-01", "balance": 5000}]},
        ],
    )
    assert_close(data.reserve_cash, 5000, "savings defaults to reserve")
    assert_close(data.operating_cash, 0, "no checking = no operating")


# ---------------------------------------------------------------------------
# 4. Tracked net worth (missing asset classes)
# ---------------------------------------------------------------------------

def test_tracked_net_worth_missing_vehicle():
    """Auto loan without vehicle asset → tracked net worth."""
    data = _make_custom_data(
        debts=[
            {"id": "auto", "title": "Auto Loan", "debt_type": "auto_loan",
             "current_balance": 20000, "interest_rate_pct": 5, "minimum_payment": 400,
             "status": "active"},
        ],
    )
    assert_true(data.is_tracked_net_worth, "missing vehicle → tracked")
    assert_in("vehicle market value", data._missing_asset_categories,
              "vehicle in missing list")


def test_full_net_worth_with_vehicle():
    """Auto loan with vehicle asset value → full net worth."""
    data = _make_custom_data(
        accounts=[
            {"id": "car", "title": "2020 Vehicle Asset", "account_type": "other_asset",
             "balance_snapshots": [{"date": "2026-09-01", "balance": 15000}]},
        ],
        debts=[
            {"id": "auto", "title": "Auto Loan", "debt_type": "auto_loan",
             "current_balance": 20000, "interest_rate_pct": 5, "minimum_payment": 400,
             "status": "active"},
        ],
    )
    assert_true(not data.is_tracked_net_worth, "vehicle present → full net worth")


# ---------------------------------------------------------------------------
# 5. Missing projection assumptions
# ---------------------------------------------------------------------------

def test_assumptions_incomplete_no_policies():
    """No policies → assumptions_complete should be False."""
    data = _make_custom_data()
    assert_true(not data.assumptions_complete, "no policies → incomplete")


def test_assumptions_incomplete_zero_values():
    """Policies with zero values → incomplete."""
    data = _make_custom_data(
        policies=[{
            "id": "a", "schema": "finance.projection-assumptions",
            "effective_date": "2026-09-01",
            "annual_income_growth_pct": 0,
            "annual_investment_return_pct": 0,
            "annual_retirement_return_pct": 0,
            "annual_inflation_pct": 0,
            "annual_contribution_growth_pct": 0,
            "employer_match_rules": [],
        }],
    )
    assert_true(not data.assumptions_complete, "zero assumptions → incomplete")


def test_assumptions_complete():
    """Fully populated assumptions → complete."""
    data = _make_custom_data(
        policies=[{
            "id": "a", "schema": "finance.projection-assumptions",
            "effective_date": "2026-09-01",
            "annual_income_growth_pct": 0.03,
            "annual_investment_return_pct": 0.06,
            "annual_retirement_return_pct": 0.07,
            "annual_inflation_pct": 0.025,
            "annual_contribution_growth_pct": 0.02,
            "employer_match_rules": [
                {"threshold_pct": 3.0, "match_rate": 1.0, "note": "100% of first 3%"},
            ],
        }],
    )
    assert_true(data.assumptions_complete, "full assumptions → complete")


# ---------------------------------------------------------------------------
# 6. Debt goals without baselines
# ---------------------------------------------------------------------------

def test_debt_goal_without_baseline():
    """Debt payoff goal with zero target → 'Baseline not established'."""
    data = _make_custom_data(
        debts=[
            {"id": "cc", "title": "CC Debt", "debt_type": "credit_card",
             "current_balance": 5000, "interest_rate_pct": 20, "minimum_payment": 100,
             "status": "active"},
        ],
        goals=[
            {"id": "payoff", "goal_type": "debt_payoff", "title": "Pay off CC",
             "target_amount": 0, "current_amount": 0, "status": "active",
             "related_debt_id": "cc"},
        ],
    )
    html = report._render_goals(data)
    assert_in("Baseline not established", html,
              "debt goal without baseline shows placeholder")


def test_debt_goal_with_baseline():
    """Debt payoff goal with target (baseline) shows progress bar."""
    data = _make_custom_data(
        debts=[
            {"id": "cc", "title": "CC Debt", "debt_type": "credit_card",
             "current_balance": 3000, "interest_rate_pct": 20, "minimum_payment": 100,
             "status": "active"},
        ],
        goals=[
            {"id": "payoff", "goal_type": "debt_payoff", "title": "Pay off CC",
             "target_amount": 5000, "original_balance": 5000,
             "current_amount": 0, "status": "active",
             "related_debt_id": "cc"},
        ],
    )
    html = report._render_goals(data)
    assert_not_in("Baseline not established", html,
                  "debt goal with baseline should not show placeholder")
    # Progress should be 40% (5000-3000=2000 paid / 5000 baseline)
    assert_in("40.0%", html, "40% payoff progress shown")


# ---------------------------------------------------------------------------
# 7. Negative values in bar charts
# ---------------------------------------------------------------------------

def test_negative_bar_chart_no_negative_width():
    """Negative values should not produce negative width attributes."""
    items = [
        ("Positive", 1000, "#00f"),
        ("Negative", -500, "#f00"),
    ]
    svg = report._svg_horizontal_bar(items, width=640)
    assert_not_in('width="-', svg, "no negative width in SVG")
    assert_in('stroke-dasharray', svg, "zero line rendered for negative values")


def test_all_positive_no_zero_line():
    """All-positive charts should not render a zero reference line."""
    items = [
        ("A", 100, "#00f"),
        ("B", 200, "#0f0"),
    ]
    svg = report._svg_horizontal_bar(items, width=640)
    assert_not_in('stroke-dasharray', svg, "no zero line for all-positive")


# ---------------------------------------------------------------------------
# 8. Dynamic chart height
# ---------------------------------------------------------------------------

def test_dynamic_bar_height():
    """Height should scale with the number of items."""
    small = report._svg_horizontal_bar([("A", 100, "#000")], width=640)
    large_items = [(f"Item {i}", 100 + i * 10, "#000") for i in range(10)]
    large = report._svg_horizontal_bar(large_items, width=640)
    # Extract viewBox height
    import re
    h_small = float(re.search(r'viewBox="0 0 640 ([\d.]+)"', small).group(1))
    h_large = float(re.search(r'viewBox="0 0 640 ([\d.]+)"', large).group(1))
    assert_true(h_large > h_small, f"10-item chart taller than 1-item ({h_large} > {h_small})")


# ---------------------------------------------------------------------------
# 9. Metric renaming
# ---------------------------------------------------------------------------

def test_metric_renamed_avg_budgeted():
    """avg_budgeted_cash_flow should exist and equal the alias."""
    data = _make_custom_data(
        income_sources=[{"id": "s", "net_amount": 5000, "frequency": "monthly"}],
        expenses=[{"id": "e", "title": "Rent", "category": "Housing", "amount": 2000,
                   "frequency": "monthly", "classification": "essential"}],
    )
    assert_true(hasattr(data, "avg_budgeted_cash_flow"), "attr exists")
    assert_eq(data.avg_budgeted_cash_flow, data.available_monthly_cash_flow,
              "alias matches")


# ---------------------------------------------------------------------------
# 10. Report rendering smoke test
# ---------------------------------------------------------------------------

def test_sample_report_renders():
    """Sample data report should render without errors."""
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    data = report.FinancialData(tmp, sample=True)
    output = tmp / "test-report.html"
    html = report._render_report(data, output)
    assert_true(len(html) > 1000, "report is substantial HTML")
    assert_in("Executive Dashboard", html, "has executive dashboard section")
    assert_in("Debt Strategy", html, "has debt strategy section")
    assert_in("Detailed Data", html, "has detailed data appendix")
    assert_in("viewport", html, "has viewport meta tag")
    assert_not_in("Available monthly cash flow", html,
                  "old metric name should not appear")


def test_incomplete_assumptions_suppresses_projections():
    """With incomplete assumptions, projections section shows warning."""
    data = _make_custom_data(
        income_sources=[{"id": "s", "net_amount": 5000, "frequency": "monthly"}],
    )
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    output = tmp / "test.html"
    html = report._render_report(data, output)
    assert_in("Assumptions incomplete", html,
              "incomplete assumptions show warning")


# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cash_flow_excludes_debt_payment_expenses()
    test_cash_flow_reconciliation()
    test_biweekly_income_breakdown()
    test_biweekly_plus_non_biweekly()
    test_operating_vs_reserve_cash()
    test_unfunded_savings_is_reserve()
    test_tracked_net_worth_missing_vehicle()
    test_full_net_worth_with_vehicle()
    test_assumptions_incomplete_no_policies()
    test_assumptions_incomplete_zero_values()
    test_assumptions_complete()
    test_debt_goal_without_baseline()
    test_debt_goal_with_baseline()
    test_negative_bar_chart_no_negative_width()
    test_all_positive_no_zero_line()
    test_dynamic_bar_height()
    test_metric_renamed_avg_budgeted()
    test_sample_report_renders()
    test_incomplete_assumptions_suppresses_projections()

    total = PASS + FAIL
    print(f"\nReport generator tests: {PASS}/{total} passed.")
    if FAIL:
        print(f"{FAIL} test(s) FAILED.")
        sys.exit(1)
    else:
        print("All report generator tests passed.")
        sys.exit(0)

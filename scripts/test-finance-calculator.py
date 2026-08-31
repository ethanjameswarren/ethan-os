#!/usr/bin/env python3
"""
Deterministic tests for the finance calculator.

Tests cover: frequency conversion, net worth, debt payoff (single and multi),
promotional rate modeling, 401k calculations, employer match, and allocation
waterfall. All use stdlib only.
"""

import importlib.util
import math
import sys
from pathlib import Path

# Load the calculator module
SCRIPT = Path(__file__).resolve().parent / "finance" / "finance_calculator.py"
spec = importlib.util.spec_from_file_location("finance_calculator", SCRIPT)
calc = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = calc
spec.loader.exec_module(calc)

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
        print(f"  FAIL: {msg}: expected {expected}, got {actual}")


def assert_true(value, msg):
    global PASS, FAIL
    if value:
        PASS += 1
    else:
        FAIL += 1
        print(f"  FAIL: {msg}")


# ---------------------------------------------------------------------------
# Frequency conversion tests
# ---------------------------------------------------------------------------

def test_to_monthly():
    # biweekly $2000 = $2000 * 26/12 = $4333.33
    assert_close(calc.to_monthly(2000, "biweekly"), 4333.33, "biweekly to monthly")
    # weekly $500 = $500 * 52/12 = $2166.67
    assert_close(calc.to_monthly(500, "weekly"), 2166.67, "weekly to monthly")
    # monthly $3000 = $3000
    assert_close(calc.to_monthly(3000, "monthly"), 3000, "monthly to monthly")
    # annual $60000 = $5000/mo
    assert_close(calc.to_monthly(60000, "annual"), 5000, "annual to monthly")
    # semimonthly $2500 = $5000/mo
    assert_close(calc.to_monthly(2500, "semimonthly"), 5000, "semimonthly to monthly")


def test_to_annual():
    assert_close(calc.to_annual(5000, "monthly"), 60000, "monthly to annual")
    assert_close(calc.to_annual(2000, "biweekly"), 52000, "biweekly to annual")


# ---------------------------------------------------------------------------
# Net worth tests
# ---------------------------------------------------------------------------

def test_net_worth():
    assert_close(calc.net_worth(50000, 20000), 30000, "net worth positive")
    assert_close(calc.net_worth(10000, 30000), -20000, "net worth negative")
    assert_close(calc.net_worth(0, 0), 0, "net worth zero")


def test_monthly_surplus():
    assert_close(calc.monthly_surplus(5000, 4000), 1000, "positive surplus")
    assert_close(calc.monthly_surplus(3000, 4000), -1000, "negative surplus")


# ---------------------------------------------------------------------------
# Single debt payoff tests
# ---------------------------------------------------------------------------

def test_months_to_payoff_zero_rate():
    # $1000 balance, 0% rate, $100/mo = 10 months
    assert_close(calc.months_to_payoff(1000, 0, 100), 10, "zero rate payoff")


def test_months_to_payoff_with_interest():
    # $5000 balance, 18% APR, $200/mo
    months = calc.months_to_payoff(5000, 18, 200)
    assert_true(months is not None, "payoff should be possible")
    assert_true(months > 25 and months < 35, f"18% payoff months ~30: got {months:.1f}")


def test_months_to_payoff_insufficient():
    # $10000, 20% APR, $100/mo — interest is $166/mo, can't pay off
    result = calc.months_to_payoff(10000, 20, 100)
    assert_eq(result, None, "insufficient payment returns None")


def test_total_interest():
    # $1000, 0% rate, $100/mo = $0 interest
    assert_close(calc.total_interest(1000, 0, 100), 0, "zero rate interest")

    # $5000, 18% APR, $200/mo
    interest = calc.total_interest(5000, 18, 200)
    assert_true(interest is not None, "interest calculable")
    assert_true(interest > 0, "positive interest for 18% debt")


def test_payoff_zero_balance():
    assert_close(calc.months_to_payoff(0, 18, 200), 0, "zero balance = 0 months")


# ---------------------------------------------------------------------------
# Promotional rate tests
# ---------------------------------------------------------------------------

def test_payoff_with_promo_paid_during():
    # $1000, 0% promo for 12 months, $200/mo — pays off in 5 months
    result = calc.payoff_with_promo(1000, 0, 20, 12, 200)
    assert_true(result["paid_off_during_promo"], "should pay off during promo")
    assert_close(result["months_total"], 5, "5 months to pay off at 0%")
    assert_close(result["total_interest"], 0, "no interest at 0%", tol=0.1)


def test_payoff_with_promo_not_paid_during():
    # $5000, 0% promo for 3 months, 20% regular, $200/mo
    result = calc.payoff_with_promo(5000, 0, 20, 3, 200)
    assert_true(not result["paid_off_during_promo"], "should not pay off during promo")
    assert_close(result["balance_at_promo_end"], 4400, "balance after 3 promo months")
    assert_true(result["months_total"] is not None, "total months calculable")
    assert_true(result["months_total"] > 3, "takes longer than promo period")
    assert_true(result["total_interest"] > 0, "interest accrued after promo")


# ---------------------------------------------------------------------------
# Multi-debt strategy tests
# ---------------------------------------------------------------------------

def test_avalanche_vs_snowball():
    debts = [
        calc.Debt("High Rate Card", 3000, 22, 60),
        calc.Debt("Low Rate Loan", 8000, 6, 150),
        calc.Debt("Medium Card", 2000, 15, 40),
    ]
    total_payment = 60 + 150 + 40 + 200  # minimums + $200 surplus

    avalanche = calc.simulate_payoff(debts, total_payment, "avalanche")
    snowball = calc.simulate_payoff(debts, total_payment, "snowball")

    # Avalanche should have less total interest
    assert_true(
        avalanche.total_interest <= snowball.total_interest,
        f"avalanche interest ({avalanche.total_interest}) <= snowball ({snowball.total_interest})"
    )

    # Snowball should pay off the smallest debt first
    smallest_debt_name = "Medium Card"
    assert_true(
        snowball.debt_payoff_months.get(smallest_debt_name, 999) <=
        snowball.debt_payoff_months.get("High Rate Card", 999),
        "snowball pays smallest first"
    )


def test_custom_order():
    debts = [
        calc.Debt("Debt A", 2000, 10, 50),
        calc.Debt("Debt B", 5000, 20, 100),
    ]
    total_payment = 50 + 100 + 100

    custom = calc.simulate_payoff(debts, total_payment, "custom", custom_order=["Debt A", "Debt B"])
    assert_true(
        custom.debt_payoff_months.get("Debt A", 999) < custom.debt_payoff_months.get("Debt B", 999),
        "custom order: Debt A paid first"
    )


def test_promo_aware_strategy():
    debts = [
        calc.Debt("Regular Card", 3000, 18, 60),
        calc.Debt("Promo Card", 4000, 0, 80,
                  promo_rate_pct=0, promo_months_remaining=6,
                  regular_rate_after_promo_pct=22),
    ]
    total_payment = 60 + 80 + 300

    promo_aware = calc.simulate_payoff(debts, total_payment, "promo_aware")
    avalanche = calc.simulate_payoff(debts, total_payment, "avalanche")

    # Promo-aware should prioritize the promo card early
    assert_true(
        promo_aware.debt_payoff_months.get("Promo Card", 999) <=
        promo_aware.debt_payoff_months.get("Regular Card", 999),
        "promo-aware pays promo card first"
    )


# ---------------------------------------------------------------------------
# 401k tests
# ---------------------------------------------------------------------------

def test_401k_per_paycheck():
    result = calc.compute_401k_per_paycheck(
        annual_target=23500,
        ytd_contributions=10000,
        remaining_paychecks=18,
        gross_pay_per_paycheck=4000,
    )
    assert_close(result["remaining_room"], 13500, "remaining room")
    assert_close(result["per_paycheck_amount"], 750, "per paycheck amount")
    assert_close(result["per_paycheck_pct"], 18.75, "per paycheck pct")


def test_401k_already_maxed():
    result = calc.compute_401k_per_paycheck(
        annual_target=23500,
        ytd_contributions=23500,
        remaining_paychecks=6,
        gross_pay_per_paycheck=4000,
    )
    assert_close(result["remaining_room"], 0, "no remaining room")
    assert_close(result["per_paycheck_amount"], 0, "zero per paycheck")


def test_401k_zero_paychecks():
    result = calc.compute_401k_per_paycheck(
        annual_target=23500,
        ytd_contributions=0,
        remaining_paychecks=0,
        gross_pay_per_paycheck=4000,
    )
    assert_close(result["per_paycheck_amount"], 0, "no paychecks left")


# ---------------------------------------------------------------------------
# Employer match tests
# ---------------------------------------------------------------------------

def test_employer_match():
    # "100% of first 3%, 50% of next 2%" with 6% employee contribution
    result = calc.compute_employer_match(
        employee_contribution_pct=6.0,
        gross_pay_per_paycheck=4000,
        match_tiers=[(3.0, 1.0), (2.0, 0.5)],
        total_paychecks=26,
    )
    # Match: 3% * 100% + 2% * 50% = 3% + 1% = 4%
    assert_close(result["match_pct"], 4.0, "match pct")
    assert_close(result["per_paycheck_match"], 160, "per paycheck match")
    assert_close(result["annual_match"], 4160, "annual match")


def test_employer_match_below_threshold():
    # Employee contributes 2% but match is "100% of first 3%"
    result = calc.compute_employer_match(
        employee_contribution_pct=2.0,
        gross_pay_per_paycheck=4000,
        match_tiers=[(3.0, 1.0), (2.0, 0.5)],
        total_paychecks=26,
    )
    # Match: 2% * 100% = 2%
    assert_close(result["match_pct"], 2.0, "partial match pct")


# ---------------------------------------------------------------------------
# Allocation waterfall tests
# ---------------------------------------------------------------------------

def test_allocation_waterfall():
    tiers = [
        calc.AllocationTier(1, "Emergency Fund", "fixed_amount", 500),
        calc.AllocationTier(2, "401k Match", "fixed_amount", 300),
        calc.AllocationTier(3, "High-Interest Debt", "fixed_amount", 400),
        calc.AllocationTier(4, "Extra Savings", "remainder"),
    ]
    result = calc.allocate_surplus(1500, tiers)

    assert_close(result[0]["allocated"], 500, "tier 1 allocation")
    assert_close(result[1]["allocated"], 300, "tier 2 allocation")
    assert_close(result[2]["allocated"], 400, "tier 3 allocation")
    assert_close(result[3]["allocated"], 300, "remainder allocation")


def test_allocation_insufficient():
    tiers = [
        calc.AllocationTier(1, "Emergency Fund", "fixed_amount", 1000),
        calc.AllocationTier(2, "Savings", "fixed_amount", 500),
    ]
    result = calc.allocate_surplus(800, tiers)

    assert_close(result[0]["allocated"], 800, "tier 1 gets all surplus")
    assert_close(result[1]["allocated"], 0, "tier 2 gets nothing")


def test_allocation_percentage():
    tiers = [
        calc.AllocationTier(1, "Emergency Fund", "percentage", 50),
        calc.AllocationTier(2, "Savings", "remainder"),
    ]
    result = calc.allocate_surplus(2000, tiers)

    assert_close(result[0]["allocated"], 1000, "50% allocation")
    assert_close(result[1]["allocated"], 1000, "remainder allocation")


def test_allocation_negative_surplus():
    tiers = [
        calc.AllocationTier(1, "Savings", "fixed_amount", 500),
    ]
    result = calc.allocate_surplus(-200, tiers)
    assert_close(result[0]["allocated"], 0, "no allocation on negative surplus")


# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_to_monthly()
    test_to_annual()
    test_net_worth()
    test_monthly_surplus()
    test_months_to_payoff_zero_rate()
    test_months_to_payoff_with_interest()
    test_months_to_payoff_insufficient()
    test_total_interest()
    test_payoff_zero_balance()
    test_payoff_with_promo_paid_during()
    test_payoff_with_promo_not_paid_during()
    test_avalanche_vs_snowball()
    test_custom_order()
    test_promo_aware_strategy()
    test_401k_per_paycheck()
    test_401k_already_maxed()
    test_401k_zero_paychecks()
    test_employer_match()
    test_employer_match_below_threshold()
    test_allocation_waterfall()
    test_allocation_insufficient()
    test_allocation_percentage()
    test_allocation_negative_surplus()

    total = PASS + FAIL
    print(f"Finance calculator tests: {PASS}/{total} passed.")
    if FAIL:
        print(f"{FAIL} test(s) FAILED.")
        sys.exit(1)
    else:
        print("All finance calculator tests passed.")
        sys.exit(0)

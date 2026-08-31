#!/usr/bin/env python3
"""
Finance calculator — stdlib-only deterministic financial math.

This module provides the core calculations referenced by
skills/finance/calculation-guidance.md. All functions use only the
Python standard library (math module). No external dependencies.

Every function returns plain Python values suitable for embedding in
YAML frontmatter or presenting to the user. None of these functions
access the filesystem or network.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Frequency helpers
# ---------------------------------------------------------------------------

FREQUENCY_TO_ANNUAL: dict[str, float] = {
    "weekly": 52,
    "biweekly": 26,
    "semimonthly": 24,
    "monthly": 12,
    "quarterly": 4,
    "annual": 1,
    "one_time": 1,
}


def to_monthly(amount: float, frequency: str) -> float:
    """Convert a per-period amount to a monthly equivalent."""
    periods_per_year = FREQUENCY_TO_ANNUAL.get(frequency)
    if periods_per_year is None:
        raise ValueError(f"Unknown frequency: {frequency}")
    return amount * periods_per_year / 12


def to_annual(amount: float, frequency: str) -> float:
    """Convert a per-period amount to an annual equivalent."""
    periods_per_year = FREQUENCY_TO_ANNUAL.get(frequency)
    if periods_per_year is None:
        raise ValueError(f"Unknown frequency: {frequency}")
    return amount * periods_per_year


def paychecks_per_year(frequency: str) -> int:
    """Return the number of paychecks per year for a pay frequency."""
    val = FREQUENCY_TO_ANNUAL.get(frequency)
    if val is None:
        raise ValueError(f"Unknown frequency: {frequency}")
    return int(val)


# ---------------------------------------------------------------------------
# Net worth
# ---------------------------------------------------------------------------

def net_worth(total_assets: float, total_liabilities: float) -> float:
    """Calculate net worth as assets minus liabilities."""
    return total_assets - total_liabilities


def monthly_surplus(monthly_income: float, monthly_expenses: float) -> float:
    """Calculate monthly surplus (income minus expenses)."""
    return monthly_income - monthly_expenses


# ---------------------------------------------------------------------------
# Debt payoff — single debt
# ---------------------------------------------------------------------------

def months_to_payoff(balance: float, annual_rate_pct: float,
                     monthly_payment: float) -> Optional[float]:
    """
    Calculate months to pay off a debt with fixed rate and payment.

    Returns None if the payment is insufficient to cover interest
    (debt will never be paid off at this payment level).
    """
    if balance <= 0:
        return 0.0
    if monthly_payment <= 0:
        return None

    if annual_rate_pct == 0:
        return balance / monthly_payment

    rate_monthly = annual_rate_pct / 100 / 12
    if monthly_payment <= rate_monthly * balance:
        return None  # payment does not cover interest

    months = -math.log(1 - (rate_monthly * balance / monthly_payment)) / math.log(1 + rate_monthly)
    return months


def total_interest(balance: float, annual_rate_pct: float,
                   monthly_payment: float) -> Optional[float]:
    """
    Calculate total interest paid over the life of a debt.

    Returns None if the debt cannot be paid off at this payment level.
    """
    months = months_to_payoff(balance, annual_rate_pct, monthly_payment)
    if months is None:
        return None
    total_paid = monthly_payment * months
    return total_paid - balance


# ---------------------------------------------------------------------------
# Debt payoff — promotional rate modeling
# ---------------------------------------------------------------------------

def payoff_with_promo(
    balance: float,
    promo_rate_pct: float,
    regular_rate_pct: float,
    promo_months_remaining: int,
    monthly_payment: float,
) -> dict:
    """
    Model debt payoff with a promotional rate that expires.

    Returns a dict with:
    - paid_off_during_promo: bool
    - months_total: float or None
    - total_interest: float or None
    - balance_at_promo_end: float
    """
    if balance <= 0:
        return {
            "paid_off_during_promo": True,
            "months_total": 0.0,
            "total_interest": 0.0,
            "balance_at_promo_end": 0.0,
        }

    # Phase 1: promo period
    promo_rate_monthly = promo_rate_pct / 100 / 12
    remaining = balance
    interest_during_promo = 0.0
    months_used = 0

    for _ in range(promo_months_remaining):
        interest = remaining * promo_rate_monthly
        interest_during_promo += interest
        remaining = remaining + interest - monthly_payment
        months_used += 1
        if remaining <= 0:
            return {
                "paid_off_during_promo": True,
                "months_total": float(months_used),
                "total_interest": interest_during_promo + min(0, remaining),
                "balance_at_promo_end": 0.0,
            }

    balance_at_promo_end = remaining

    # Phase 2: regular rate
    post_months = months_to_payoff(balance_at_promo_end, regular_rate_pct, monthly_payment)
    post_interest = total_interest(balance_at_promo_end, regular_rate_pct, monthly_payment)

    if post_months is None:
        return {
            "paid_off_during_promo": False,
            "months_total": None,
            "total_interest": None,
            "balance_at_promo_end": balance_at_promo_end,
        }

    return {
        "paid_off_during_promo": False,
        "months_total": float(months_used) + post_months,
        "total_interest": interest_during_promo + (post_interest or 0),
        "balance_at_promo_end": balance_at_promo_end,
    }


# ---------------------------------------------------------------------------
# Debt payoff — multi-debt strategy simulation
# ---------------------------------------------------------------------------

@dataclass
class Debt:
    """Represents a single debt for payoff simulation."""
    name: str
    balance: float
    annual_rate_pct: float
    minimum_payment: float
    promo_rate_pct: Optional[float] = None
    promo_months_remaining: Optional[int] = None
    regular_rate_after_promo_pct: Optional[float] = None


@dataclass
class PayoffResult:
    """Result of a multi-debt payoff simulation."""
    strategy: str
    debt_payoff_months: dict  # debt name -> months to payoff
    total_interest: float
    total_months: float
    monthly_schedule: list  # list of {month, payments: {name: amount}}


def _effective_rate(debt: Debt, month: int) -> float:
    """Return the effective annual rate for a debt at a given simulation month."""
    if (debt.promo_rate_pct is not None
            and debt.promo_months_remaining is not None
            and month < debt.promo_months_remaining):
        return debt.promo_rate_pct
    if debt.regular_rate_after_promo_pct is not None and debt.promo_months_remaining is not None:
        return debt.regular_rate_after_promo_pct
    return debt.annual_rate_pct


def _sort_debts_avalanche(debts: List[Debt], month: int) -> List[Debt]:
    """Sort debts by effective interest rate, highest first."""
    return sorted(debts, key=lambda d: _effective_rate(d, month), reverse=True)


def _sort_debts_snowball(debts: List[Debt], _month: int) -> List[Debt]:
    """Sort debts by balance, smallest first."""
    return sorted(debts, key=lambda d: d.balance)


def _sort_debts_promo_aware(debts: List[Debt], month: int) -> List[Debt]:
    """Sort debts: promo-expiring first (by months remaining), then avalanche."""
    promo_debts = [d for d in debts
                   if d.promo_months_remaining is not None and month < d.promo_months_remaining]
    non_promo = [d for d in debts if d not in promo_debts]

    promo_debts.sort(key=lambda d: (d.promo_months_remaining or 0) - month)
    non_promo.sort(key=lambda d: _effective_rate(d, month), reverse=True)
    return promo_debts + non_promo


STRATEGY_SORTERS = {
    "avalanche": _sort_debts_avalanche,
    "snowball": _sort_debts_snowball,
    "promo_aware": _sort_debts_promo_aware,
}


def simulate_payoff(
    debts: List[Debt],
    total_monthly_payment: float,
    strategy: str = "avalanche",
    custom_order: Optional[List[str]] = None,
    max_months: int = 600,
) -> PayoffResult:
    """
    Simulate multi-debt payoff under a given strategy.

    For 'custom' strategy, provide custom_order as a list of debt names
    in the desired payoff priority order.
    """
    # Work on copies
    balances = {d.name: d.balance for d in debts}
    debt_map = {d.name: d for d in debts}
    payoff_months: dict[str, float] = {}
    total_interest_paid = 0.0
    schedule: list = []

    for month in range(1, max_months + 1):
        active = [d for d in debts if balances[d.name] > 0]
        if not active:
            break

        # Sort by strategy
        if strategy == "custom" and custom_order:
            active_names = {d.name for d in active}
            ordered_names = [n for n in custom_order if n in active_names]
            remaining = [n for n in active_names if n not in ordered_names]
            active = [debt_map[n] for n in ordered_names + sorted(remaining)]
        elif strategy in STRATEGY_SORTERS:
            active = STRATEGY_SORTERS[strategy](active, month)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        # Apply interest
        month_payments: dict[str, float] = {}
        for d in active:
            rate = _effective_rate(d, month) / 100 / 12
            interest = balances[d.name] * rate
            balances[d.name] += interest
            total_interest_paid += interest

        # Apply minimum payments
        surplus = total_monthly_payment
        for d in active:
            payment = min(d.minimum_payment, balances[d.name])
            balances[d.name] -= payment
            month_payments[d.name] = payment
            surplus -= payment

        # Apply surplus to priority debt
        for d in active:
            if surplus <= 0:
                break
            if balances[d.name] <= 0:
                continue
            extra = min(surplus, balances[d.name])
            balances[d.name] -= extra
            month_payments[d.name] = month_payments.get(d.name, 0) + extra
            surplus -= extra

        # Record payoffs
        for d in active:
            if balances[d.name] <= 0.005 and d.name not in payoff_months:
                payoff_months[d.name] = float(month)
                balances[d.name] = 0

        schedule.append({"month": month, "payments": month_payments})

    total_months_val = max(payoff_months.values()) if payoff_months else 0.0

    return PayoffResult(
        strategy=strategy,
        debt_payoff_months=payoff_months,
        total_interest=round(total_interest_paid, 2),
        total_months=total_months_val,
        monthly_schedule=schedule,
    )


# ---------------------------------------------------------------------------
# 401k per-paycheck calculation
# ---------------------------------------------------------------------------

def compute_401k_per_paycheck(
    annual_target: float,
    ytd_contributions: float,
    remaining_paychecks: int,
    gross_pay_per_paycheck: float,
) -> dict:
    """
    Calculate per-paycheck 401k contribution to reach an annual target.

    Returns a dict with per_paycheck_amount, per_paycheck_pct,
    remaining_room, and annual_target.
    """
    remaining_room = max(0, annual_target - ytd_contributions)

    if remaining_paychecks <= 0:
        return {
            "annual_target": annual_target,
            "ytd_contributions": ytd_contributions,
            "remaining_room": remaining_room,
            "remaining_paychecks": 0,
            "per_paycheck_amount": 0.0,
            "per_paycheck_pct": 0.0,
        }

    per_paycheck_amount = remaining_room / remaining_paychecks
    per_paycheck_pct = (per_paycheck_amount / gross_pay_per_paycheck * 100
                        if gross_pay_per_paycheck > 0 else 0.0)

    return {
        "annual_target": annual_target,
        "ytd_contributions": ytd_contributions,
        "remaining_room": remaining_room,
        "remaining_paychecks": remaining_paychecks,
        "per_paycheck_amount": round(per_paycheck_amount, 2),
        "per_paycheck_pct": round(per_paycheck_pct, 2),
    }


def compute_employer_match(
    employee_contribution_pct: float,
    gross_pay_per_paycheck: float,
    match_tiers: List[Tuple[float, float]],
    total_paychecks: int,
) -> dict:
    """
    Calculate employer 401k match.

    match_tiers is a list of (threshold_pct, match_rate) tuples.
    Example: [(3.0, 1.0), (2.0, 0.5)] means "100% of first 3%, 50% of next 2%".

    Returns per_paycheck_match, annual_match, and effective_match_pct.
    """
    remaining_pct = employee_contribution_pct
    match_pct = 0.0

    for threshold, rate in match_tiers:
        matched = min(remaining_pct, threshold)
        match_pct += matched * rate
        remaining_pct -= matched
        if remaining_pct <= 0:
            break

    per_paycheck_match = match_pct / 100 * gross_pay_per_paycheck
    annual_match = per_paycheck_match * total_paychecks

    return {
        "employee_contribution_pct": employee_contribution_pct,
        "match_pct": round(match_pct, 4),
        "per_paycheck_match": round(per_paycheck_match, 2),
        "annual_match": round(annual_match, 2),
    }


# ---------------------------------------------------------------------------
# Allocation waterfall
# ---------------------------------------------------------------------------

@dataclass
class AllocationTier:
    """A single tier in the allocation waterfall."""
    priority: int
    label: str
    target_type: str  # "fixed_amount", "percentage", "remainder"
    amount: float = 0.0  # dollar amount or percentage


def allocate_surplus(
    monthly_surplus_amount: float,
    tiers: List[AllocationTier],
) -> List[dict]:
    """
    Walk the allocation waterfall and return per-tier allocations.

    Returns a list of dicts: {priority, label, allocated, remaining_after}.
    """
    remaining = monthly_surplus_amount
    results = []

    sorted_tiers = sorted(tiers, key=lambda t: t.priority)
    for tier in sorted_tiers:
        if remaining <= 0:
            allocated = 0.0
        elif tier.target_type == "fixed_amount":
            allocated = min(tier.amount, remaining)
        elif tier.target_type == "percentage":
            allocated = monthly_surplus_amount * tier.amount / 100
            allocated = min(allocated, remaining)
        elif tier.target_type == "remainder":
            allocated = remaining
        else:
            allocated = 0.0

        remaining -= allocated
        results.append({
            "priority": tier.priority,
            "label": tier.label,
            "allocated": round(allocated, 2),
            "remaining_after": round(remaining, 2),
        })

    return results

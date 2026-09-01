#!/usr/bin/env python3
"""
Generate a standalone HTML financial report from Ethan Life finance data.

This script reads finance objects from the ethan-life file tree, performs
calculations with ethan-os/scripts/finance/finance_calculator.py, and writes a
single self-contained HTML report that can be opened locally in a browser.

All projections and recommendations are clearly labeled as assumptions or
recommendations, never facts. The report does not store sensitive account
identifiers.
"""

from __future__ import annotations

import argparse
import html as html_module
import importlib.util
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Load the existing finance calculator
# ---------------------------------------------------------------------------

def _load_calculator():
    try:
        calc_path = Path(__file__).resolve().parent / "finance_calculator.py"
        spec = importlib.util.spec_from_file_location("finance_calculator", calc_path)
        calc = importlib.util.module_from_spec(spec)
        sys.modules["finance_calculator"] = calc
        spec.loader.exec_module(calc)
        return calc
    except Exception as exc:
        print(f"Warning: could not load finance_calculator.py: {exc}", file=sys.stderr)
        return None


CALC = _load_calculator()


FREQUENCY_TO_ANNUAL = {
    "weekly": 52,
    "biweekly": 26,
    "semimonthly": 24,
    "monthly": 12,
    "quarterly": 4,
    "annual": 1,
    "one_time": 1,
    "irregular": 1,
}

# Account types that are liabilities when the balance is outstanding.
LIABILITY_TYPES = {
    "credit_card", "loan", "mortgage", "auto_loan", "student_loan",
    "personal_loan", "medical", "other_debt",
}

LIQUID_TYPES = {"checking", "savings", "cash", "money_market"}

RETIREMENT_TYPES = {"retirement_401k", "retirement_ira", "retirement_roth_ira", "hsa"}

INVESTMENT_TYPES = {"taxable_investment", "investment", "brokerage"}

HIGH_INTEREST_THRESHOLD = 10.0

SAFETY_RESERVE_GOALS = {
    "starter_safety_reserve",
    "three_month_safety_reserve",
    "six_month_safety_reserve",
}


def _fmt_currency(value, currency="USD"):
    if value is None:
        return "—"
    sign = "-$" if value < 0 else "$"
    return f"{sign}{abs(value):,.2f}"


def _fmt_number(value):
    if value is None:
        return "—"
    return f"{value:,.2f}"


def _fmt_percent(value):
    if value is None:
        return "—"
    return f"{value:.2f}%"


def _coerce_date(value):
    if isinstance(value, datetime):
        return value.date().isoformat()
    if value:
        return str(value)[:10]
    return "—"


def _to_monthly(amount, frequency):
    if CALC is not None and hasattr(CALC, "to_monthly"):
        try:
            return CALC.to_monthly(amount, frequency)
        except Exception:
            pass
    periods = FREQUENCY_TO_ANNUAL.get(frequency, 12)
    return amount * periods / 12


def _load_yaml_file(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        content = f.read()

    if path.suffix in (".md", ".markdown"):
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[1]

    return yaml.safe_load(content) or {}


class DesignProfile:
    """
    Load the user's private design profile from the personal data layer.

    Searches, in order:
      1. <life_dir>/global/design-tokens.yaml
      2. <life_dir>/global/design-philosophy.md
      3. <life_dir>/domains/design/profile.yaml
      4. <life_dir>/domains/design/design-philosophy.md

    Falls back to a clean, neutral, professional default if no profile is found.

    Use `DesignProfile.create_interactive(life_dir)` to generate a new profile by
    asking the user about aesthetic preferences (cars, clothes, furniture style,
    color mood, whitespace, corner style) and writing both a human-readable
    design-philosophy.md and a machine-readable design-tokens.yaml.
    """

    _SEARCH_PATHS = [
        "global/design-tokens.yaml",
        "global/design-philosophy.md",
        "domains/design/profile.yaml",
        "domains/design/design-philosophy.md",
    ]

    _DEFAULT_TOKENS = {
        "background": "#f8f8f6",
        "surface": "#ffffff",
        "text": "#111827",
        "muted": "#6b7280",
        "accent": "#1e3a5f",
        "accent-light": "#2c5282",
        "danger": "#b91c1c",
        "success": "#047857",
        "warning": "#b45309",
        "border": "#e5e7eb",
        "radius": "14px",
        "spacing": "24px",
        "shadow": "0 4px 28px rgba(17, 24, 39, 0.06)",
        "shadow-sm": "0 1px 4px rgba(17, 24, 39, 0.04)",
        "font": (
            'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", '
            'Roboto, "Helvetica Neue", Arial, sans-serif'
        ),
        "max-width": "1100px",
        "chart-line-width": "2.5",
    }

    _COLOR_MAP = {
        "white": "#ffffff",
        "off-white": "#f8f8f6",
        "charcoal": "#1f2937",
        "black": "#111827",
        "steel gray": "#6b7280",
        "steel-grey": "#6b7280",
        "deep blue": "#1e3a5f",
        "deep-blue": "#1e3a5f",
        "muted silver": "#9ca3af",
        "muted-silver": "#9ca3af",
        "navy": "#1e3a5f",
        "slate": "#475569",
        "gray": "#9ca3af",
    }

    def __init__(self, life_dir: Path):
        self.life_dir = life_dir
        self.source_path: Path | None = None
        self.raw: dict = {}
        self.tokens: dict = dict(self._DEFAULT_TOKENS)
        self._load()

    def _load(self):
        for rel in self._SEARCH_PATHS:
            path = self.life_dir / rel
            if path.exists():
                self.source_path = path
                if path.suffix in (".yaml", ".yml"):
                    try:
                        self.raw = _load_yaml_file(path) or {}
                    except Exception:
                        self.raw = {}
                    self._apply_yaml_tokens()
                else:
                    try:
                        self.raw = {"text": path.read_text(encoding="utf-8")}
                    except Exception:
                        self.raw = {}
                    self._apply_markdown_tokens()
                break

    def _apply_yaml_tokens(self):
        for key, value in self.raw.items():
            if isinstance(value, (str, int, float)):
                self.tokens[key.lower()] = str(value)

    def _apply_markdown_tokens(self):
        text = self.raw.get("text", "").lower()
        if "white" in text:
            self.tokens["surface"] = self._COLOR_MAP.get("white")
        if "off-white" in text:
            self.tokens["background"] = self._COLOR_MAP.get("off-white")
        if "charcoal" in text:
            self.tokens["text"] = self._COLOR_MAP.get("charcoal")
        if "black" in text:
            self.tokens["text"] = self._COLOR_MAP.get("black")
        if "steel gray" in text or "steel-grey" in text:
            self.tokens["muted"] = self._COLOR_MAP.get("steel gray")
        if "deep blue" in text or "deep-blue" in text:
            self.tokens["accent"] = self._COLOR_MAP.get("deep blue")
        if "muted silver" in text:
            self.tokens["border"] = self._COLOR_MAP.get("muted silver")
        if "restrained" in text or "premium" in text:
            self.tokens["shadow"] = "0 4px 28px rgba(17, 24, 39, 0.05)"
        if "generous" in text and ("white space" in text or "whitespace" in text):
            self.tokens["spacing"] = "28px"
        self.tokens["radius"] = "14px"

    def get(self, key: str, default=None):
        return self.tokens.get(key.lower(), default)

    def css_variables(self) -> str:
        lines = []
        for k, v in self.tokens.items():
            name = re.sub(r"\s+", "-", str(k))
            lines.append(f"  --{name}: {v};")
        return "\n".join(lines)

    def palette(self) -> dict:
        return {
            "background": self.get("background"),
            "surface": self.get("surface"),
            "text": self.get("text"),
            "muted": self.get("muted"),
            "border": self.get("border"),
            "accent": self.get("accent"),
            "accent-light": self.get("accent-light"),
            "danger": self.get("danger"),
            "success": self.get("success"),
            "warning": self.get("warning"),
            "chart-line-width": self.get("chart-line-width"),
        }

    @staticmethod
    def _tokens_from_choices(aesthetic, car, clothes, home, mood, space, corners):
        """Map free-form design-preference answers to a concrete token set."""
        text = " ".join([aesthetic, car, clothes, home, mood]).lower()
        tokens = dict(DesignProfile._DEFAULT_TOKENS)

        # Color mood sets the base palette.
        if "dark" in mood:
            tokens.update({
                "background": "#0f172a",
                "surface": "#1e293b",
                "text": "#f8fafc",
                "muted": "#94a3b8",
                "border": "#334155",
                "accent": "#38bdf8",
                "accent-light": "#7dd3fc",
            })
        elif "warm" in mood:
            tokens.update({
                "background": "#fafaf9",
                "surface": "#ffffff",
                "text": "#292524",
                "muted": "#78716c",
                "border": "#e7e5e4",
                "accent": "#d97706",
                "accent-light": "#f59e0b",
            })
        elif "bold" in mood or "colorful" in mood:
            tokens.update({
                "accent": "#7c3aed",
                "accent-light": "#a78bfa",
            })
        elif "cool" in mood or "crisp" in mood:
            tokens.update({
                "background": "#f8fafc",
                "surface": "#ffffff",
                "text": "#0f172a",
                "muted": "#64748b",
                "border": "#e2e8f0",
                "accent": "#1e3a5f",
                "accent-light": "#2c5282",
            })
        else:  # light & airy / default
            tokens.update({
                "background": "#ffffff",
                "surface": "#f8fafc",
                "text": "#111827",
                "muted": "#6b7280",
                "border": "#e5e7eb",
                "accent": "#0ea5e9",
                "accent-light": "#38bdf8",
            })

        # Style cues from car / clothes / home / aesthetic adjust radius & shadow.
        if any(k in text for k in ("luxury", "classic", "vintage", "traditional")):
            tokens["shadow"] = "0 8px 32px rgba(17, 24, 39, 0.08)"
            tokens["shadow-sm"] = "0 2px 8px rgba(17, 24, 39, 0.04)"
        elif any(k in text for k in ("sports", "streetwear", "industrial", "sharp")):
            tokens["radius"] = "4px"
        elif any(k in text for k in ("cozy", "casual", "eclectic", "rounded")):
            tokens["radius"] = "18px"
            tokens["shadow"] = "0 6px 24px rgba(17, 24, 39, 0.06)"
        elif any(k in text for k in ("scandinavian", "japanese", "minimal", "softly rounded")):
            tokens["radius"] = "12px"
        elif any(k in text for k in ("sleek", "contemporary", "electric", "futuristic")):
            tokens["radius"] = "8px"

        # Whitespace preference.
        if "tight" in space:
            tokens["spacing"] = "16px"
        elif "generous" in space:
            tokens["spacing"] = "32px"
        else:
            tokens["spacing"] = "24px"

        # Corner-style preference overrides style-cue radius.
        if corners == "sharp":
            tokens["radius"] = "4px"
        elif corners == "very rounded":
            tokens["radius"] = "20px"
        elif corners == "softly rounded":
            tokens["radius"] = "12px"

        return tokens

    @classmethod
    def create_interactive(cls, life_dir: Path, overwrite: bool = False) -> Path | None:
        """
        Ask the user a few taste questions and write a design profile.

        Writes:
          - <life_dir>/global/design-philosophy.md  (human-readable summary)
          - <life_dir>/global/design-tokens.yaml    (concrete tokens the report uses)

        Returns the path to design-philosophy.md, or None if the user cancels.
        """
        profile_dir = life_dir / "global"
        philosophy_path = profile_dir / "design-philosophy.md"
        tokens_path = profile_dir / "design-tokens.yaml"

        existing = [p for p in (philosophy_path, tokens_path) if p.exists()]
        if existing and not overwrite:
            print(f"Design profile already exists at {existing[0]}.")
            print("Re-run with --overwrite-design-profile to replace it.")
            return existing[0]

        profile_dir.mkdir(parents=True, exist_ok=True)

        def ask(prompt: str, default: str = "") -> str:
            try:
                answer = input(f"{prompt} [{default}]: ").strip()
            except EOFError:
                answer = ""
            return answer if answer else default

        print("\nLet's build your design profile. Defaults are shown in [brackets].")
        print("Press Enter to accept a default, or type your own answer.\n")

        aesthetic = ask("Describe your ideal look in one phrase", "clean and professional")
        car = ask("Car style you gravitate toward: classic, sports, minimalist, luxury, rugged, electric/futuristic, practical", "minimalist")
        clothes = ask("Clothing style: casual, tailored, streetwear, minimalist, vintage, outdoorsy, business", "business")
        home = ask("Furniture/home style: mid-century, scandinavian, industrial, cozy/eclectic, sleek/contemporary, traditional, japanese/minimal", "scandinavian")
        mood = ask("Color mood: light & airy, dark & moody, warm & neutral, cool & crisp, bold & colorful", "cool & crisp")
        space = ask("Whitespace preference: tight & dense, balanced, generous & airy", "balanced")
        corners = ask("Corner style: sharp, softly rounded, very rounded", "softly rounded")

        tokens = cls._tokens_from_choices(aesthetic, car, clothes, home, mood, space, corners)

        philosophy = f"""# Design Philosophy

Aesthetic: {aesthetic}.

This profile favors a {mood} palette, {space} spacing, and {corners} corners.
Taste cues include {car} cars, {clothes} clothing, and a {home} home.
"""

        tokens_yaml = {
            "background": tokens["background"],
            "surface": tokens["surface"],
            "text": tokens["text"],
            "muted": tokens["muted"],
            "accent": tokens["accent"],
            "accent-light": tokens["accent-light"],
            "danger": tokens["danger"],
            "success": tokens["success"],
            "warning": tokens["warning"],
            "border": tokens["border"],
            "radius": tokens["radius"],
            "spacing": tokens["spacing"],
            "shadow": tokens["shadow"],
            "shadow-sm": tokens["shadow-sm"],
            "font": tokens["font"],
            "max-width": tokens["max-width"],
            "chart-line-width": tokens["chart-line-width"],
        }

        philosophy_path.write_text(philosophy, encoding="utf-8")
        tokens_path.write_text(yaml.safe_dump(tokens_yaml, sort_keys=False), encoding="utf-8")

        print(f"\nDesign profile created:")
        print(f"  {philosophy_path}")
        print(f"  {tokens_path}")
        return philosophy_path


def _load_domain(life_dir: Path, name: str) -> list[dict]:
    domain_dir = life_dir / "domains" / "finance" / name
    if not domain_dir.exists():
        return []

    results = []
    for pattern in ("*.yaml", "*.yml", "*.md"):
        for path in sorted(domain_dir.glob(pattern)):
            if path.name.lower() in ("readme.md", "index.md", ".ds_store"):
                continue
            try:
                obj = _load_yaml_file(path)
            except Exception:
                continue
            if isinstance(obj, dict) and obj.get("id"):
                results.append(obj)
    return results


def _latest_snapshot_date(snapshots: list[dict]) -> str | None:
    if not snapshots:
        return None
    return max((s.get("as_of_date") or s.get("created_at") or "" for s in snapshots), default=None)


def _latest_balance(obj: dict):
    snapshots = obj.get("balance_snapshots") or []
    if not snapshots:
        return None, None
    latest = max(snapshots, key=lambda x: x.get("date", ""))
    return latest.get("balance"), latest.get("date")


def _monthly_income(src: dict) -> float:
    amount = src.get("net_amount") or src.get("gross_amount") or 0
    if not amount:
        return 0.0
    freq = src.get("frequency", "monthly")
    if freq == "one_time" or freq == "irregular":
        return 0.0
    return _to_monthly(amount, freq)


def _monthly_expense(exp: dict) -> float:
    amount = exp.get("amount", 0) or 0
    freq = exp.get("frequency", "monthly")
    if freq == "one_time":
        return 0.0
    if exp.get("monthly_equivalent") is not None:
        return float(exp["monthly_equivalent"])
    return _to_monthly(amount, freq)


# ---------------------------------------------------------------------------
# Data assembly
# ---------------------------------------------------------------------------

class FinancialData:
    def __init__(self, life_dir: Path, sample: bool = False):
        self.life_dir = life_dir
        if sample:
            self._load_sample()
        else:
            self._load_life()
        self._compute()

    def _load_sample(self):
        self.accounts = [
            {"id": "chase-checking", "schema": "finance.account", "title": "Chase Checking", "account_type": "checking", "currency": "USD", "balance_snapshots": [{"date": "2026-09-01", "balance": 4250, "source": "user_stated"}]},
            {"id": "chase-savings", "schema": "finance.account", "title": "Chase Savings", "account_type": "savings", "currency": "USD", "balance_snapshots": [{"date": "2026-09-01", "balance": 12000, "source": "user_stated"}]},
            {"id": "navy-savings", "schema": "finance.account", "title": "Navy Federal Savings", "account_type": "savings", "currency": "USD", "balance_snapshots": [{"date": "2026-09-01", "balance": 5600, "source": "user_stated"}]},
            {"id": "chase-amazon", "schema": "finance.account", "title": "Chase Amazon Card", "account_type": "credit_card", "currency": "USD", "balance_snapshots": [{"date": "2026-09-01", "balance": -890, "source": "user_stated"}]},
            {"id": "navy-platinum", "schema": "finance.account", "title": "Navy Federal Platinum", "account_type": "credit_card", "currency": "USD", "balance_snapshots": [{"date": "2026-09-01", "balance": -2400, "source": "user_stated"}]},
        ]
        self.income_sources = [
            {"id": "salary-acme", "schema": "finance.income-source", "title": "Acme Salary", "source": "Acme Corp", "income_type": "salary", "gross_amount": 0, "net_amount": 6500, "frequency": "monthly", "stability": "high", "pre_tax_deductions": [{"label": "401k", "amount": 1200, "per_paycheck": False}, {"label": "HSA", "amount": 250, "per_paycheck": False}]},
            {"id": "freelance-design", "schema": "finance.income-source", "title": "Freelance Design", "source": "Design client", "income_type": "freelance", "net_amount": 800, "frequency": "monthly", "stability": "medium"},
            {"id": "rental-income", "schema": "finance.income-source", "title": "Rental Income", "source": "Rental property", "income_type": "rental", "net_amount": 1200, "frequency": "monthly", "stability": "high"},
        ]
        self.expenses = [
            {"id": "student-loan-1", "schema": "finance.expense-profile-item", "title": "Student Loan 1", "category": "Debt", "amount": 250, "frequency": "monthly", "classification": "essential", "expense_type": "fixed"},
            {"id": "student-loan-2", "schema": "finance.expense-profile-item", "title": "Student Loan 2", "category": "Debt", "amount": 250, "frequency": "monthly", "classification": "essential", "expense_type": "fixed"},
            {"id": "auto-loan", "schema": "finance.expense-profile-item", "title": "Auto Loan", "category": "Transportation", "amount": 400, "frequency": "monthly", "classification": "essential", "expense_type": "fixed"},
            {"id": "rent", "schema": "finance.expense-profile-item", "title": "Rent", "category": "Housing", "amount": 2200, "frequency": "monthly", "classification": "essential", "expense_type": "fixed"},
            {"id": "utilities", "schema": "finance.expense-profile-item", "title": "Utilities", "category": "Utilities", "amount": 300, "frequency": "monthly", "classification": "committed", "expense_type": "variable"},
            {"id": "groceries", "schema": "finance.expense-profile-item", "title": "Groceries", "category": "Food", "amount": 600, "frequency": "monthly", "classification": "essential", "expense_type": "variable"},
            {"id": "dining-out", "schema": "finance.expense-profile-item", "title": "Dining Out", "category": "Food", "amount": 200, "frequency": "monthly", "classification": "discretionary", "expense_type": "discretionary"},
        ]
        self.debts = [
            {"id": "chase-amazon-debt", "schema": "finance.debt", "title": "Chase Amazon Card", "debt_type": "credit_card", "creditor": "Chase", "current_balance": 890, "interest_rate_pct": 24.99, "minimum_payment": 35, "payment_due_date": "15", "status": "active"},
            {"id": "navy-platinum-debt", "schema": "finance.debt", "title": "Navy Federal Platinum", "debt_type": "credit_card", "creditor": "Navy Federal", "current_balance": 2400, "interest_rate_pct": 18.99, "minimum_payment": 75, "payment_due_date": "20", "status": "active"},
            {"id": "auto-loan-debt", "schema": "finance.debt", "title": "Auto Loan", "debt_type": "auto_loan", "creditor": "Auto Lender", "current_balance": 18000, "interest_rate_pct": 5.9, "minimum_payment": 400, "payment_due_date": "1", "status": "active"},
        ]
        self.goals = [
            {"id": "emergency-fund", "schema": "finance.financial-goal", "title": "6-Month Emergency Fund", "goal_type": "six_month_safety_reserve", "target_amount": 15000, "current_amount": 0, "current_amount_as_of": "2026-09-01", "status": "active", "priority": 1, "target_basis": "calculated"},
            {"id": "vacation", "schema": "finance.financial-goal", "title": "Vacation", "goal_type": "major_purchase_savings", "target_amount": 3000, "current_amount": 0, "current_amount_as_of": "2026-09-01", "status": "active", "priority": 2},
            {"id": "payoff-credit-cards", "schema": "finance.financial-goal", "title": "Pay Off Credit Cards", "goal_type": "debt_payoff", "target_amount": 3290, "current_amount": 0, "current_amount_as_of": "2026-09-01", "status": "active", "priority": 3, "related_debt_id": "chase-amazon-debt"},
        ]
        self.snapshots = []
        self.policies = [
            {
                "id": "acme-match",
                "schema": "finance.projection-assumptions",
                "title": "Sample projection assumptions",
                "effective_date": "2026-09-01",
                "created_at": "2026-09-01",
                "annual_income_growth_pct": 0.03,
                "annual_investment_return_pct": 0.06,
                "annual_retirement_return_pct": 0.07,
                "annual_inflation_pct": 0.025,
                "annual_contribution_growth_pct": 0.02,
                "employer_match_rules": [
                    {"threshold_pct": 3.0, "match_rate": 1.0, "note": "100% of first 3%"},
                    {"threshold_pct": 2.0, "match_rate": 0.5, "note": "50% of next 2%"},
                ],
                "provenance": {"agent_version": "ethan-os/0.1.1", "provenance_note": "Sample data for report testing"},
            }
        ]

    def _load_life(self):
        self.accounts = _load_domain(self.life_dir, "accounts")
        self.income_sources = _load_domain(self.life_dir, "income-sources")
        self.expenses = _load_domain(self.life_dir, "expenses")
        self.debts = _load_domain(self.life_dir, "debts")
        self.goals = _load_domain(self.life_dir, "goals")
        self.snapshots = _load_domain(self.life_dir, "snapshots")
        # Policies are loaded together, then split into active assumptions and allocation policy.
        self.policies = _load_domain(self.life_dir, "policies")

    def _compute(self):
        # Account balances
        self.account_balances = {}
        for a in self.accounts:
            bal, as_of = _latest_balance(a)
            if bal is None:
                continue
            self.account_balances[a["id"]] = {
                "account": a,
                "balance": float(bal),
                "as_of": as_of,
                "type": a.get("account_type", "other"),
            }

        # Asset/liability split
        self.total_assets = 0.0
        self.total_liabilities = 0.0
        self.liquid_cash = 0.0
        self.retirement_balance = 0.0
        self.investment_balance = 0.0
        self.other_asset = 0.0

        for ab in self.account_balances.values():
            bal = ab["balance"]
            typ = ab["type"]
            if typ in LIABILITY_TYPES:
                # Liability account balances are intentionally not double-counted;
                # the canonical debt total comes from finance.debt objects below.
                continue
            self.total_assets += bal

            if typ in LIQUID_TYPES:
                self.liquid_cash += bal
            elif typ in RETIREMENT_TYPES:
                self.retirement_balance += bal
            elif typ in INVESTMENT_TYPES:
                self.investment_balance += bal
            else:
                self.other_asset += bal

        # Income
        self.monthly_income_total = 0.0
        self.monthly_income_reliable = 0.0
        self.monthly_income_variable = 0.0
        for src in self.income_sources:
            m = _monthly_income(src)
            self.monthly_income_total += m
            if src.get("stability") == "high":
                self.monthly_income_reliable += m
            elif src.get("stability") in ("medium", "low"):
                self.monthly_income_variable += m
            else:
                self.monthly_income_reliable += m

        # Retirement contributions
        self.monthly_retirement_contributions = 0.0
        for src in self.income_sources:
            freq = src.get("frequency", "monthly")
            for d in src.get("pre_tax_deductions", []):
                amt = d.get("amount", 0) or 0
                if d.get("per_paycheck"):
                    periods = FREQUENCY_TO_ANNUAL.get(freq, 12)
                    self.monthly_retirement_contributions += amt * periods / 12
                else:
                    self.monthly_retirement_contributions += _to_monthly(amt, "monthly")

        # Expenses
        self.monthly_expenses_total = 0.0
        self.monthly_essential = 0.0
        self.monthly_committed = 0.0
        self.monthly_discretionary = 0.0
        self.expense_by_category = {}
        for exp in self.expenses:
            if exp.get("status") == "ended":
                continue
            m = _monthly_expense(exp)
            self.monthly_expenses_total += m
            classification = exp.get("classification", "committed")
            if classification == "essential":
                self.monthly_essential += m
            elif classification == "committed":
                self.monthly_committed += m
            elif classification == "discretionary":
                self.monthly_discretionary += m

            cat = exp.get("category", "Other")
            self.expense_by_category[cat] = self.expense_by_category.get(cat, 0.0) + m

        # Debt
        self.monthly_debt_payments = 0.0
        for d in self.debts:
            if d.get("status") == "paid_off":
                continue
            self.monthly_debt_payments += d.get("minimum_payment", 0) or 0

        self.total_debt = sum((d.get("current_balance", 0) or 0) for d in self.debts if d.get("status") != "paid_off")
        self.total_liabilities = self.total_debt
        self.net_worth = self.total_assets - self.total_liabilities

        # Cash flow
        self.available_monthly_cash_flow = (
            self.monthly_income_total - self.monthly_expenses_total - self.monthly_debt_payments
        )

        # Latest snapshot date
        self.latest_snapshot_date = _latest_snapshot_date(self.snapshots)

        # Active projection assumptions and allocation policy
        self.assumptions = self._active_assumptions()
        self.active_policy = self._active_allocation_policy()

    def _active_assumptions(self):
        if not self.policies:
            return {}
        assumptions = [p for p in self.policies if p.get("schema") == "finance.projection-assumptions"]
        if not assumptions:
            return {}
        return max(assumptions, key=lambda a: a.get("effective_date", ""))

    def _active_allocation_policy(self):
        if not self.policies:
            return None
        policies = [p for p in self.policies if p.get("schema") == "finance.allocation-policy"]
        if not policies:
            return None
        return max(policies, key=lambda p: p.get("effective_date", ""))

    def assumption(self, key, default=0.0):
        """Return a value from the active projection assumptions."""
        return self.assumptions.get(key, default)


# ---------------------------------------------------------------------------
# Calculations for the report
# ---------------------------------------------------------------------------

def _payoff_months(debt: dict, monthly_payment: float) -> float | None:
    if CALC is not None and hasattr(CALC, "months_to_payoff"):
        return CALC.months_to_payoff(
            float(debt.get("current_balance", 0) or 0),
            float(debt.get("interest_rate_pct", 0) or 0),
            monthly_payment,
        )
    return None


def _monthly_growth_factor(annual_rate: float) -> float:
    if annual_rate is None or annual_rate == 0.0:
        return 0.0
    return (1 + annual_rate) ** (1 / 12) - 1


def _avalanche_extra_payment(data: FinancialData) -> float:
    return max(0.0, data.available_monthly_cash_flow)


def _project_cash_and_debt(data: FinancialData, months: int = 12) -> list[dict]:
    """Project liquid cash and remaining debt under the current plan and active assumptions."""
    inc_growth = _monthly_growth_factor(data.assumption("annual_income_growth_pct", 0.0))
    inflation = _monthly_growth_factor(data.assumption("annual_inflation_pct", 0.0))
    contrib_growth = _monthly_growth_factor(data.assumption("annual_contribution_growth_pct", 0.0))

    liquid = float(data.liquid_cash)
    debts = [
        {
            "id": d["id"],
            "balance": float(d.get("current_balance", 0) or 0),
            "rate": float(d.get("interest_rate_pct", 0) or 0),
            "min": float(d.get("minimum_payment", 0) or 0),
            "title": d.get("title", d.get("id")),
        }
        for d in data.debts
        if d.get("status") != "paid_off"
    ]

    monthly_income = float(data.monthly_income_total)
    monthly_expenses = float(data.monthly_expenses_total)
    base_extra = max(0.0, data.available_monthly_cash_flow)

    projections = []
    for i in range(months):
        # Apply growth assumptions
        monthly_income *= (1 + inc_growth)
        monthly_expenses *= (1 + inflation)
        desired_extra = base_extra * (1 + contrib_growth) ** i

        # Apply interest
        for d in debts:
            if d["balance"] > 0:
                d["balance"] += d["balance"] * d["rate"] / 100 / 12

        # Pay minimums
        total_paid = 0.0
        for d in debts:
            if d["balance"] > 0:
                payment = min(d["min"], d["balance"])
                d["balance"] -= payment
                total_paid += payment

        # Extra to highest-rate debt, limited by available cash
        available = monthly_income - monthly_expenses - total_paid
        extra_budget = min(desired_extra, max(0.0, available))
        ordered = sorted([d for d in debts if d["balance"] > 0.005], key=lambda x: x["rate"], reverse=True)
        for d in ordered:
            if extra_budget <= 0:
                break
            extra = min(extra_budget, d["balance"])
            d["balance"] -= extra
            total_paid += extra
            extra_budget -= extra

        # Cash change = income - expenses - total paid
        liquid += monthly_income - monthly_expenses - total_paid
        total_remaining = sum(max(0.0, d["balance"]) for d in debts)
        projections.append({
            "cash": round(liquid, 2),
            "debt": round(total_remaining, 2),
            "net_worth_delta": round(liquid - total_remaining, 2),
            "income": round(monthly_income, 2),
            "expenses": round(monthly_expenses, 2),
            "paid": round(total_paid, 2),
        })
    return projections


def _debt_payoff_simulation(debts: list[dict], total_monthly_payment: float, max_months: int = 360) -> dict:
    """Avalanche payoff simulation for a set of debts."""
    if not debts:
        return {"by_id": {}, "total_months": None, "total_interest_paid": 0.0, "remaining_balance": 0.0}

    balances = {d["id"]: float(d.get("balance", 0)) for d in debts}
    rates = {d["id"]: float(d.get("rate", 0)) for d in debts}
    mins = {d["id"]: float(d.get("min", 0)) for d in debts}
    payoff_months = {}
    total_interest = 0.0

    for month in range(1, max_months + 1):
        active = [i for i, b in balances.items() if b > 0.005]
        if not active:
            break

        # Apply interest
        for i in active:
            interest = balances[i] * rates[i] / 100 / 12
            balances[i] += interest
            total_interest += interest

        # Minimums
        surplus = total_monthly_payment
        for i in active:
            payment = min(mins[i], balances[i])
            balances[i] -= payment
            surplus -= payment

        # Avalanche extra
        ordered = sorted(active, key=lambda x: rates[x], reverse=True)
        for i in ordered:
            if surplus <= 0:
                break
            extra = min(surplus, balances[i])
            balances[i] -= extra
            surplus -= extra

        for i in active:
            if balances[i] <= 0.005 and i not in payoff_months:
                payoff_months[i] = month
                balances[i] = 0.0

    last_payoff = max(payoff_months.values()) if payoff_months else None
    return {
        "by_id": payoff_months,
        "total_months": last_payoff,
        "total_interest_paid": round(total_interest, 2),
        "remaining_balance": round(sum(balances.values()), 2),
    }


def _project_debt_payoff(data: FinancialData) -> dict:
    """Debt payoff scenarios: current minimums vs accelerated avalanche."""
    debts = [
        {
            "id": d["id"],
            "balance": float(d.get("current_balance", 0) or 0),
            "rate": float(d.get("interest_rate_pct", 0) or 0),
            "min": float(d.get("minimum_payment", 0) or 0),
            "title": d.get("title", d.get("id")),
        }
        for d in data.debts
        if d.get("status") != "paid_off"
    ]

    if not debts:
        return {"minimum": None, "accelerated": None}

    min_payment = sum(d["min"] for d in debts)
    minimum = _debt_payoff_simulation(debts, min_payment)

    accelerated_payment = data.monthly_debt_payments + max(0.0, data.available_monthly_cash_flow)
    accelerated = _debt_payoff_simulation(debts, accelerated_payment)

    return {"minimum": minimum, "accelerated": accelerated}


def _project_retirement(data: FinancialData, months: int = 12) -> dict:
    """Project 401k balance at year-end under active assumptions."""
    ret_return = _monthly_growth_factor(data.assumption("annual_retirement_return_pct", 0.0))
    income_growth = _monthly_growth_factor(data.assumption("annual_income_growth_pct", 0.0))
    contrib_growth = _monthly_growth_factor(data.assumption("annual_contribution_growth_pct", 0.0))
    match_rules = data.assumption("employer_match_rules", [])

    balance = float(data.retirement_balance)
    total_employee = 0.0
    total_employer = 0.0
    current_month_employee = 0.0

    for i in range(months):
        month_employee = 0.0
        month_employer = 0.0
        for src in data.income_sources:
            if src.get("status") == "ended":
                continue
            freq = src.get("frequency", "monthly")
            for d in src.get("pre_tax_deductions", []):
                if "401k" in (d.get("label") or "").lower():
                    amt = d.get("amount", 0) or 0
                    if d.get("per_paycheck"):
                        periods = FREQUENCY_TO_ANNUAL.get(freq, 12)
                        monthly = amt * periods / 12
                    else:
                        monthly = _to_monthly(amt, "monthly")
                    monthly *= (1 + contrib_growth) ** i
                    month_employee += monthly

                    salary_period = src.get("gross_amount") or src.get("net_amount") or 0
                    if salary_period:
                        salary_monthly = _to_monthly(salary_period, freq)
                        salary_monthly *= (1 + income_growth) ** i
                        employee_pct = (monthly / salary_monthly * 100) if salary_monthly > 0 else 0.0
                        tiers = [(r.get("threshold_pct", 0), r.get("match_rate", 0)) for r in match_rules]
                        if CALC is not None and hasattr(CALC, "compute_employer_match"):
                            match = CALC.compute_employer_match(employee_pct, salary_monthly, tiers, 12)
                            month_employer += match["per_paycheck_match"]
                        else:
                            remaining_pct = employee_pct
                            match_pct = 0.0
                            for threshold, rate in tiers:
                                matched = min(remaining_pct, threshold)
                                match_pct += matched * rate
                                remaining_pct -= matched
                                if remaining_pct <= 0:
                                    break
                            month_employer += match_pct / 100 * salary_monthly

        balance = (balance + month_employee + month_employer) * (1 + ret_return)
        total_employee += month_employee
        total_employer += month_employer
        current_month_employee = month_employee

    return {
        "year_end_balance": round(balance, 2),
        "total_employee_contributions": round(total_employee, 2),
        "total_employer_match": round(total_employer, 2),
        "monthly_employee_current": round(current_month_employee, 2),
    }


def _project_emergency_fund(data: FinancialData, months: int = 12) -> dict:
    """Project current savings rate toward the active 3/6 month safety reserve goal."""
    goal = next(
        (g for g in data.goals
         if g.get("status") == "active" and g.get("goal_type") in SAFETY_RESERVE_GOALS),
        None,
    )

    if goal:
        target = float(goal.get("target_amount", 0) or 0)
        current = float(goal.get("current_amount", 0) or 0)
    else:
        current = data.liquid_cash
        if data.monthly_essential > 0:
            months_reserve = 3 if data.liquid_cash < 3 * data.monthly_essential else 6
            target = months_reserve * data.monthly_essential
        else:
            target = current

    monthly_rate = goal.get("monthly_contribution") if goal and goal.get("monthly_contribution") is not None else max(0.0, data.available_monthly_cash_flow)
    monthly_rate = float(monthly_rate or 0.0)

    contrib_growth = _monthly_growth_factor(data.assumption("annual_contribution_growth_pct", 0.0))
    projected = current
    for i in range(months):
        projected += monthly_rate * (1 + contrib_growth) ** i

    months_to_target = None
    if monthly_rate > 0 and target > current:
        months_to_target = math.ceil((target - current) / monthly_rate)

    return {
        "goal": goal,
        "target": round(target, 2),
        "current": round(current, 2),
        "monthly_rate": round(monthly_rate, 2),
        "projected_in_12_months": round(projected, 2),
        "months_to_target": months_to_target,
    }


def _default_next_dollar_recommendation(data: FinancialData) -> str:
    """Generic fallback hierarchy used when no allocation policy or goals are set."""
    if data.monthly_essential <= 0:
        return "Build an expense baseline before allocating surplus cash flow."

    if data.liquid_cash < data.monthly_essential:
        return (
            f"Build your starter safety reserve. Liquid cash ({_fmt_currency(data.liquid_cash)}) "
            f"does not yet cover one month of essential expenses ({_fmt_currency(data.monthly_essential)})."
        )

    high_interest = [d for d in data.debts if d.get("status") != "paid_off" and (d.get("interest_rate_pct") or 0) > HIGH_INTEREST_THRESHOLD]
    if high_interest:
        highest = max(high_interest, key=lambda d: d.get("interest_rate_pct", 0))
        return (
            f"Put extra cash toward the highest-interest debt: {highest.get('title', highest.get('id'))} "
            f"at {highest.get('interest_rate_pct', 0)}% APR."
        )

    if data.liquid_cash < 3 * data.monthly_essential:
        return (
            f"Build a 3-month safety net. Liquid cash covers "
            f"{data.liquid_cash / data.monthly_essential:.1f} months of essential expenses; target 3."
        )

    if data.liquid_cash < 6 * data.monthly_essential:
        return (
            f"Build a 6-month safety net. Current coverage: "
            f"{data.liquid_cash / data.monthly_essential:.1f} months."
        )

    # 401k target
    retirement_goals = [g for g in data.goals if g.get("goal_type") == "annual_401k_contribution" and g.get("status") == "active"]
    if retirement_goals:
        goal = retirement_goals[0]
        target = goal.get("target_amount", 0)
        current = goal.get("current_amount", 0)
        if current < target:
            return f"Increase 401(k) contributions to reach the annual target of {_fmt_currency(target)}."

    # Taxable / other goals
    other_goals = [g for g in data.goals if g.get("status") == "active" and g.get("goal_type") in ("taxable_investment", "major_purchase_savings", "custom")]
    if other_goals:
        return f"Fund the next priority goal: {other_goals[0].get('title', other_goals[0].get('id'))}."

    return "Discretionary allocation: all higher-priority tiers appear adequately funded."


def _next_dollar_recommendation(data: FinancialData) -> str:
    """Recommend where the next dollar goes, using policy, goals, then a labeled fallback."""
    # 1. Active allocation policy tiers
    if data.active_policy:
        tiers = data.active_policy.get("tiers", [])
        if tiers:
            surplus = max(0.0, data.available_monthly_cash_flow)
            sorted_tiers = sorted(tiers, key=lambda t: t.get("priority", 99))
            for tier in sorted_tiers:
                target_type = tier.get("target_type")
                amount = tier.get("amount", 0) or 0
                label = tier.get("label", "Unnamed tier")

                if target_type == "fixed_amount":
                    needed = float(amount)
                elif target_type == "percentage":
                    needed = surplus * float(amount) / 100
                elif target_type == "remainder":
                    return f"Allocation policy: direct the next dollar to the remainder tier — {html_module.escape(label)}."
                else:
                    needed = float(amount)

                if surplus < needed:
                    return (
                        f"Allocation policy: fund tier '{html_module.escape(label)}' "
                        f"({_fmt_currency(needed)} per month, {target_type or 'fixed'})."
                    )
                surplus -= needed
            return (
                "Allocation policy: the active tiers are on track for this month's cash flow. "
                "Distribute any additional surplus according to the policy's remainder tier or priorities."
            )

    # 2. Active goals by priority
    active_goals = [g for g in data.goals if g.get("status") == "active"]
    if active_goals:
        active_goals.sort(key=lambda g: (g.get("priority") or 99, g.get("target_amount") or 0))
        for g in active_goals:
            target = g.get("target_amount", 0) or 0
            current = g.get("current_amount", 0) or 0
            if current < target:
                return (
                    f"Next priority goal: {html_module.escape(g.get('title', g.get('id')))} "
                    f"— {_fmt_currency(target - current)} remaining."
                )
        return "Active goals appear fully funded for their target amounts."

    # 3. Fallback default hierarchy
    fallback = _default_next_dollar_recommendation(data)
    return f"Default recommendation — no allocation policy or goals set. {fallback}"


# ---------------------------------------------------------------------------
# Visualization helpers
# ---------------------------------------------------------------------------

def _progress_bar(value, max_value, color="#2563eb"):
    pct = min(100.0, max(0.0, (value / max_value * 100) if max_value else 0))
    return (
        f'<div class="progress"><div class="progress-bar" style="width: {pct:.1f}%; background: {color};">'
        f'</div></div>'
    )


def _svg_horizontal_bar(items, width=640, height=None, palette=None):
    """Ranked horizontal bar chart. Items are (label, value, color)."""
    if not items:
        return ""
    palette = palette or {}
    max_v = max(float(v) for _, v, _ in items)
    if max_v <= 0:
        return ""
    margin_left = 132
    margin_right = 80
    margin_top = 20
    bar_h = 22
    gap = 18
    n = len(items)
    if height is None:
        height = margin_top * 2 + n * (bar_h + gap) - gap
    plot_w = width - margin_left - margin_right
    text_c = palette.get("text", "#111827")
    muted_c = palette.get("muted", "#6b7280")

    parts = []
    for i, (label, value, color) in enumerate(items):
        y = margin_top + i * (bar_h + gap)
        bar_w = float(value) / max_v * plot_w
        parts.append(
            f'<rect x="{margin_left}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" '
            f'fill="{color}" rx="4" data-tooltip="{html_module.escape(label)}: {_fmt_currency(value)}" />'
        )
        parts.append(
            f'<text x="{margin_left - 10}" y="{y + bar_h / 2 + 4}" text-anchor="end" '
            f'font-size="12" fill="{text_c}">{html_module.escape(label)}</text>'
        )
        parts.append(
            f'<text x="{margin_left + bar_w + 8}" y="{y + bar_h / 2 + 4}" font-size="12" '
            f'fill="{muted_c}">{_fmt_currency(value)}</text>'
        )
    return f'<svg viewBox="0 0 {width} {height}" class="bar-chart">{"".join(parts)}</svg>'


def _svg_line_chart(labels, series, width=800, height=260, palette=None, fill_area=False):
    if not labels or not series:
        return ""
    all_values = [float(v) for _, _, values in series for v in values if v is not None]
    if not all_values:
        return ""
    min_v = min(all_values)
    max_v = max(all_values)
    y_min = 0.0 if min_v >= 0 else min_v * 1.1
    y_max = max_v * 1.1 if max_v > 0 else max_v / 1.1
    span = y_max - y_min if y_max != y_min else 1.0

    n = len(labels)
    left = 54
    right = width - 24
    top = 24
    bottom = height - 46
    plot_w = right - left
    plot_h = bottom - top

    def x(i):
        return left + (i / (n - 1) * plot_w) if n > 1 else left + plot_w / 2

    def y(v):
        return bottom - ((v - y_min) / span * plot_h)

    palette = palette or {}
    border_c = palette.get("border", "#e5e7eb")
    muted_c = palette.get("muted", "#6b7280")
    surface_c = palette.get("surface", "#ffffff")

    parts = []
    for j in range(5):
        gy = top + j * plot_h / 4
        parts.append(
            f'<line x1="{left}" y1="{gy}" x2="{right}" y2="{gy}" stroke="{border_c}" stroke-width="0.5" />'
        )
    parts.append(
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{muted_c}" stroke-width="1" />'
    )
    parts.append(
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="{muted_c}" stroke-width="1" />'
    )

    step = max(1, len(labels) // 6)
    for i, label in enumerate(labels):
        if i % step == 0 or i == len(labels) - 1:
            parts.append(
                f'<text x="{x(i)}" y="{height - 18}" font-size="11" text-anchor="middle" '
                f'fill="{muted_c}">{html_module.escape(str(label))}</text>'
            )

    for j in range(5):
        v = y_min + j * span / 4
        parts.append(
            f'<text x="{left - 8}" y="{top + (4 - j) * plot_h / 4 + 4}" font-size="10" '
            f'text-anchor="end" fill="{muted_c}">{_fmt_currency(v)}</text>'
        )

    legend_items = []
    for name, color, _ in series:
        legend_items.append(
            f'<span><span class="legend-dot" style="background:{color};"></span>{html_module.escape(name)}</span>'
        )
    legend_html = '<div class="chart-legend">' + "".join(legend_items) + "</div>"

    for name, color, values in series:
        points = [(x(i), y(v)) for i, v in enumerate(values) if v is not None]
        if len(points) < 2:
            continue
        d = f"M {points[0][0]} {points[0][1]}" + "".join(f" L {px} {py}" for px, py in points[1:])
        if fill_area:
            d_area = (
                f"M {points[0][0]} {bottom} "
                + " ".join(f"L {px} {py}" for px, py in points)
                + f" L {points[-1][0]} {bottom} Z"
            )
            parts.append(
                f'<path d="{d_area}" fill="{color}" fill-opacity="0.08" stroke="none" />'
            )
        parts.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{palette.get("chart-line-width", "2.5")}" '
            f'stroke-linecap="round" stroke-linejoin="round" />'
        )
        for i, v in enumerate(values):
            if v is None:
                continue
            px, py = x(i), y(v)
            parts.append(
                f'<circle cx="{px}" cy="{py}" r="3.5" fill="{color}" stroke="{surface_c}" stroke-width="1.5" '
                f'data-tooltip="{html_module.escape(name)}: {_fmt_currency(v)}" />'
            )
    return legend_html + f'<svg viewBox="0 0 {width} {height}" class="line-chart">{"".join(parts)}</svg>'


def _svg_stacked_bar(segments, width=640, height=96, palette=None):
    """Single horizontal stacked bar. Segments are (label, value, color)."""
    if not segments:
        return ""
    total = sum(float(v) for _, v, _ in segments)
    if total <= 0:
        return ""
    palette = palette or {}
    text_c = palette.get("text", "#111827")
    margin = 24
    plot_w = width - 2 * margin
    y = 30
    bar_h = 28
    x = margin

    parts = []
    for label, value, color in segments:
        frac = float(value) / total
        seg_w = frac * plot_w
        parts.append(
            f'<rect x="{x}" y="{y}" width="{seg_w:.1f}" height="{bar_h}" fill="{color}" '
            f'data-tooltip="{html_module.escape(label)}: {_fmt_currency(value)} ({frac*100:.1f}%)" />'
        )
        if seg_w > 44:
            parts.append(
                f'<text x="{x + seg_w / 2}" y="{y + bar_h / 2 + 4}" text-anchor="middle" '
                f'font-size="11" fill="#ffffff" font-weight="500">{frac*100:.0f}%</text>'
            )
        x += seg_w

    parts.append(
        f'<text x="{margin - 8}" y="{y + bar_h / 2 + 4}" text-anchor="end" font-size="12" '
        f'fill="{text_c}" font-weight="600">{_fmt_currency(total)}</text>'
    )

    legend_items = []
    for label, value, color in segments:
        legend_items.append(
            f'<span><span class="legend-dot" style="background:{color};"></span>'
            f'{html_module.escape(label)} <span class="muted">{_fmt_currency(value)}</span></span>'
        )
    legend_html = '<div class="chart-legend">' + "".join(legend_items) + "</div>"
    return legend_html + f'<svg viewBox="0 0 {width} {height}" class="stacked-bar-chart">{"".join(parts)}</svg>'


def _svg_donut(segments, width=320, height=320, palette=None, hole=0.55):
    """Donut chart. Segments are (label, value, color)."""
    if not segments:
        return ""
    total = sum(float(v) for _, v, _ in segments)
    if total <= 0:
        return ""
    palette = palette or {}
    surface_c = palette.get("surface", "#ffffff")
    muted_c = palette.get("muted", "#6b7280")
    cx, cy = width / 2, height / 2
    r = min(cx, cy) * 0.8
    hole_r = r * hole
    start = -math.pi / 2

    parts = []
    for label, value, color in segments:
        frac = float(value) / total
        angle = frac * 2 * math.pi
        end = start + angle
        x1 = cx + r * math.cos(start)
        y1 = cy + r * math.sin(start)
        x2 = cx + r * math.cos(end)
        y2 = cy + r * math.sin(end)
        hx1 = cx + hole_r * math.cos(end)
        hy1 = cy + hole_r * math.sin(end)
        hx2 = cx + hole_r * math.cos(start)
        hy2 = cy + hole_r * math.sin(start)
        large = 1 if angle > math.pi else 0
        path = (
            f"M {x1} {y1} A {r} {r} 0 {large} 1 {x2} {y2} "
            f"L {hx1} {hy1} A {hole_r} {hole_r} 0 {large} 0 {hx2} {hy2} Z"
        )
        parts.append(
            f'<path d="{path}" fill="{color}" stroke="{surface_c}" stroke-width="2" '
            f'data-tooltip="{html_module.escape(label)}: {_fmt_currency(value)} ({frac*100:.1f}%)" />'
        )
        start = end

    parts.append(
        f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" '
        f'font-size="13" fill="{muted_c}">Total</text>'
    )

    legend_items = []
    for label, value, color in segments:
        legend_items.append(
            f'<span><span class="legend-dot" style="background:{color};"></span>'
            f'{html_module.escape(label)} <span class="muted">{_fmt_currency(value)}</span></span>'
        )
    legend_html = '<div class="chart-legend">' + "".join(legend_items) + "</div>"
    return legend_html + f'<svg viewBox="0 0 {width} {height}" class="donut-chart">{"".join(parts)}</svg>'


# ---------------------------------------------------------------------------
# HTML report rendering
# ---------------------------------------------------------------------------

def _css(profile: DesignProfile) -> str:
    """Render the report stylesheet from the active design tokens."""
    t = profile.tokens
    return "\n".join(
        [
            ":root {",
            profile.css_variables(),
            "}",
            "* { box-sizing: border-box; }",
            f"body {{ font-family: {t.get('font')}; background: {t.get('background')}; color: {t.get('text')}; margin: 0; padding: 0; line-height: 1.55; -webkit-font-smoothing: antialiased; }}",
            f".container {{ max-width: {t.get('max-width')}; margin: 0 auto; padding: {t.get('spacing')}; }}",
            f"header {{ margin-bottom: {t.get('spacing')}; }}",
            f"header h1 {{ font-size: 1.9rem; font-weight: 600; letter-spacing: -0.02em; margin: 0 0 0.4rem; }}",
            f"header .subtitle {{ color: {t.get('muted')}; font-size: 0.95rem; }}",
            f".card {{ background: {t.get('surface')}; border: 1px solid {t.get('border')}; border-radius: {t.get('radius')}; box-shadow: {t.get('shadow')}; padding: {t.get('spacing')}; margin-bottom: {t.get('spacing')}; }}",
            f".card-title {{ font-size: 1.15rem; font-weight: 600; margin: 0 0 1rem; letter-spacing: -0.01em; color: {t.get('text')}; }}",
            ".section-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem; }",
            ".kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem; }",
            f".kpi {{ background: {t.get('surface')}; border: 1px solid {t.get('border')}; border-radius: {t.get('radius')}; padding: 1.5rem; box-shadow: {t.get('shadow-sm')}; }}",
            f".kpi-hero {{ border-left: 4px solid {t.get('accent')}; }}",
            f".kpi-hero .label {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; color: {t.get('muted')}; margin-bottom: 0.4rem; }}",
            ".kpi-hero .value { font-size: 2.2rem; font-weight: 700; letter-spacing: -0.03em; line-height: 1.2; }",
            f".kpi-hero .sub {{ font-size: 0.9rem; color: {t.get('muted')}; margin-top: 0.35rem; }}",
            f".kpi .value.positive {{ color: {t.get('success')}; }}",
            f".kpi .value.negative {{ color: {t.get('danger')}; }}",
            ".kpi-small .value { font-size: 1.4rem; font-weight: 600; }",
            f".kpi-small .label {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: {t.get('muted')}; margin-bottom: 0.3rem; }}",
            ".two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start; }",
            "@media (max-width: 760px) { .two-col { grid-template-columns: 1fr; } }",
            ".line-chart, .bar-chart, .stacked-bar-chart, .donut-chart { width: 100%; height: auto; display: block; }",
            f".chart-legend {{ display: flex; flex-wrap: wrap; gap: 8px 18px; margin: 0.75rem 0 0.25rem; font-size: 0.9rem; color: {t.get('muted')}; }}",
            ".chart-legend span { display: inline-flex; align-items: center; }",
            ".legend-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }",
            f".progress {{ height: 10px; background: {t.get('border')}; border-radius: 999px; overflow: hidden; margin-top: 0.5rem; }}",
            f".progress-bar {{ height: 100%; border-radius: 999px; background: {t.get('accent')}; }}",
            "table { width: 100%; border-collapse: collapse; margin: 0.5rem 0; font-size: 0.92rem; }",
            f"th, td {{ padding: 0.65rem 0.75rem; text-align: left; border-bottom: 1px solid {t.get('border')}; }}",
            f"th {{ font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; color: {t.get('muted')}; background: transparent; }}",
            f"td {{ color: {t.get('text')}; }}",
            ".text-right { text-align: right; }",
            f".muted {{ color: {t.get('muted')}; }}",
            f".tag {{ display: inline-block; padding: 0.18rem 0.55rem; border-radius: 999px; font-size: 0.75rem; font-weight: 500; background: {t.get('border')}; color: {t.get('muted')}; }}",
            f".tag-essential {{ background: #fef2f2; color: {t.get('danger')}; }}",
            f".tag-committed {{ background: #fffbeb; color: {t.get('warning')}; }}",
            f".tag-discretionary {{ background: #ecfdf5; color: {t.get('success')}; }}",
            f".tag-high {{ background: #eff6ff; color: {t.get('accent')}; }}",
            ".tag-medium { background: #f5f5f4; color: #6b7280; }",
            ".tag-low { background: #f3f4f6; color: #6b7280; }",
            f"details {{ border: 1px solid {t.get('border')}; border-radius: {t.get('radius')}; overflow: hidden; margin-bottom: 0.75rem; background: {t.get('surface')}; }}",
            f"summary {{ cursor: pointer; padding: 0.9rem 1.1rem; font-weight: 500; color: {t.get('text')}; list-style: none; display: flex; justify-content: space-between; align-items: center; }}",
            "summary::-webkit-details-marker { display: none; }",
            f"summary::after {{ content: '+'; font-size: 1.3rem; color: {t.get('muted')}; font-weight: 300; }}",
            "details[open] summary::after { content: '−'; }",
            "details > .details-body { padding: 0 1.1rem 1.1rem; }",
            ".goal-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; }",
            f".goal-card {{ background: {t.get('surface')}; border: 1px solid {t.get('border')}; border-radius: {t.get('radius')}; padding: 1.25rem; box-shadow: {t.get('shadow-sm')}; }}",
            ".goal-card h4 { margin: 0 0 0.25rem; font-size: 1rem; }",
            f".goal-card .meta {{ color: {t.get('muted')}; font-size: 0.85rem; margin-bottom: 0.75rem; }}",
            ".scenarios { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1rem; }",
            f".scenario {{ background: {t.get('background')}; border: 1px solid {t.get('border')}; border-radius: {t.get('radius')}; padding: 1rem; }}",
            f".scenario strong {{ color: {t.get('accent')}; }}",
            f".disclaimer {{ border-left: 3px solid {t.get('muted')}; padding: 1rem 1.2rem; background: {t.get('background')}; color: {t.get('muted')}; font-size: 0.9rem; border-radius: 0 {t.get('radius')} {t.get('radius')} 0; }}",
            f"#tooltip {{ position: fixed; pointer-events: none; background: {t.get('text')}; color: {t.get('surface')}; padding: 0.35rem 0.6rem; border-radius: 6px; font-size: 0.8rem; z-index: 1000; opacity: 0; transition: opacity 0.12s ease; white-space: nowrap; }}",
            f"footer {{ margin-top: 2rem; color: {t.get('muted')}; font-size: 0.85rem; }}",
        ]
    )


SCRIPT = """
(function(){
  const tooltip = document.createElement('div');
  tooltip.id = 'tooltip';
  document.body.appendChild(tooltip);
  document.body.addEventListener('mouseover', function(e){
    const target = e.target.closest('[data-tooltip]');
    if (!target) return;
    tooltip.textContent = target.getAttribute('data-tooltip');
    tooltip.style.opacity = '1';
  });
  document.body.addEventListener('mousemove', function(e){
    tooltip.style.left = (e.clientX + 10) + 'px';
    tooltip.style.top = (e.clientY + 10) + 'px';
  });
  document.body.addEventListener('mouseout', function(e){
    if (e.target.closest('[data-tooltip]')) {
      tooltip.style.opacity = '0';
    }
  });
})();
"""


def _render_account_table(data: FinancialData) -> str:
    rows = []
    for ab in sorted(data.account_balances.values(), key=lambda x: x["type"]):
        bal = ab["balance"]
        rows.append(
            f"<tr>"
            f"<td>{html_module.escape(ab['account'].get('title', ab['account'].get('id')))}</td>"
            f"<td>{html_module.escape(ab['type'])}</td>"
            f'<td class="text-right">{_fmt_currency(bal)}</td>'
            f'<td class="text-right muted">{_coerce_date(ab["as_of"])}</td>'
            f"</tr>"
        )
    if not rows:
        return "<p class='muted'>No account data captured yet.</p>"
    return (
        f"<table><thead><tr><th>Account</th><th>Type</th><th class='text-right'>Balance</th><th class='text-right'>As of</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _render_income_table(data: FinancialData) -> str:
    rows = []
    for src in data.income_sources:
        monthly = _monthly_income(src)
        stability = src.get("stability", "—")
        rows.append(
            f"<tr>"
            f"<td>{html_module.escape(src.get('title', src.get('id')))}</td>"
            f"<td>{html_module.escape(src.get('source', '—'))}</td>"
            f"<td class='text-right'>{_fmt_currency(monthly)}</td>"
            f"<td class='text-right'>{html_module.escape(src.get('frequency', '—'))}</td>"
            f"<td><span class='tag tag-{stability}'>{html_module.escape(stability)}</span></td>"
            f"</tr>"
        )
    if not rows:
        return "<p class='muted'>No income sources captured yet.</p>"
    return (
        f"<table><thead><tr><th>Source</th><th>Payer</th><th class='text-right'>Monthly</th><th class='text-right'>Frequency</th><th>Stability</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _render_expense_table(data: FinancialData) -> str:
    rows = []
    for exp in data.expenses:
        monthly = _monthly_expense(exp)
        cls = exp.get("classification", "committed")
        rows.append(
            f"<tr>"
            f"<td>{html_module.escape(exp.get('title', exp.get('id')))}</td>"
            f"<td>{html_module.escape(exp.get('category', '—'))}</td>"
            f"<td class='text-right'>{_fmt_currency(monthly)}</td>"
            f"<td>{html_module.escape(exp.get('frequency', '—'))}</td>"
            f"<td><span class='tag tag-{cls}'>{html_module.escape(cls)}</span></td>"
            f"</tr>"
        )
    if not rows:
        return "<p class='muted'>No expenses captured yet.</p>"
    return (
        f"<table><thead><tr><th>Expense</th><th>Category</th><th class='text-right'>Monthly</th><th class='text-right'>Frequency</th><th>Class</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _render_debt_table(data: FinancialData) -> str:
    rows = []
    for d in sorted(data.debts, key=lambda x: x.get("interest_rate_pct", 0), reverse=True):
        min_pay = d.get("minimum_payment", 0) or 0
        extra = _avalanche_extra_payment(data)
        planned = min_pay + extra if d == max(data.debts, key=lambda x: x.get("interest_rate_pct", 0)) else min_pay
        months = _payoff_months(d, planned)
        months_display = f"{months:.1f} mo" if months is not None else "—"
        rows.append(
            f"<tr>"
            f"<td>{html_module.escape(d.get('title', d.get('id')))}</td>"
            f"<td class='text-right'>{_fmt_currency(d.get('current_balance'))}</td>"
            f"<td class='text-right'>{_fmt_percent(d.get('interest_rate_pct'))}</td>"
            f"<td class='text-right'>{_fmt_currency(min_pay)}</td>"
            f"<td class='text-right'>{_fmt_currency(planned)}</td>"
            f"<td class='text-right'>{html_module.escape(months_display)}</td>"
            f"</tr>"
        )
    if not rows:
        return "<p class='muted'>No debts captured yet.</p>"
    return (
        f"<table><thead><tr><th>Debt</th><th class='text-right'>Balance</th><th class='text-right'>APR</th>"
        f"<th class='text-right'>Minimum</th><th class='text-right'>Planned</th><th class='text-right'>Payoff</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _render_goals(data: FinancialData) -> str:
    rows = []
    for g in sorted(data.goals, key=lambda x: (x.get("priority") or 99)):
        target = g.get("target_amount", 0) or 0
        current = g.get("current_amount", 0) or 0
        pct = (current / target * 100) if target else 0
        rows.append(
            f"<tr>"
            f"<td>{html_module.escape(g.get('title', g.get('id')))}</td>"
            f"<td>{html_module.escape(g.get('goal_type', '—'))}</td>"
            f'<td>{_progress_bar(current, target)}{_fmt_percent(pct)}</td>'
            f"<td class='text-right'>{_fmt_currency(target)}</td>"
            f"<td class='text-right'>{_fmt_currency(current)}</td>"
            f"<td class='text-right'>{_coerce_date(g.get('target_date'))}</td>"
            f"</tr>"
        )
    if not rows:
        return "<p class='muted'>No financial goals captured yet.</p>"
    return (
        f"<table><thead><tr><th>Goal</th><th>Type</th><th>Progress</th><th class='text-right'>Target</th><th class='text-right'>Current</th><th class='text-right'>Target Date</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _render_projection_table(projections: list[dict]) -> str:
    if not projections:
        return ""
    rows = ""
    for i, p in enumerate(projections):
        if (i + 1) not in (3, 6, 12, 36, 60):
            continue
        rows += (
            f"<tr>"
            f"<td class='text-right'>{i + 1}</td>"
            f"<td class='text-right'>{_fmt_currency(p['cash'])}</td>"
            f"<td class='text-right'>{_fmt_currency(p['debt'])}</td>"
            f"<td class='text-right'>{_fmt_currency(p['net_worth_delta'])}</td>"
            f"</tr>"
        )
    if not rows:
        return "<p class='muted'>Projection table will show at 3, 6, 12, 36, or 60 months.</p>"
    return (
        f"<table><thead><tr><th class='text-right'>Months</th><th class='text-right'>Liquid Cash</th><th class='text-right'>Remaining Debt</th><th class='text-right'>Net Position</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _render_historical_charts(data: FinancialData, palette: dict | None = None) -> str:
    if len(data.snapshots) < 2:
        return "<p class='muted'>At least two financial snapshots are required for trend charts.</p>"

    palette = palette or {}
    accent = palette.get("accent", "#1e3a5f")
    danger = palette.get("danger", "#b91c1c")
    success = palette.get("success", "#047857")

    labels = [s.get("as_of_date") or s.get("created_at") or "—" for s in data.snapshots]
    assets = [s.get("total_assets") for s in data.snapshots]
    liabilities = [s.get("total_liabilities") for s in data.snapshots]
    net_worth = [s.get("net_worth") for s in data.snapshots]
    income = [s.get("monthly_income_total") for s in data.snapshots]
    expenses = [s.get("monthly_expense_total") for s in data.snapshots]
    surplus = [s.get("monthly_surplus") for s in data.snapshots]

    chart1 = _svg_line_chart(
        labels,
        [
            ("Assets", success, assets),
            ("Liabilities", danger, liabilities),
            ("Net worth", accent, net_worth),
        ],
        palette=palette,
    )

    chart2 = _svg_line_chart(
        labels,
        [
            ("Income", success, income),
            ("Expenses", danger, expenses),
            ("Surplus", accent, surplus),
        ],
        palette=palette,
    )

    return (
        f"<div class='card'><h3 class='card-title'>Net worth, assets, and liabilities</h3>{chart1}</div>"
        f"<div class='card'><h3 class='card-title'>Cash flow over time</h3>{chart2}</div>"
    )


def _render_allocation_bar(data: FinancialData) -> str:
    total = data.monthly_essential + data.monthly_committed + data.monthly_discretionary + data.monthly_debt_payments
    if total <= 0:
        return "<p class='muted'>No expense/debt data to allocate.</p>"

    def pct(v):
        return v / total * 100

    segments = [
        ("Essential", data.monthly_essential, "#dc2626"),
        ("Committed", data.monthly_committed, "#f59e0b"),
        ("Discretionary", data.monthly_discretionary, "#16a34a"),
        ("Debt min.", data.monthly_debt_payments, "#7c3aed"),
    ]

    bar = "".join(
        f'<div class="stack-segment" style="width: {pct(v):.2f}%; background: {color};" title="{name}: {_fmt_currency(v)}"></div>'
        for name, v, color in segments
    )

    legend = " ".join(
        f'<span style="margin-right: 14px;"><span style="display:inline-block;width:10px;height:10px;background:{color};border-radius:2px;"></span> {html_module.escape(name)} {_fmt_currency(v)}</span>'
        for name, v, color in segments
    )
    return f'<div class="stack-bar">{bar}</div><div class="muted" style="margin-top:6px;">{legend}</div>'


def _render_expense_by_category(data: FinancialData) -> str:
    if not data.expense_by_category:
        return ""
    total = sum(data.expense_by_category.values())
    rows = ""
    for cat, amt in sorted(data.expense_by_category.items(), key=lambda x: -x[1]):
        pct = amt / total * 100 if total else 0
        rows += (
            f"<tr>"
            f"<td>{html_module.escape(cat)}</td>"
            f'<td class="text-right">{_fmt_currency(amt)}</td>'
            f'<td class="text-right">{pct:.1f}%</td>'
            f"</tr>"
        )
    return (
        f"<h3>Expenses by category</h3>"
        f"<table><thead><tr><th>Category</th><th class='text-right'>Monthly</th><th class='text-right'>%</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _render_safety_net(data: FinancialData) -> str:
    if data.monthly_essential <= 0:
        return "<p class='muted'>Capture essential expenses to calculate safety-net coverage.</p>"
    months = data.liquid_cash / data.monthly_essential
    return (
        f"<p>Liquid cash of {_fmt_currency(data.liquid_cash)} covers "
        f"<strong>{months:.1f} months</strong> of essential monthly expenses "
        f"({_fmt_currency(data.monthly_essential)}). Safety-net goals below assume this expense rate.</p>"
    )


def _render_debt_payoff_scenarios(data: FinancialData) -> str:
    payoff = _project_debt_payoff(data)
    if not payoff.get("minimum") or not payoff.get("accelerated"):
        return "<p class='muted'>No active debts to model payoff scenarios.</p>"

    min_total = payoff["minimum"]["total_months"]
    acc_total = payoff["accelerated"]["total_months"]
    min_display = f"{min_total:.1f}" if min_total is not None else "never (interest exceeds payments)"
    acc_display = f"{acc_total:.1f}" if acc_total is not None else "never (interest exceeds payments)"
    interest_min = _fmt_currency(payoff["minimum"]["total_interest_paid"])
    interest_acc = _fmt_currency(payoff["accelerated"]["total_interest_paid"])
    total_min_payment = data.monthly_debt_payments
    total_accel_payment = data.monthly_debt_payments + max(0.0, data.available_monthly_cash_flow)

    return (
        f"<p><strong>Scenario 1 — Current minimums only:</strong> debts paid off in <strong>{html_module.escape(str(min_display))} months</strong>; "
        f"estimated interest paid: {interest_min}. Total monthly payment: {_fmt_currency(total_min_payment)}.</p>"
        f"<p><strong>Scenario 2 — Accelerated avalanche:</strong> apply available cash flow ({_fmt_currency(max(0.0, data.available_monthly_cash_flow))}) "
        f"to the highest-interest debt first; estimated payoff in <strong>{html_module.escape(str(acc_display))} months</strong>; "
        f"estimated interest paid: {interest_acc}. Total monthly payment: {_fmt_currency(total_accel_payment)}.</p>"
        f"<p class='muted'>These are planning scenarios, not guarantees. Rates, cash flow, and behavior can change.</p>"
    )


def _render_retirement_projection(data: FinancialData) -> str:
    proj = _project_retirement(data, months=12)
    return (
        f"<p>Projected year-end 401(k) balance: <strong>{_fmt_currency(proj['year_end_balance'])}</strong>. "
        f"Employee contributions over 12 months: {_fmt_currency(proj['total_employee_contributions'])}; "
        f"employer match: {_fmt_currency(proj['total_employer_match'])}.</p>"
        f"<p class='muted'>Assumes annual retirement return of {_fmt_percent(data.assumption('annual_retirement_return_pct', 0.0) * 100)}, "
        f"contribution growth of {_fmt_percent(data.assumption('annual_contribution_growth_pct', 0.0) * 100)}, "
        f"and the configured employer match rules. Not a guarantee.</p>"
    )


def _render_emergency_fund_projection(data: FinancialData) -> str:
    proj = _project_emergency_fund(data, months=12)
    months_to_target = proj.get("months_to_target")
    return (
        f"<p>Current reserve: {_fmt_currency(proj['current'])}. Target: {_fmt_currency(proj['target'])}. "
        f"Monthly savings rate: {_fmt_currency(proj['monthly_rate'])}.</p>"
        f"<p>Projected reserve in 12 months: <strong>{_fmt_currency(proj['projected_in_12_months'])}</strong>. "
        f"Months to target at current rate: {months_to_target if months_to_target is not None else '—'}.</p>"
        f"<p class='muted'>Assumes the current monthly savings rate grows at the contribution growth assumption. Not a guarantee.</p>"
    )


def _render_current_vs_target(data: FinancialData) -> str:
    """Compare current trajectory to stated targets, when target data exists."""
    if not data.goals:
        return ""

    target_goals = [g for g in data.goals if g.get("status") == "active" and g.get("target_amount")]
    if not target_goals:
        return ""

    parts = ["<div class='section'><h3>Current Plan vs Target Plan</h3>"]
    has_content = False

    # Emergency fund
    ef = next((g for g in target_goals if g.get("goal_type") in SAFETY_RESERVE_GOALS), None)
    if ef:
        has_content = True
        target = float(ef.get("target_amount", 0) or 0)
        current = float(ef.get("current_amount", 0) or 0)
        target_date = ef.get("target_date")
        current_rate = ef.get("monthly_contribution")
        if current_rate is None:
            current_rate = max(0.0, data.available_monthly_cash_flow)

        needed = None
        months_left = None
        if target_date:
            try:
                target_dt = datetime.strptime(str(target_date)[:10], "%Y-%m-%d")
                now = datetime.now()
                months_left = max(0, (target_dt.year - now.year) * 12 + (target_dt.month - now.month))
            except Exception:
                months_left = None
        if months_left and months_left > 0 and target > current:
            needed = (target - current) / months_left

        parts.append(
            f"<h4>Emergency fund</h4>"
            f"<p>Target: {_fmt_currency(target)} by {_coerce_date(target_date)}. Current: {_fmt_currency(current)}. "
            f"Current monthly savings rate: {_fmt_currency(current_rate)}.</p>"
        )
        if needed is not None:
            parts.append(f"<p>Required monthly savings rate to hit target on time: <strong>{_fmt_currency(needed)}</strong>.</p>")

    # Retirement
    ret = next((g for g in target_goals if g.get("goal_type") == "annual_401k_contribution"), None)
    if ret:
        has_content = True
        target = float(ret.get("target_amount", 0) or 0)
        current = float(ret.get("current_amount", 0) or 0)
        ret_proj = _project_retirement(data, months=12)
        parts.append(
            f"<h4>Retirement / 401k</h4>"
            f"<p>Annual 401(k) target: {_fmt_currency(target)}. Current progress: {_fmt_currency(current)}.</p>"
            f"<p>Projected year-end 401(k) balance: <strong>{_fmt_currency(ret_proj['year_end_balance'])}</strong> "
            f"(employee contributions: {_fmt_currency(ret_proj['total_employee_contributions'])}; "
            f"employer match: {_fmt_currency(ret_proj['total_employer_match'])}).</p>"
        )

    # Debt
    payoff = _project_debt_payoff(data)
    debt_goals = [g for g in target_goals if g.get("goal_type") == "debt_payoff" or g.get("related_debt_id")]
    if debt_goals and payoff.get("minimum") and payoff.get("accelerated"):
        has_content = True
        parts.append("<h4>Debt payoff</h4>")
        for g in debt_goals:
            related = g.get("related_debt_id")
            target_date = g.get("target_date")
            title = g.get("title", g.get("id"))

            if related:
                min_m = payoff["minimum"]["by_id"].get(related)
                acc_m = payoff["accelerated"]["by_id"].get(related)
            else:
                min_m = payoff["minimum"]["total_months"]
                acc_m = payoff["accelerated"]["total_months"]

            months_to_target = None
            if target_date:
                try:
                    target_dt = datetime.strptime(str(target_date)[:10], "%Y-%m-%d")
                    now = datetime.now()
                    months_to_target = max(0, (target_dt.year - now.year) * 12 + (target_dt.month - now.month))
                except Exception:
                    pass

            min_display = f"{min_m:.1f} months" if min_m is not None else "never"
            acc_display = f"{acc_m:.1f} months" if acc_m is not None else "never"
            target_note = f" Target date {_coerce_date(target_date)} leaves {months_to_target} months." if months_to_target is not None else ""

            parts.append(
                f"<p>{html_module.escape(title)}: minimums payoff <strong>{html_module.escape(min_display)}</strong>; "
                f"accelerated avalanche <strong>{html_module.escape(acc_display)}</strong>.{target_note}</p>"
            )

    if not has_content:
        return ""
    parts.append("</div>")
    return "".join(parts)


def _render_assumptions(data: FinancialData) -> str:
    rules = data.assumption("employer_match_rules", [])
    rules_text = "; ".join(
        f"{r.get('note') or ''} ({r.get('threshold_pct', 0)}% threshold, {r.get('match_rate', 0)}x match)".strip()
        for r in rules
    ) or "None configured."

    return (
        f"<div class='section'><h3>Active projection assumptions</h3>"
        f"<p class='muted'>The values below are user-configurable assumptions. They are not facts or guarantees.</p>"
        f"<table>"
        f"<thead><tr><th>Assumption</th><th class='text-right'>Value</th></tr></thead>"
        f"<tbody>"
        f"<tr><td>Annual income growth</td><td class='text-right'>{_fmt_percent(data.assumption('annual_income_growth_pct', 0.0) * 100)}</td></tr>"
        f"<tr><td>Annual investment return</td><td class='text-right'>{_fmt_percent(data.assumption('annual_investment_return_pct', 0.0) * 100)}</td></tr>"
        f"<tr><td>Annual retirement return</td><td class='text-right'>{_fmt_percent(data.assumption('annual_retirement_return_pct', 0.0) * 100)}</td></tr>"
        f"<tr><td>Annual inflation</td><td class='text-right'>{_fmt_percent(data.assumption('annual_inflation_pct', 0.0) * 100)}</td></tr>"
        f"<tr><td>Annual contribution growth</td><td class='text-right'>{_fmt_percent(data.assumption('annual_contribution_growth_pct', 0.0) * 100)}</td></tr>"
        f"<tr><td>Employer 401(k) match rules</td><td>{html_module.escape(rules_text)}</td></tr>"
        f"</tbody></table>"
        f"</div>"
    )


def _render_report(data: FinancialData, output_path: Path) -> str:
    profile = DesignProfile(data.life_dir)
    palette = profile.palette()
    projections = _project_cash_and_debt(data, months=12)
    next_dollar = _next_dollar_recommendation(data)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    accent = palette["accent"]
    success = palette["success"]
    danger = palette["danger"]
    warning = palette["warning"]
    muted = palette["muted"]

    net_class = "positive" if data.net_worth >= 0 else "negative"
    flow_class = "positive" if data.available_monthly_cash_flow >= 0 else "negative"

    safety_months = None
    if data.monthly_essential > 0:
        safety_months = data.liquid_cash / data.monthly_essential

    sections = []

    # Header
    sections.append(
        f"<header>"
        f"<h1>Financial Review</h1>"
        f"<div class='subtitle'>Generated {generated}"
        f"{f' · Latest snapshot: {data.latest_snapshot_date}' if data.latest_snapshot_date else ''}"
        f"</div>"
        f"</header>"
    )

    # 1. Financial Overview (KPI cards)
    overview = []
    overview.append(
        f"<div class='kpi-grid'>"
        f"<div class='kpi kpi-hero'>"
        f"<div class='label'>Net worth</div>"
        f"<div class='value {net_class}'>{_fmt_currency(data.net_worth)}</div>"
        f"<div class='sub'>Assets {_fmt_currency(data.total_assets)} · Liabilities {_fmt_currency(data.total_liabilities)}</div>"
        f"</div>"
        f"<div class='kpi kpi-hero'>"
        f"<div class='label'>Available monthly cash flow</div>"
        f"<div class='value {flow_class}'>{_fmt_currency(data.available_monthly_cash_flow)}</div>"
        f"<div class='sub'>Income {_fmt_currency(data.monthly_income_total)} · Outgo {_fmt_currency(data.monthly_expenses_total + data.monthly_debt_payments)}</div>"
        f"</div>"
        f"<div class='kpi kpi-hero'>"
        f"<div class='label'>Safety-net coverage</div>"
        f"<div class='value'>{f'{safety_months:.1f} months' if safety_months is not None else '—'}</div>"
        f"<div class='sub'>Liquid cash {_fmt_currency(data.liquid_cash)} · Essentials {_fmt_currency(data.monthly_essential)}/mo</div>"
        f"</div>"
        f"</div>"
    )
    overview.append(
        f"<div class='kpi-grid'>"
        f"<div class='kpi kpi-small'><div class='label'>Liquid cash</div><div class='value'>{_fmt_currency(data.liquid_cash)}</div></div>"
        f"<div class='kpi kpi-small'><div class='label'>Monthly income</div><div class='value'>{_fmt_currency(data.monthly_income_total)}</div></div>"
        f"<div class='kpi kpi-small'><div class='label'>Monthly expenses</div><div class='value'>{_fmt_currency(data.monthly_expenses_total)}</div></div>"
        f"<div class='kpi kpi-small'><div class='label'>Total debt</div><div class='value'>{_fmt_currency(data.total_debt)}</div></div>"
        f"</div>"
    )
    sections.append(
        f"<div class='card'><h2 class='card-title'>Financial Overview</h2>{''.join(overview)}</div>"
    )

    # 2. Monthly Money Flow
    flow_items = [
        ("Monthly income", data.monthly_income_total, accent),
        ("Monthly expenses", data.monthly_expenses_total, danger),
        ("Debt minimums", data.monthly_debt_payments, warning),
        ("Available cash flow", data.available_monthly_cash_flow, success if data.available_monthly_cash_flow >= 0 else danger),
    ]
    sections.append(
        f"<div class='card'>"
        f"<h2 class='card-title'>Monthly Money Flow</h2>"
        f"{_svg_horizontal_bar(flow_items, width=760, height=180, palette=palette)}"
        f"<p class='muted'>Income versus committed and discretionary outgo. Available cash flow is what remains after expenses and minimum debt payments.</p>"
        f"</div>"
    )

    # 3. Balance Sheet
    balance_segments = [
        ("Assets", data.total_assets, success),
        ("Liabilities", data.total_liabilities, danger),
    ]
    sections.append(
        f"<div class='card'>"
        f"<h2 class='card-title'>Balance Sheet</h2>"
        f"<div class='two-col'>"
        f"<div>{_svg_donut(balance_segments, width=320, height=280, palette=palette)}</div>"
        f"<div>"
        f"<div class='kpi kpi-small' style='margin-bottom:0.75rem;'><div class='label'>Total assets</div><div class='value positive'>{_fmt_currency(data.total_assets)}</div></div>"
        f"<div class='kpi kpi-small' style='margin-bottom:0.75rem;'><div class='label'>Total liabilities</div><div class='value negative'>{_fmt_currency(data.total_liabilities)}</div></div>"
        f"<div class='kpi kpi-small' style='margin-bottom:0.75rem;'><div class='label'>Net worth</div><div class='value {net_class}'>{_fmt_currency(data.net_worth)}</div></div>"
        f"<p class='muted'>Composition of assets and liabilities. Assets include liquid cash, retirement, and investment accounts. Liabilities reflect active debt balances.</p>"
        f"</div>"
        f"</div>"
        f"</div>"
    )

    # 4. Goals
    goal_cards = []
    for g in sorted((g for g in data.goals if g.get("status") == "active"), key=lambda x: (x.get("priority") or 99)):
        target = g.get("target_amount", 0) or 0
        current = g.get("current_amount", 0) or 0
        pct = (current / target * 100) if target else 0
        remaining = max(0, target - current)
        goal_cards.append(
            f"<div class='goal-card'>"
            f"<h4>{html_module.escape(g.get('title', g.get('id')))}</h4>"
            f"<div class='meta'>{html_module.escape(g.get('goal_type', 'goal'))} · {_fmt_currency(current)} of {_fmt_currency(target)}</div>"
            f"{_progress_bar(current, target, color=accent)}"
            f"<div style='display:flex;justify-content:space-between;margin-top:0.4rem;font-size:0.85rem;color:{muted};'>"
            f"<span>{_fmt_percent(pct)}</span><span>{_fmt_currency(remaining)} remaining</span></div>"
            f"</div>"
        )
    sections.append(
        f"<div class='card'>"
        f"<h2 class='card-title'>Goals</h2>"
        f"<div class='goal-grid'>{''.join(goal_cards) if goal_cards else '<p class=\'muted\'>No active goals.</p>'}</div>"
        f"</div>"
    )

    # 5. Debt Strategy
    active_debts = [d for d in data.debts if d.get("status") != "paid_off"]
    palette_colors = [danger, warning, accent, "#6b7280", "#9ca3af", "#475569"]
    debt_segments = [
        (d.get("title", d.get("id", d["id"])), d.get("current_balance", 0) or 0, palette_colors[i % len(palette_colors)])
        for i, d in enumerate(active_debts)
    ]
    debt_ranked = sorted(
        debt_segments,
        key=lambda item: next((d.get("interest_rate_pct", 0) or 0 for d in active_debts if d.get("title", d.get("id")) == item[0]), 0),
        reverse=True,
    )
    sections.append(
        f"<div class='card'>"
        f"<h2 class='card-title'>Debt Strategy</h2>"
        f"<div class='two-col'>"
        f"<div>{_svg_donut(debt_segments, width=300, height=260, palette=palette)}</div>"
        f"<div>{_svg_horizontal_bar(debt_ranked, width=420, height=150, palette=palette)}</div>"
        f"</div>"
        f"{_render_debt_payoff_scenarios(data)}"
        f"</div>"
    )

    # 6. Projections
    cash_series = [p["cash"] for p in projections]
    debt_series = [p["debt"] for p in projections]
    net_series = [p["cash"] - p["debt"] for p in projections]
    projection_labels = [f"M{i+1}" for i in range(len(projections))]
    projection_chart = _svg_line_chart(
        projection_labels,
        [
            ("Liquid cash", success, cash_series),
            ("Remaining debt", danger, debt_series),
            ("Net position", accent, net_series),
        ],
        width=760,
        height=260,
        palette=palette,
        fill_area=True,
    )
    ef = _project_emergency_fund(data, months=12)
    ef_labels = ["Now"] + [f"M{i+1}" for i in range(1, 13)]
    ef_current = ef["current"]
    ef_target = ef["target"]
    monthly_rate = ef["monthly_rate"]
    ef_series = [ef_current + monthly_rate * i for i in range(13)]
    ef_chart = _svg_line_chart(
        ef_labels,
        [
            ("Emergency reserve", accent, ef_series),
            ("Target", warning, [ef_target] * 13),
        ],
        width=760,
        height=220,
        palette=palette,
    )
    sections.append(
        f"<div class='card'>"
        f"<h2 class='card-title'>Projections</h2>"
        f"<h3 class='card-title' style='font-size:1rem;margin-top:0;'>Cash, debt, and net position</h3>"
        f"{projection_chart}"
        f"<h3 class='card-title' style='font-size:1rem;margin-top:1.5rem;'>Emergency fund trajectory</h3>"
        f"{ef_chart}"
        f"<div class='two-col' style='margin-top:1rem;'>"
        f"<div>{_render_retirement_projection(data)}</div>"
        f"<div>{_render_emergency_fund_projection(data)}</div>"
        f"</div>"
        f"</div>"
    )

    # 7. Current Plan vs Target Plan
    current_vs_target = _render_current_vs_target(data)
    if current_vs_target:
        sections.append(current_vs_target.replace("<div class='section'>", "<div class='card'>"))

    # 8. Historical Trends
    if len(data.snapshots) >= 2:
        sections.append(
            f"<h2 class='card-title' style='margin-top:0;'>Historical Trends</h2>{_render_historical_charts(data, palette)}"
        )
    else:
        sections.append(
            f"<div class='card'><h2 class='card-title'>Historical Trends</h2>"
            f"<p class='muted'>No snapshots on file. Save a new snapshot next period to see trends.</p></div>"
        )

    # 9. Detailed Data
    details = []
    details.append(("Accounts", _render_account_table(data)))
    details.append(("Income sources", _render_income_table(data)))
    details.append(("Expenses", _render_expense_table(data)))
    details.append(("Expenses by category", _render_expense_by_category(data)))
    details.append(("Debts", _render_debt_table(data)))
    details.append(("Goals (detail)", _render_goals(data)))
    detail_html = "".join(
        f"<details><summary>{html_module.escape(title)}</summary><div class='details-body'>{content}</div></details>"
        for title, content in details
    )
    sections.append(
        f"<div class='card'><h2 class='card-title'>Detailed Data</h2>{detail_html}</div>"
    )

    # 10. Assumptions & Disclaimer
    sections.append(
        f"<div class='card'>"
        f"<h2 class='card-title'>Assumptions &amp; Disclaimer</h2>"
        f"{_render_assumptions(data)}"
        f"<div class='disclaimer' style='margin-top:1rem;'>"
        f"This report is based on information you provided. Calculations, projections, and suggestions are "
        f"planning scenarios, not professional financial, tax, investment, or legal advice. Projections use the "
        f"active assumptions listed above, but real-world results will differ. Review important decisions with a "
        f"qualified professional."
        f"</div>"
        f"</div>"
    )

    html = (
        f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Financial Report</title>"
        f"<style>{_css(profile)}</style></head><body>"
        f"<div class='container'>"
        f"{''.join(sections)}"
        f"<footer>Report file: {html_module.escape(str(output_path))}</footer>"
        f"<script>{SCRIPT}</script>"
        f"</div></body></html>"
    )
    return html


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate a financial report HTML artifact.")
    parser.add_argument("--life-dir", type=Path, help="Path to the ethan-life repository root.")
    parser.add_argument("--output", type=Path, help="Output HTML file path.")
    parser.add_argument("--sample", action="store_true", help="Generate a report using built-in sample data for testing.")
    parser.add_argument("--create-design-profile", action="store_true", help="Interactively create a design profile and exit.")
    parser.add_argument("--overwrite-design-profile", action="store_true", help="Overwrite an existing design profile when used with --create-design-profile.")
    args = parser.parse_args()

    life_dir = args.life_dir
    if not life_dir:
        # Default: ethan-life is the sibling of ethan-os, which is the grandparent of this script.
        life_dir = Path(__file__).resolve().parents[3] / "ethan-life"

    if args.create_design_profile:
        DesignProfile.create_interactive(life_dir, overwrite=args.overwrite_design_profile)
        return

    output = args.output
    if not output:
        output_dir = life_dir / "reports" / "finance"
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / f"financial-report-{datetime.now().strftime('%Y-%m-%d')}.html"

    data = FinancialData(life_dir, sample=args.sample)
    html = _render_report(data, output)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        f.write(html)

    print(f"Financial report generated: {output}")
    print(f"  Net worth: {_fmt_currency(data.net_worth)}")
    print(f"  Monthly cash flow: {_fmt_currency(data.available_monthly_cash_flow)}")


if __name__ == "__main__":
    main()

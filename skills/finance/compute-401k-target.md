# Skill: compute-401k-target

## Purpose

Calculate per-paycheck 401k contribution amounts needed to hit an annual contribution target, accounting for employer match, pay frequency, and IRS limits.

## Input

- User's gross pay per paycheck and pay frequency (from `finance.income-source`)
- Current 401k contribution rate or per-paycheck amount
- Annual contribution target (user-stated or IRS limit)
- Employer match formula, if stated (e.g. "100% of first 3%, 50% of next 2%")
- Year-to-date contributions, if stated
- Number of remaining paychecks in the year, if calculable

## Steps

1. Determine the annual target (user-stated or IRS limit for the year).
2. Calculate remaining contribution room = annual target - year-to-date contributions.
3. Calculate per-paycheck amount = remaining room / remaining paychecks.
4. Calculate per-paycheck percentage = per-paycheck amount / gross pay per paycheck.
5. If an employer match formula is known, calculate the match amount and total annual contribution (employee + employer).
6. Present results clearly with all assumptions labeled.

## Rules

- Apply `instructions/policies/mandatory/financial-guidance.md`.
- State that the result is based on the selected annual target and dated payroll inputs. Ask the user to verify contribution limits, plan rules, eligibility, match mechanics, and tax treatment before making a consequential change.
- All outputs are calculations, not facts. Label them explicitly.
- Use the user's stated salary, pay frequency, and contribution data; do not look up IRS limits unless the user asks (and then label the IRS limit as a reference, not a user fact).
- If IRS limits are referenced, note the tax year and that limits may change.
- Do not assume the user wants to max out their 401k; they state the target.
- Employer match formulas vary widely; record exactly what the user states and calculate from that.
- If year-to-date contributions are not known, ask rather than assuming $0.
- Round per-paycheck amounts to the nearest cent; note if the final paycheck needs adjustment.

## Output

A clear summary showing:

- Annual target
- Year-to-date contributions (user-stated)
- Remaining contribution room
- Per-paycheck contribution amount needed
- Per-paycheck percentage of gross pay
- Employer match amount (if formula known)
- Total annual contribution (employee + employer)
- All assumptions explicitly labeled

## Confirmation policy

- Read-only calculation: no confirmation required.
- If the user wants to update their income-source pre-tax deductions based on results, that goes through `skills/finance/capture-income-source.md`.

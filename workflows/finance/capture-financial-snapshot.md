# Workflow: capture-financial-snapshot

## Purpose

Walk the user through capturing a current financial snapshot, collecting account balances and computing summary metrics.

## Steps

1. Load all active `finance.account` objects and their most recent balance snapshots.
2. Ask the user to confirm or update each account balance. For accounts with stale snapshots (>30 days), prompt explicitly.
3. Run `skills/finance/capture-financial-snapshot.md` to create the snapshot.
4. Present the snapshot summary: total assets, total liabilities, net worth, monthly surplus.
5. If a prior snapshot exists, show the change from the last snapshot.

## Output

- Financial Snapshot object ID
- Summary of net worth, assets, liabilities, and monthly surplus
- Comparison to prior snapshot, if available

## Confirmation policy

- Auto-execute: creating the snapshot from confirmed balances.
- Ask for confirmation: when any account balance is >30 days stale.

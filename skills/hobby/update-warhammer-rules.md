# Skill: update-warhammer-rules

## Purpose

Audit and update a local, versioned Warhammer rules library for any faction and edition represented by a project's configuration and canonical collection.

## Sources

- Datasheets: use the configured faction/edition Wahapedia pages.
- Points: prefer the current official Games Workshop Munitorum Field Manual. Never substitute Wahapedia points when the official MFM is available.

## Workflow

1. Load `collection/inventory.yaml` and `purchases/plan.yaml`; collect every unique owned, planned, or ordered `unit_id`. A datasheet never implies ownership.
2. Load `rules/datasheets/*.yaml` and `rules/points/current.yaml`.
3. Verify the live faction-pack edition, version, source update date, and each relevant datasheet.
4. Verify the current official MFM version and every supported unit size. Preserve contextual cost tiers such as first-unit and subsequent-unit costs.
5. Build a complete candidate snapshot outside the canonical directory. Do not partially update canonical rules during research.
6. Run `python scripts/hobby/warhammer_rules.py --project <project> compare --candidate <candidate>`.
7. Present changed fields as `previous -> new`, unchanged count, missing/failed checks, and army-list point impacts. Do not alter list composition.
8. Ask for confirmation before applying a changed snapshot.
9. Apply with `python scripts/hobby/warhammer_rules.py --project <project> apply --candidate <candidate>`. This archives the prior datasheets and points before replacement and writes a dated report.
10. Run rules and collection validation, recalculate collection/list points, and regenerate `collection-overview.html`.

## Data rules

Each datasheet requires source provider/URL, edition, faction-pack version, source update date, retrieval date, last verification date, verification status, full profile, ranged/melee weapons and keywords, core/army/unit abilities, leader/support attachments, wargear, keywords, faction keywords, notes, and change history.

Points remain separate from datasheets and ownership. Store one record per unit size and cost tier with official MFM source metadata. Never guess uncertain values; mark the snapshot or field `needs-review` and explain why.

Use the local library first for gameplay questions. If the requested record is missing, `needs-review`, or stale, disclose that status and offer to run this audit.

## Freshness

- GREEN: recently verified and no known source-version change.
- YELLOW: verification is aging, a field needs review, or a newer source may exist.
- RED: known source update, missing required snapshot, or failed verification.

Existence alone never means current.

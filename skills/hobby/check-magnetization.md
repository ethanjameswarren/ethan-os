# Skill: check-magnetization

## Purpose

Before assembling a kit with alternate builds or weapon options, decide whether magnetization is worth the effort and record the decision.

## Input

- Kit name and game system.
- Whether the kit has alternate weapon options, alternate poses/heads, or sub-assemblies that affect future playstyles.
- User's current preference and future uncertainty.

## Output

- A decision recorded in `magnetization_status` with a `magnetization_note`.

## Instructions

1. Evaluate the kit's alternate options. Use game-system knowledge only to identify objective options, not to choose for the user.
2. Classify the decision:
   - `not_applicable` — only one configuration exists or options are cosmetic-only.
   - `recommended` — loadout choices meaningfully affect gameplay and the user is likely to change their mind.
   - `optional` — options exist but one is clearly preferred or the kit is likely to stay in one configuration.
   - `undecided` — the user has not committed; block assembly status updates until resolved.
3. Record the decision and rationale in the collection item.
4. If recommending magnetization, briefly outline what parts to magnetize and any safety/modeling notes.

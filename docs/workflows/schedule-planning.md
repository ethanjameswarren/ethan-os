# Workflow: Schedule Your Week

## What you do

Describe a change, ask for a weekly plan, or ask why the schedule feels broken.

Examples:

- "I have dinner Thursday at 7 this week."
- "From now on Wednesday night is reading night."
- "Plan my week."
- "Why do I never have time to read?"
- "My schedule isn't working. Redo it."

## What Ethan OS does

1. Identifies the intent: create, adjust, plan, or diagnose.
2. Loads your baseline schedule.
3. Loads any overrides that apply to the relevant week.
4. Loads active goals and tasks.
5. Generates a draft weekly plan:
   - fixed blocks first,
   - flexible blocks second,
   - optional blocks last.
6. Resolves conflicts by moving flexible items or dropping optional ones.
7. Warns about dependency cascades (e.g., earlier departure affects wake and bedtime).
8. Presents the plan or diagnosis.
9. Applies changes only after confirmation and at the correct scope.

## Conceptual stages

- **Capture** — understand the change or question.
- **Scope** — decide whether it is one-off, temporary, or permanent.
- **Load** — baseline, overrides, goals, tasks.
- **Generate** — produce a concrete weekly plan.
- **Resolve** — handle conflicts and dependencies.
- **Confirm** — get explicit agreement for permanent baseline changes or full rebuilds.
- **Save** — store the override, updated baseline, and accepted weekly plan.

## Outputs

- A draft or accepted `planning.weekly-plan`.
- New or updated `planning.schedule-override` objects.
- An updated `planning.baseline-schedule` only for permanent changes.
- A diagnosis with targeted recommendations when asked.

## Safeguards

- One-off and temporary changes never rewrite the baseline.
- Permanent baseline changes require explicit confirmation.
- Fixed commitments are never silently deleted.
- Optional blocks drop before flexible ones; flexible ones move before fixed ones.
- Sleep and recovery constraints are respected.
- Dependency implications are surfaced before a change is applied.

## Scope guide

| user says | scope |
|-----------|-------|
| "this week", "Thursday", "tomorrow", "just once" | one_off |
| "for the next two weeks", "until...", "while I'm on call" | temporary |
| "from now on", "every Wednesday", "make it the new normal" | permanent |

## Technical details

- Workflow: `workflows/planning/schedule-weekly-plan.md`
- Skills: `skills/planning/apply-schedule-change.md`, `skills/planning/generate-weekly-plan.md`, `skills/planning/diagnose-schedule.md`
- Schemas: `schemas/domains/planning/baseline-schedule.schema.yaml`, `weekly-plan.schema.yaml`, `schedule-override.schema.yaml`

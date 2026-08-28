# Daily Schedule

## What you do

Ask for your day, adjust it, or ask Ethan OS to fit something in.

Examples:

> **You:** "What's my schedule today?"  
> **You:** "I have dinner at 7 tonight; adjust my day."  
> **You:** "I need a workout and an hour of reading today."  
> **You:** "My meeting ran an hour late. Redo the rest of today."  
> **You:** "It's 6 PM and I still want to read tonight."

## What Ethan OS does

1. **Loads your baseline** — the normal daily structure for that day of the week.
2. **Applies today's overrides** — one-off or temporary commitments, such as a dinner at 7.
3. **Identifies hard constraints** — work, appointments, commute, sleep, recovery. These do not move unless you explicitly say so.
4. **Places flexible priorities** — workouts, reading, project work, chores. These move within today's constraints.
5. **Preserves recovery and transitions** — sleep, wind-down, meals, and travel are not squeezed out.
6. **Detects conflicts** — if a fixed commitment overlaps another fixed commitment or pushes into recovery time, the OS tells you.
7. **Makes the smallest necessary change** — it re-optimizes only the part of the day that is still open, not the entire day.
8. **Presents a simple human-readable day** — a short timeline with the changes explained.

## How today is built

```
Baseline
+ today's fixed commitments
+ temporary changes
+ current priorities
= today's plan
```

The baseline does most of the work. Today only needs adjustment where today differs.

## Replanning from the current point

If the day has already started, the OS:

- preserves completed or past blocks;
- does not rewrite history;
- looks at remaining time only;
- re-places flexible items;
- preserves hard constraints;
- drops or moves optional items if time is now too tight;
- explains any meaningful tradeoff.

## Example interaction

> **You:** "I have dinner at 7 tonight. Adjust my day."  
> **OS:** "Got it. Your normal Thursday dinner is at 6, so tonight I need to shift reading from 7 to 8:15 and move the workout to 5:15. Wind-down stays at 10. Does that work?"

## Example daily output

```
Today

5:00–5:45    Workout
5:45–6:30    Breakfast + get ready
7:00–8:00    Commute
8:00–5:00    Work
5:00–6:00    Commute
6:30–7:15    Dinner
7:15–8:00    Reading
8:00 onward  Free / wind-down

Changes today:
- Reading moved later because dinner is at 7.
```

## What you do not see

The human-facing output does not show:

- schema metadata;
- scheduling scores or weights;
- internal routing information;
- uncertainty ratings.

If you want to inspect the underlying plan object, you can ask for it.

## Core principle

**The user should not rebuild their day every morning.**

Your baseline carries the normal structure. Today only changes where today is different.

## Safeguards

- One-off commitments do not become permanent baseline changes.
- Fixed commitments are never silently deleted.
- Sleep and recovery are protected.
- Mid-day replanning preserves the past and only adjusts the future.
- Dependency implications are surfaced (e.g., earlier departure → earlier wake).

## Technical details

- Workflow: `workflows/planning/schedule-weekly-plan.md`
- Skills: `skills/planning/apply-schedule-change.md`, `skills/planning/generate-weekly-plan.md`, `skills/planning/diagnose-schedule.md`
- Schemas: `schemas/domains/planning/baseline-schedule.schema.yaml`, `weekly-plan.schema.yaml`, `schedule-override.schema.yaml`
- For the broader Schedule Planning domain, see [Schedule Planning](../capabilities/schedule-planning.md).

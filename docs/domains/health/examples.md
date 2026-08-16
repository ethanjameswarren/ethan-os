# Health Domain Examples

## Capture

> slept 7.5 hours, went for a 30 min run this morning, feeling pretty good today

## Resulting objects

- Log Entry: metric_type "sleep", value "7.5 hours"
- Log Entry: metric_type "exercise", value "30 min run", linked to the existing "Run 3x/week" Habit
- Log Entry: metric_type "mood", value "good"

`log-metric` recomputes the "Run 3x/week" habit's `current_streak` to include today's run.

## Weekly review

`weekly-health-review` surfaces:

- "Run 3x/week" habit has a 4-day streak — no flag
- "Meditate daily" habit has no logs in 5 days — surfaced as a broken streak

## Medical note

> saw dr. patel for the annual physical, everything looked fine, follow up in a year

Resulting Medical Note: note_type "appointment", provider "Dr. Patel", summary "Annual physical, no issues found", follow_up "Next annual physical in ~1 year", status "resolved".

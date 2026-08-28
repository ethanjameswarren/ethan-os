---
id: demo-baseline-schedule
schema: planning.baseline-schedule
schema_version: 1
title: Demo baseline schedule
status: active
created_at: 2026-01-05T08:00:00Z
provenance:
  source: user
  captured_at: 2026-01-05T08:00:00Z
recurring_blocks:
  - day_of_week: Monday
    start_time: "07:00"
    end_time: "08:00"
    label: morning routine
    category: fixed
  - day_of_week: Monday
    start_time: "08:00"
    end_time: "09:00"
    label: commute
    category: fixed
  - day_of_week: Monday
    start_time: "09:00"
    end_time: "17:00"
    label: work
    category: fixed
  - day_of_week: Monday
    start_time: "17:00"
    end_time: "18:00"
    label: commute
    category: fixed
  - day_of_week: Monday
    start_time: "18:00"
    end_time: "19:00"
    label: dinner
    category: fixed
  - day_of_week: Monday
    start_time: "19:00"
    end_time: "20:00"
    label: workout
    category: flexible
  - day_of_week: Monday
    start_time: "20:00"
    end_time: "21:00"
    label: reading
    category: flexible
  - day_of_week: Monday
    start_time: "22:00"
    end_time: "23:00"
    label: wind down
    category: recovery
  - day_of_week: Monday
    start_time: "23:00"
    end_time: "07:00"
    label: sleep
    category: recovery
  - day_of_week: Thursday
    start_time: "18:00"
    end_time: "19:00"
    label: dinner
    category: fixed
  - day_of_week: Thursday
    start_time: "19:00"
    end_time: "20:00"
    label: reading
    category: flexible
constraints:
  earliest_wake: "06:00"
  latest_bed: "23:30"
  minimum_sleep_hours: 7
preferences:
  preferred_workout_time: evening
  cognitive_work_window: morning
---

Demo baseline schedule for testing schedule-planning behavior.

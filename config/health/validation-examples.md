# Health Equipment / Location Validation Examples

These examples demonstrate the new `health.training-location`, `health.exercise`, `health.equipment`, and `health.workout` architecture using `scripts/health/gym_query.py`.

All examples use the `apartment-gym` training location from the 2026-08-31 photo audit.

## 1. What chest exercises can I do at Apartment Gym?

```powershell
python ethan-os/scripts/health/gym_query.py --chest
```

Output:

```
Available chest exercises at Apartment Gym:
  cable_fly                           Cable Fly                           moderate load | supported
  dumbbell_bench_press                Dumbbell Bench Press                high load | free
  high_to_low_cable_fly               High-to-Low Cable Fly               moderate load | supported
  incline_dumbbell_bench_press        Incline Dumbbell Bench Press        high load | free
  low_to_high_cable_fly               Low-to-High Cable Fly               moderate load | supported
  push_up                             Push-up                             low load | free
  smith_machine_bench_press           Smith Machine Bench Press           high load | supported
  cable_chest_press                   Standing Cable Chest Press          moderate load | supported
```

## 2. Can I perform my current workout at Apartment Gym?

A sample `health.workout` object (`ethan-life/domains/health/workouts/sample-push-day.md`) was created for this test.

```powershell
python ethan-os/scripts/health/gym_query.py --workout sample-push-day
```

Output:

```
Feasibility check for "Sample Push Day" at Apartment Gym:
#   Planned                             Status          Action / Substitute
1   Barbell Bench Press                 NOT AVAILABLE   Smith Machine Bench Press
2   Barbell Back Squat                  NOT AVAILABLE   Smith Machine Back Squat
3   Dumbbell Overhead Press             OK              -
4   Cable Lateral Raise                 OK              -
5   Triceps Pushdown                    OK              -

Some exercises are not available. Substitutes listed above.
```

## 3. Replace barbell back squat with something available here.

```powershell
python ethan-os/scripts/health/gym_query.py --exercise barbell_back_squat --substitute
```

Output:

```
Barbell Back Squat is NOT available at Apartment Gym.
Closest substitute: Smith Machine Back Squat
```

## 4. Give me hamstring exercises using equipment at Apartment Gym.

```powershell
python ethan-os/scripts/health/gym_query.py --hamstring
```

Output:

```
Available hamstrings exercises at Apartment Gym:
  cable_pull_through                  Cable Pull-Through                  moderate load | supported
  cable_romanian_deadlift             Cable Romanian Deadlift             moderate load | supported
  dumbbell_romanian_deadlift          Dumbbell Romanian Deadlift          high load | free
  leg_curl                            Seated Leg Curl                     moderate load | fixed
  smith_romanian_deadlift             Smith Machine Romanian Deadlift     high load | supported
```

## 5. The Smith machine is occupied. What should I do instead?

```powershell
python ethan-os/scripts/health/gym_query.py --exclude smith_machine --chest
```

Output:

```
Available chest exercises at Apartment Gym:
  cable_fly                           Cable Fly                           moderate load | supported
  dumbbell_bench_press                Dumbbell Bench Press                high load | free
  high_to_low_cable_fly               High-to-Low Cable Fly               moderate load | supported
  incline_dumbbell_bench_press        Incline Dumbbell Bench Press        high load | free
  low_to_high_cable_fly               Low-to-High Cable Fly               moderate load | supported
  push_up                             Push-up                             low load | free
  cable_chest_press                   Standing Cable Chest Press          moderate load | supported
```

For a direct substitution when the Smith machine is occupied:

```powershell
python ethan-os/scripts/health/gym_query.py --exclude smith_machine --exercise smith_machine_bench_press --substitute
```

Output:

```
Smith Machine Bench Press is NOT available at Apartment Gym.
Closest substitute: Dumbbell Bench Press
```

## 6. Build a 45-minute workout using only Apartment Gym equipment.

```powershell
python ethan-os/scripts/health/gym_query.py --build 45
```

Output:

```
45-minute workout at Apartment Gym:
#   Exercise                            Sets  Reps     Rest
1   Smith Machine Bench Press           3     5        120s
2   Seated Cable Row                    3     8-10     90s
3   Dumbbell Bent-Over Row              3     8-10     90s
4   Smith Machine Overhead Press        3     5        120s
5   Leg Press                           3     5        120s
6   Smith Machine Romanian Deadlift     3     5        120s
```

## Notes

- The architecture checks `required_equipment` against the location inventory.
- `excluded_equipment` is treated as a temporary session constraint and does not mutate the location object.
- Substitution ranking considers movement pattern, primary muscle, stability, and loading potential.

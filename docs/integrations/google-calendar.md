# Google Calendar Integration

## What it does

Google Calendar can provide real fixed commitments to the Schedule Planning workflow. Ethan OS reads the events, normalizes them, and treats busy events as fixed blocks when generating daily or weekly plans.

Ethan OS remains the source of truth for your baseline schedule, preferences, and generated plans. Google Calendar is an external commitment source, not a replacement for your routine.

## What it does not do

- It does not copy calendar events into your baseline schedule.
- It does not automatically write Ethan OS generated plans back to Google Calendar.
- It does not treat all-day events, free events, cancelled events, or declined meetings as fixed commitments.

## Setup

1. Create a Google Cloud project and OAuth client.
2. Register the redirect URI: `http://127.0.0.1:8888/callback`.
3. Set the client credentials in your shell or private environment (never commit them):

```
GOOGLE_CLIENT_ID=<your client id>
GOOGLE_CLIENT_SECRET=<your client secret>
```

4. Run the one-time authorization script:

```
python ethan-os/scripts/calendar/auth.py
```

5. Store the printed `GOOGLE_REFRESH_TOKEN` in the same private environment.

## Choose which calendars matter

Edit `ethan-life/domains/planning/calendar-integration.yaml`:

```yaml
calendar_integration:
  provider: google
  enabled: true
  calendars:
    - id: primary
      name: Personal
      planning_behavior: fixed
    - id: <work-calendar-id>
      name: Work
      planning_behavior: fixed
    - id: <country-code>__#holiday@group.v.calendar.google.com
      name: Holidays
      planning_behavior: informational
```

`planning_behavior` can be:

- `fixed` — busy events from this calendar are treated as hard commitments.
- `informational` — events are noted but do not block time.
- `ignore` — the calendar is not read.

## Usage

Once enabled, daily and weekly planning will fetch relevant calendar events automatically before building the plan.

Example prompts:

- "What's my schedule today?"
- "Plan my week using my calendar."
- "My meeting moved to 4 PM — replan the rest of my day."

## Privacy and security

- OAuth tokens and client secrets are never written to a repository file.
- The refresh token is obtained once and kept in your private shell/environment.
- Calendar IDs and selected calendars live in `ethan-life`, not `ethan-os`.
- Public repository tests use fake fixtures, never real calendar data.

## Write-back status

Writing generated plans to Google Calendar is planned for v1.1. For v1, the integration is read-only.

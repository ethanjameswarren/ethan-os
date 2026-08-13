# Configurable Review Frequency Policy

Defines how often the system suggests reviews.

## Default configuration

- `captured` ideas older than 7 days: suggest review.
- `understood` ideas older than 30 days: suggest review.
- `internalized` ideas older than 90 days: light review.
- Ideas with low confidence: review sooner.
- Ideas with contradictions: review immediately.

## Permitted configuration

- `default`: as above.
- `aggressive`: half the default intervals.
- `relaxed`: double the default intervals.

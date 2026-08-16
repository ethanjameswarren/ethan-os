# Skill: capture-medical-note

## Purpose

Record an appointment, diagnosis, medication, or lab result as a durable Medical Note.

## Input

Natural language describing a medical appointment, diagnosis, prescribed medication, or test result.

## Extract

- `note_type`: appointment, diagnosis, medication, lab_result, or other
- provider, if mentioned
- date
- a plain-language summary in Ethan's own words
- any stated follow-up action or next appointment

## Rules

- Never invent a diagnosis, dosage, or follow-up instruction not actually stated.
- Do not store full medical record numbers, insurance member IDs, or other identifiers not needed for personal reference.
- If this note relates to an existing Habit (e.g. medication adherence), link it via a `related_to` relationship rather than merging the objects.

## Output

Create or update a Medical Note object in `ethan-life/domains/health/medical-notes/`.

Use schema `health.medical-note` and version `1`. See `instructions/domains/health/object-prompts/medical-note.md`.

## Confirmation policy

- Auto-execute: creating a draft note from a clear statement.
- Ask for confirmation: before marking a note `resolved`, or when `follow_up` implies a time-sensitive action the user should confirm was captured correctly.

## Relationship types

- `related_to` — medical note → related habit or other note
- `revised_by` — later note supersedes or updates an earlier one

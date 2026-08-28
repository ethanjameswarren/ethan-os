# Skill: capture-decision

## Purpose

Capture a meaningful, durable decision with its context, options, reasoning, and review date.

## Triggers

- "I decided to..."
- "I'm going with..."
- "I'm not doing..."
- "I chose X over Y."
- "We are using architecture A."
- "I am pausing this project."

## What to capture

Material decisions worth saving usually have:

- alternatives
- future consequences
- reasoning that may be useful later
- assumptions to test
- impact on goals or resources

Examples:

- taking or declining a job
- choosing one course over another
- pausing or resuming a project
- selecting an architecture or approach
- permanently moving a schedule block

Examples not usually worth a durable decision:

- "I'll have chicken tonight."
- "I think I'll read for 20 minutes."

## Steps

1. Identify the chosen option from the user's message.
2. Identify alternatives, if the user mentions them.
3. Extract the reasoning in the user's own words.
4. Note assumptions the user is making.
5. Note known risks or expected outcomes.
6. Link the decision to relevant goals, projects, learning, or career objects.
7. Set a `review_date` only if it makes sense.
8. Save a `knowledge.decision` object in `ethan-life/domains/knowledge/decisions/`.

## Distinctions

- **Fact:** "I chose Course A."
- **Reason:** "Course A is more relevant to the AI-engineering goal."
- **Assumption:** "I expect to finish it within four weeks."
- **Expected outcome:** "It should improve agent-evaluation knowledge."
- **Actual outcome:** captured later, in a review, not at creation.

## Rules

- Do not turn capture into a long questionnaire.
- Ask only for materially missing information.
- Preserve original reasoning; do not rewrite it to sound more certain.
- Never set `actual_outcome` at capture time.
- Preserve the distinction between expected and actual.
- A later changed decision creates a new `knowledge.decision` and links the old one as `superseded`.

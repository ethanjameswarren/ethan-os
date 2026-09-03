# Skill: generate-lore-candidates

## Purpose

Derive candidate story ideas from a battle report, hobby session, or collection milestone without promoting any of them to canon.

## Input

- Source object ID and type (`battle-report`, `session`, or `collection-item`).
- Raw events, outcomes, and user commentary.

## Output

- Zero or more `hobby.lore-candidate` Markdown files in `ethan-life/domains/hobby/<project>/candidates/`.
- A summary of candidates and why each one might matter.

## Instructions

1. Read the source object and related collection items / canon entries.
2. Look for patterns that could become lore:
   - A unit repeatedly performing the same role.
   - A model earning a nickname or notable kill.
   - A defeat suggesting doctrine change, new acquisitions, or Red/Purple escalation.
   - A character decision or paint-scheme meaning.
3. Generate one candidate per distinct idea. Set `candidate_type` to the closest category.
4. Keep the content concise and grounded in the source events.
5. Mark every candidate as `proposed`.
6. Never fabricate events that did not occur. If no candidate is justified, return none.
7. Surface all candidates to Ethan and ask whether to review them now or later.

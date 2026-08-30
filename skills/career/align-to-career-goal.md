# Skill: align-to-career-goal

## Purpose

Evaluate any proposed career action or output against the active career goal and determine whether it advances the user's declared professional direction.

The active career goal is the highest-level guidance for career decisions in Ethan OS. It informs what evidence to capture, what capabilities to strengthen, what opportunities to pursue, what learning to prioritize, and how to frame experience for external audiences.

## Inputs

- The active `career.goal` object
- A proposed action or output, such as:
  - resume content
  - LinkedIn profile section
  - Indeed profile section
  - cover letter
  - job target
  - work artifact to capture
  - project to prioritize
  - course or book to consume
  - skill to develop

## Process

### 1. Load the active career goal

Identify the active `career.goal` in `ethan-life/domains/career/goals/`. If multiple goals exist, use the one marked `active`. If none are active, ask the user to confirm or create one.

### 2. Extract goal priorities

From the goal, identify:

- target positioning themes
- desired role characteristics
- evidence dimensions to emphasize
- framings to de-emphasize
- long-term career narrative
- decision criteria

### 3. Evaluate the proposal against the goal

For the proposed content or action, determine:

- Does it demonstrate a capability the goal says to emphasize?
- Does it move toward strategic scope, architecture ownership, or cross-functional influence?
- Does it risk framing the user as execution-only or in a role the goal says to avoid?
- Does it fit the long-term narrative?
- Is there stronger evidence that would better support the goal?

### 4. Adjust framing

When presenting existing evidence, prefer language that emphasizes:

- architecture and platform building
- reusable systems and frameworks
- cross-functional ownership and strategic influence
- experimentation and business measurement
- AI enablement and agentic systems
- enterprise-scale analytics
- technical leadership without formal management authority
- translating ambiguous problems into durable systems

Avoid framing that emphasizes:

- ad-hoc report generation
- dashboard-only work
- narrowly scoped execution
- support or maintenance without ownership
- tool use without architectural context

### 5. Flag gaps

If current evidence does not strongly support the goal, surface the gap. Do not invent evidence. Recommend one of:

- capturing additional work that demonstrates the missing dimension
- reframing existing evidence more strategically
- noting the gap honestly in generated materials

### 6. Recommend next highest-leverage action

When appropriate, suggest the next action that would best move the user toward the goal. Examples:

- capture a project with stronger architecture ownership
- pursue a learning resource on AI platform design
- apply to a role with explicit strategic scope
- build a public artifact that demonstrates a target capability

## Output

Return a concise alignment assessment:

- `alignment`: strong / partial / weak / gap
- `supporting_evidence`: capabilities or artifacts that support the proposal
- `misalignment_risks`: ways the proposal might work against the goal
- `suggested_framing`: how to reframe the proposal to better fit the goal
- `gaps`: missing evidence that would strengthen alignment
- `recommended_next_action`: highest-leverage next step, if relevant

## Rules

- The active career goal takes precedence over generic best practices.
- Do not override or ignore the goal because evidence is stronger in another direction.
- Do not invent evidence to close a gap.
- Do not force every output to mention every goal priority; select the most relevant ones.
- When the user explicitly requests a different framing, honor it and optionally note how it relates to the goal.

## Confirmation policy

- Auto-execute: applying the active career goal to clear career outputs and actions.
- Ask for confirmation: when the active goal is ambiguous or missing, when a proposal appears to contradict the goal, or when reframing would materially change the meaning of the evidence.

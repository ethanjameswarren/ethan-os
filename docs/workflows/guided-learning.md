# Guided Learning Workflow

## Lifecycle

```
START
→ PRE-ASSESS
→ LEARN / SESSION
→ ACTIVE RECALL
→ DISCUSS
→ CONNECT
→ CAPTURE
→ RETAIN
→ REVIEW
→ FINISH
→ SYNTHESIZE
```

## 1. Start a program

**You say:** "I'm starting Statistics 301."

**The OS does:**

- Creates a `knowledge.learning-program`.
- Asks 0-3 short questions about prior familiarity, target, and depth.
- Records course type, provider, goals, and any known deadline.

## 2. Progress a session

**You say:** "Finished lecture 5." or "Watched the section on MCP."

**The OS does:**

- Updates `current_module_id` and `completed_module_ids`.
- Asks for active recall first.
- Asks 1-3 adaptive questions based on the course type.
- Records durable takeaways, mistakes, and real-world applications.
- Updates the `knowledge.learning-program`.

## 3. Review

**You say:** "Quiz me on this week." or "I have a midterm next week."

**The OS does:**

- Surfaces due retention items with conversational retrieval questions.
- For assessments, builds a targeted review from your sessions, weak concepts, and exam scope.
- Updates retention confidence.

## 4. Finish

**You say:** "I finished the course."

**The OS does:**

- Marks the program finished.
- Asks a brief final reflection.
- Generates a user-grounded synthesis from your sessions and insights.

## What makes the workflow feel different

- **Format-aware.** University, online, and certification programs are treated differently.
- **Low friction.** You talk; the OS structures and remembers.
- **Connected.** Course ideas can link to books, projects, tasks, and other courses.
- **Selective.** Only durable, meaningful insights are retained.

## Technical implementation

- Capability overview: `docs/capabilities/guided-learning.md`
- Workflow: `workflows/knowledge/guided-learning.md`
- Skills: `skills/knowledge/`
- Schemas: `schemas/domains/knowledge/learning-program.schema.yaml`, `learning-session.schema.yaml`

# Guided Reading Workflow

This is the human-facing lifecycle for reading a book with Ethan OS.

## Lifecycle

```
DISCOVER / ADD
→ QUEUE
→ PRE-ASSESS
→ START
→ READ
→ RECALL
→ DISCUSS
→ CONNECT
→ CAPTURE
→ RETAIN
→ REVIEW
→ FINISH
→ SYNTHESIZE
→ RECOMMEND NEXT
```

Each stage below describes what the user typically says and what the OS does in response.

## 1. Discover / add a book

**You say:** "I bought The Box." or "Add Skunk Works to my wishlist." or "I finished The Psychology of Money years ago."

**The OS does:**

- Creates or updates the book in your library.
- Sets ownership and reading status from your words:
  - bought / own → owned, unread
  - wishlist → wishlist, unread
  - finished → finished
  - borrowed → borrowed, unread
- Avoids creating duplicate books for the same work.

## 2. Queue

**You say:** "Put Dune next." or "Build me my next 5-book queue."

**The OS does:**

- Builds a coherent reading sequence from your library and goals.
- Considers owned unread books, wishlist items, recent reading, and variety.
- Lets you reorder or remove entries.

## 3. Pre-assess

**You say:** "I'm starting Dune."

**The OS does:**

- Asks 0-3 short questions about your familiarity and goals.
- Learns whether you want a light chat or deep dive.
- Establishes spoiler policy, especially for fiction.

If you already said enough — "I know the films and want to focus on politics" — it skips the questions.

## 4. Start

**The OS does:**

- Marks the book as active.
- Records your starting page.
- Associates the pre-reading profile with the book.
- Checks whether a digital copy is available for grounded discussion.

## 5. Read / report progress

**You say:** "Finished pages 1-15." or "Read through page 42." or "Did another chapter."

**The OS does:**

- Updates your progress in the canonical reading state.
- Advances the spoiler boundary to the highest page you explicitly reported.
- Checks whether actual source text is available for the range.

## 6. Active recall

**The OS says:** "Before we dig into it, what are the 1-3 things you remember most?"

**You say:** whatever comes to mind, including "honestly, not much."

**The OS does:**

- Uses your recall as the starting point for discussion.
- If you already described what stood out, it skips the prompt.

## 7. Discuss

**You say:** observations, questions, disagreements, connections.

**The OS does:**

- Asks adaptive follow-ups based on the book, your profile, and prior knowledge.
- Keeps the conversation focused and low-friction.
- For fiction, stays within the spoiler boundary.
- For nonfiction, grounds questions in actual text if available, otherwise relies on your observations and reliable general knowledge.

## 8. Connect

**The OS says:** "This sounds similar to the leverage points idea from Thinking in Systems. Do you see a link?"

**The OS does:**

- Surfaces connections to earlier ideas, books, or questions.
- Records meaningful links with context.
- Asks you to articulate the connection before explaining it.

## 9. Capture

**The OS does:**

- Saves a reading session with your observations, the discussion, extracted insights, predictions, and applications.
- Promotes only reusable, distinct insights to durable ideas.
- Leaves most detail inside the session note.

## 10. Compress and retain

**The OS does:**

- Identifies 0-3 durable takeaways from the session.
- Schedules high-value items for later review on a simple spaced schedule.
- Lets you say "skip" or "I don't care about remembering this one."

## 11. Review

**You say:** "What do I need to review?" or "Quiz me on Thinking in Systems."

**The OS does:**

- Surfaces a small number of due retention items.
- Asks retrieval questions that require you to reconstruct the idea, not pick from choices.
- Adjusts the schedule based on how well you recall.

## 12. Finish

**You say:** "I finished Dune."

**The OS does:**

- Marks the book as finished.
- Gathers a few final reflection questions if needed.
- Generates a synthesis from your actual sessions, ideas, and notes.
- Identifies strong retained ideas, weak items, and unresolved questions.

## 13. Recommend next

**You say:** "What should I read next?" or "What should I buy next?"

**The OS does:**

- Recommends from your owned unread books, wishlist, and broader interests.
- Explains why each recommendation fits.
- Lets you add a recommendation to your wishlist or remove it from future suggestions.

## What makes the workflow feel different

- **Low friction.** No forms. No mandatory page templates. No automatic flooding of your notes.
- **User in control.** You can skip recall, pause retention, archive a recommendation, or change goals mid-book.
- **Spoiler-safe.** Fiction discussions stay behind your current page unless you explicitly allow more.
- **Grounded when possible.** If you provide a digital copy, discussion can reference actual text; if not, it relies on your observations.
- **Continuity.** Ideas from one book can connect to ideas from another, and reviews keep important concepts alive.

## Example conversation

> **You:** "I'm starting Thinking in Systems."  
> **OS:** "How familiar are you with it, and is there anything you want to focus on?"  
> **You:** "Not very. I want to understand stocks and flows and how they apply at work."  
> **OS:** "I'll keep questions at a normal depth and look for applications to your work."  
>
> **You:** "Finished 1-15."  
> **OS:** "What stood out?"  
> **You:** "The stock and flow idea made me think about labor budgets."  
> **OS:** "What connection do you see?"  
> **You:** "The final labor plan number hides all the inputs that changed it."  
> **OS:** "That seems worth keeping. Want me to save it as a durable idea?"  
> **You:** "Yes."  
> *(idea saved; retention scheduled)*

## Technical implementation

- [Capability overview](../capabilities/guided-reading.md)
- [Technical reference](../../docs/domains/knowledge/guided-reading.md)
- Workflows: `workflows/knowledge/`
- Skills: `skills/knowledge/`
- Schemas: `schemas/domains/knowledge/`

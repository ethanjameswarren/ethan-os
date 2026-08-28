# Guided Reading

## What it does

You read and talk about a book. Ethan OS tracks the book, your progress, your ideas, and the connections that come up, then helps you retain what matters and decide what to read next.

It works for fiction, nonfiction, music/culture history, and other reading modes.

## Why it exists

Reading produces a stream of thoughts, highlights, and insights that usually disappear. Guided Reading turns that stream into durable, connected knowledge without making you fill out forms or organize files by hand.

The goal is not to collect every note. The goal is to capture the ideas you would want to remember months later and connect them to the rest of your knowledge.

## What you do

- Say what you are starting, continuing, or finishing.
- Answer a few conversational questions about what stood out.
- Ask questions, disagree, connect ideas to your life, or mark something important.
- Optionally provide a digital copy if you want discussions grounded in the actual text.

That is it. The OS handles note-taking, scheduling, and synthesis.

## What Ethan OS does

- Maintains your library: owned, reading, finished, wishlist, considered, and abandoned books.
- Tracks active books and current progress in one canonical place.
- Runs a short pre-reading assessment to learn your familiarity and goals.
- Begins with active recall before explaining a section.
- Asks adaptive questions based on the book, your profile, and prior knowledge.
- Protects you from fiction spoilers until you have read past the relevant material.
- Saves session notes, durable ideas, predictions, and connections.
- Schedules important ideas for spaced review.
- Generates a final synthesis from your actual sessions and notes when you finish a book.
- Recommends what to read next from your library or beyond.

## Key ideas

### Your library is the universe

Every book is tracked, not just the one you are reading now. A book can be owned but unread, on your wishlist, finished years ago, or merely considered after a recommendation.

### Progress lives in one place

Current page and spoiler boundary are kept in a single canonical reading state. Book metadata (title, author, format, ownership) lives with the book. They are separate so a book can be owned and unread, or borrowed and finished.

### Spoiler-safe by default

For fiction, the system treats your current page as a boundary. It will not reveal, imply, or confirm events, character developments, or later terminology from beyond that page unless you explicitly change the policy.

### Grounded when possible

If you provide a legitimate digital copy, the system can ground questions and discussion in the actual text. If not, it uses your observations and reliable general knowledge, without pretending it has read a specific page.

### Active recall before explanation

When you report finishing a section, the system first asks what you remember. This makes retrieval happen in your own words before the system adds context.

### Retention, not flashcards

Important ideas resurface later as conversational prompts, not as quiz questions. The schedule is simple and adaptive; you can skip, pause, or say an idea is not worth keeping.

### Recommendations are explainable

Next-book suggestions are based on your library, reading history, ratings, retained ideas, and stated interests. The system can recommend books you do not yet own, and it explains why each one fits.

## Example interaction

> **You:** "I'm starting Dune."  
> **OS:** "How familiar are you with it, and is there anything you especially want to focus on?"  
> **You:** "Very familiar — I've seen the films. I want to focus on politics, religion, power structures, and what the movies left out."  
> **OS:** "Got it. I'll treat this as a deep reread and stay at your current page for spoilers unless you say otherwise."  
>
> *(later)*  
>
> **You:** "Finished pages 1-20."  
> **OS:** "Before we dig in, what stood out?"  
> **You:** "The Bene Gesserit seem sketchy."  
> **OS:** "What makes you say that?"  
> *(conversation continues; a session note and a retention item are saved)*

## What gets saved

- **Book** — metadata, ownership, reading status, format, themes.
- **Reading profile** — your familiarity, goals, spoiler policy, discussion depth.
- **Progress state** — active books, current page, last completed range, spoiler boundary.
- **Reading sessions** — your observations, the discussion, extracted insights, predictions, connections.
- **Durable ideas** — reusable insights promoted from sessions.
- **Retention schedule** — when to review which ideas.
- **Final synthesis** — a personal summary after finishing the book.

## Important behaviors

- **No quizzes.** Active recall is conversational.
- **No automatic idea flooding.** Only reusable, distinct insights become durable ideas.
- **No Notion authority.** Notion can display reading data, but `ethan-life` is canonical.
- **No full-text dumping.** Digital copies are used for grounded discussion; the full text is not stored inside generated notes.
- **Familiarity does not imply spoiler permission.** Even if you know a story well, the default spoiler policy is explicit and conservative.
- **You can override anything.** Skip recall, pause retention, archive a book, change goals, or mark an idea unimportant.

## Related capabilities

- [Knowledge & Learning](../domains/knowledge/overview.md) — the broader domain for captures, ideas, summaries, and reviews.
- [Guided Reading workflow](../workflows/guided-reading.md) — the end-to-end lifecycle.

## Technical implementation

- [Human workflow summary](../workflows/guided-reading.md)
- [Technical reference](../../docs/domains/knowledge/guided-reading.md)
- Workflows: `workflows/knowledge/start-reading.md`, `continue-reading.md`, `discuss-reading.md`, `finish-reading.md`, `review-reading.md`, `book-recommendation.md`, `build-reading-queue.md`, `manage-book-library.md`
- Skills: `skills/knowledge/*`
- Schemas: `schemas/domains/knowledge/source.schema.yaml`, `reading-session.schema.yaml`, `reading-profile.schema.yaml`
- State: `ethan-life/domains/knowledge/reading-state.yaml`, `retention-state.yaml`

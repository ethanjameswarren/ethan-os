# Intent Router

## Purpose

Classify user input into an intent and select the corresponding workflow.

## v0.1 intents

| intent | trigger examples | workflow |
|--------|------------------|----------|
| capture | "I had a thought...", "Save this..." | `workflows/core/capture-and-route.md` |
| process learning notes | "Here are my notes on...", "Save these learning notes" | `workflows/knowledge/process-learning-notes.md` |
| start reading | "I'm starting Dune", "I'm reading Thinking in Systems", "Start a reading session for Good Strategy Bad Strategy" | `workflows/knowledge/start-reading.md` |
| continue reading | "Finished pages 1-15", "Read through page 42", "Did another chapter", "I got to page 80", "Just finished 16-32", "Did 16-32" | `workflows/knowledge/continue-reading.md` |
| discuss reading | "The Bene Gesserit seem sketchy", "This reminds me of work", "I don't buy his argument here", "What do you think about this idea?" | `workflows/knowledge/discuss-reading.md` |
| finish reading | "I finished Dune", "Done with the book", "Finished Thinking in Systems" | `workflows/knowledge/finish-reading.md` |
| reading status | "What am I reading?", "Where am I in Dune?", "What have I thought about Thinking in Systems so far?", "What books have I finished?" | `workflows/knowledge/reading-status.md` |
| review reading | "What ideas are due for review?", "Quiz me on Thinking in Systems.", "What have I retained from Dune?" | `workflows/knowledge/review-reading.md` |
| update reading profile | "I've actually read this before", "You can spoil Dune", "Don't spoil anything beyond the movies", "I want to focus more on the ecology", "Let's keep the questions lighter" | `workflows/knowledge/update-reading-profile.md` |
| manage book library | "I bought The Box.", "I own Dune already.", "Add Fooled by Randomness to my wishlist.", "I have this on Kindle.", "Mark Thinking in Systems as paused." | `workflows/knowledge/manage-book-library.md` |
| bootstrap library | "Here are the books I own...", "These are books I've already read...", "Add these to my wishlist..." | `workflows/knowledge/manage-book-library.md` |
| book recommendation | "What should I read next?", "What should I buy next?", "Give me something completely different.", "What should I read after Dune?", "Show my reading library." | `workflows/knowledge/book-recommendation.md` |
| build reading queue | "Build me my next 5-book queue.", "Put Dune next.", "Move Good Strategy after Dune.", "What's my reading queue?" | `workflows/knowledge/build-reading-queue.md` |
| reading stats | "Show my reading stats.", "What have I finished this year?", "How many books do I own that I haven't read?" | `workflows/knowledge/reading-status.md` |
| cross-reading retrieval | "What have I learned about incentives?", "What did I think about Dune's politics?", "What themes keep coming up across books?" | `workflows/knowledge/reading-status.md` |
| ask / retrieve | "What do I know about...?", "What have I learned about...?" | `workflows/core/ask.md` |
| summarize | "Summarize Atomic Habits" | `workflows/knowledge/process-learning-notes.md` (or `workflows/core/ask.md`) |
| review | "What should I review?" | `workflows/core/review.md` |
| revise | "I changed my mind about..." | `workflows/core/revise.md` |
| status | "Status", "What is pending?" | `workflows/core/status.md` |
| start listening session | "Start SK11X025", "Listen to KW34", "Lookup Holden Federico - Dust" | `workflows/music/lookup-release-and-listen.md` |
| capture listening note | "A1 energy 3, rating 4", "B2 favorite", "next", "done" | `workflows/music/capture-listening-note.md` |
| build dj set | "Build me a techno set", "Build a 90-minute hypnotic set", "Give me a driving set around 140 BPM", "Build a set from records I've rated highest", "Find some peak-time options from my collection" | `workflows/music/build-dj-set.md` |
| audition dj set | "Let's audition it", "Audition Hypnotic 01" | `workflows/music/audition-dj-set.md` |
| capture set audition feedback | "This is more of a builder", "Move this toward the end", "This works perfectly after track 4", "Don't use these two together", "next", "done" (while `active-set-audition.yaml` exists) | `workflows/music/capture-set-audition-feedback.md` |
| manage dj set | "Save that as 'Hypnotic 01'", "Open Hypnotic 01", "Confirm this set", "Mark Hypnotic 01 as played", "Archive set-20260822-001", "Remove track 6 from Hypnotic 01" | `workflows/music/manage-dj-set.md` |
| enrich dj track assessments | "Assess RYCL016 A1 for DJ use", "Assess tracks with no AI assessment", "Batch-enrich 50 more tracks", "Refresh stale AI assessments", "Reassess A2, the style read seems wrong" | `workflows/music/enrich-dj-track-assessments.md` |
| audit record labels | "Audit my record labels", "What records still need labels?", "What labels are ready to print?", "What do I need to listen to before I can finish labeling them?", "What labels are blocked only by factual metadata?" | `workflows/music/audit-record-labels.md` |
| print record labels | "Give me everything that's ready to print", "Make a sheet starting at label 11", "Print labels for RYCL016", "Reprint the label for SK11X015-A1" | `workflows/music/print-record-labels.md` |
| mark record labels | "Those are printed", "Mark RYCL016's label as applied", "SK11X015-A1 has its sticker now", "I wrote the BPM on A1" | `workflows/music/mark-record-labels.md` |
| resolve spotify track | "Find the Spotify version of this track", "Map RYCL016-A1 to Spotify", "Map my collection to Spotify", "Resolve the tracks with no Spotify match yet" | `workflows/music/resolve-spotify-track.md` |
| export dj set to spotify | "Put this set on Spotify", "Send Hypnotic 01 to Spotify", "Put the candidates for Hypnotic 01 on Spotify", "Make a Spotify playlist from these candidates" | `workflows/music/export-dj-set-to-spotify.md` |
| sync dj set to spotify | "Sync Hypnotic 01 to Spotify", "Sync the Spotify playlist" | `workflows/music/sync-dj-set-to-spotify.md` |
| review spotify matches | "Show Spotify matches that need review", "Approve the Spotify match for RYCL016-A1", "Reject that Spotify match", "Use this Spotify track instead" | `workflows/music/review-spotify-matches.md` |
| sync collection style to spotify | "Make sure my Techno records are in this playlist", "Add my [style] vinyl tracks to my [style] Spotify playlist", "Sync my collection's Techno tracks into <playlist>" | `workflows/music/sync-collection-style-to-spotify.md` |

| schedule change | "I have dinner Thursday at 7", "For the next two weeks I'm working late Tuesday", "From now on Wednesday night is reading" | `workflows/planning/schedule-weekly-plan.md` |
| plan week | "Plan my week", "What does tomorrow look like", "Make my schedule for this week" | `workflows/planning/schedule-weekly-plan.md` |
| plan day | "What's my plan today", "What does today look like" | `workflows/planning/schedule-weekly-plan.md` |
| diagnose schedule | "I never have time to read", "My schedule sucks, fix it", "Where can I fit another workout" | `workflows/planning/schedule-weekly-plan.md` |
| sunday review | "Let's do my Sunday review", "Plan next week", "What does next week look like", "Build next week's schedule" | `workflows/planning/weekly-review.md` |

## Routing rules

- If intent is ambiguous, ask for clarification.
- For substantive Life OS requests, follow the cross-repository execution order:
  `ethan-os` → `ethan-life` → `ethan-notion` → live Notion.
  Do not route directly to Notion unless the user explicitly asks for a pure Notion infrastructure or presentation change (e.g., add a database property, fix a relation, update a database ID, change a mapping).
- If input matches multiple domains but only Knowledge is enabled, route to Knowledge.
- Future domains (food, health, etc.) require enablement in `ethan-life/.ethan-os.yaml`.
- While `ethan-life/domains/music/sessions/active-set-audition.yaml` exists, short feedback-style
  messages (track references, role/energy/rating statements, "next", "done") route to
  `capture set audition feedback` rather than `capture listening note`, unless a single-release
  `current.yaml` session is also explicitly active and Ethan's message clearly refers to it.
- For reading messages, use `ethan-life/domains/knowledge/reading-state.yaml` to resolve active books.
  - Exactly one active book + a page-range or reading observation → route to `continue reading` or `discuss reading`.
  - Multiple active books + ambiguous reference → ask which book.
  - No active books + reading language → route to `start reading` or ask for the title.

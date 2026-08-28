# Universal Personal Retrieval

## Purpose

Answer natural-language questions about `ethan-life` without the user needing to know which domain owns the answer.

## Contract

- **Input**: natural-language `query`, optional `intent`, `domains`, `avoid_domains`, `entity_refs`, `time_horizon`, `desired_depth`, `top_k`.
- **Output**: ranked list of retrieval results with `object_id`, `title`, `schema`, `domain`, `status`, `source_path`, `relevance_score`, `relevance_explanation`, and `provenance`.

## Implementation

`scripts/core/universal_retrieval.py` scans the `ethan-life/domains/` tree (and demo fixtures) and indexes objects by:

- `id`
- `title`
- `tags`
- `schema` and `domain`
- `status`
- body text
- typed `links` to other objects

It does not use a vector database, a graph database, or a new canonical data store. The canonical data remains in plain Markdown and YAML.

## Ranking

Retrieval uses a transparent, deterministic score based on:

1. explicit entity references
2. title matches
3. tag matches
4. schema/domain matches
5. body text matches
6. active/current status
7. recency

Relationship traversal (one hop) is used when `depth=deep`.

## Privacy

`avoid_domains` and `domains` are respected. Sensitive domains are not loaded unless the request explicitly asks for them.

## Explainability

Every result includes a `relevance_explanation` such as:

> "Included because: title matches query terms, active/current state."

## Usage

```python
from universal_retrieval import build_retriever

r = build_retriever()
results = r.retrieve("What have I learned about agent evaluation?", top_k=10)
```

## Status

Implemented and tested. Semantic/vector search remains an optional future backend.

#!/usr/bin/env python3
"""
Universal Personal Retrieval for Ethan OS.

Searches across ethan-life and demo fixtures without requiring the caller
 to know the owning domain. Deterministic, transparent, file-based.
"""

import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), text


def _domain(schema: str | None) -> str:
    if not schema:
        return "unknown"
    return schema.split(".")[0] if "." in schema else "unknown"


def _now_utc():
    return datetime.now(timezone.utc)


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                return None
    return None


def _is_active(obj: dict) -> bool:
    status = obj.get("status")
    active_statuses = {
        "active",
        "reading",
        "learning",
        "in_progress",
        "accepted",
        "current",
        "understood",
        "captured",
        "connected",
        "testing",
        "practicing",
        "internalized",
    }
    return status in active_statuses


class UniversalRetriever:
    def __init__(self, roots: list[Path] | None = None):
        self.objects: dict[str, dict] = {}
        self.by_domain: dict[str, list[str]] = defaultdict(list)
        self.by_schema: dict[str, list[str]] = defaultdict(list)
        self.by_keyword: dict[str, set[str]] = defaultdict(set)
        self.by_link: dict[str, set[str]] = defaultdict(set)
        self.roots: list[Path] = []
        if roots:
            for root in roots:
                self.roots.append(root)
                self.load_root(root)

    def load_root(self, root: Path):
        if not root.exists():
            return
        for path in root.rglob("*.md"):
            if path.name == "README.md":
                continue
            fm, body = parse_frontmatter(path)
            if not fm or "id" not in fm:
                continue
            obj = dict(fm)
            obj["_path"] = str(path)
            obj["_body"] = body
            obj["_domain"] = _domain(obj.get("schema"))
            obj_id = obj["id"]
            self.objects[obj_id] = obj
            self.by_domain[obj["_domain"]].append(obj_id)
            self.by_schema[obj.get("schema", "unknown")].append(obj_id)

            # Index title.
            title = obj.get("title") or ""
            for token in self._tokens(title):
                self.by_keyword[token].add(obj_id)

            # Index tags.
            for tag in obj.get("tags", []) or []:
                for token in self._tokens(str(tag)):
                    self.by_keyword[token].add(obj_id)

            # Index schema name and domain.
            for token in self._tokens(obj.get("schema", "")):
                self.by_keyword[token].add(obj_id)
            for token in self._tokens(obj["_domain"]):
                self.by_keyword[token].add(obj_id)

            # Index status.
            if obj.get("status"):
                self.by_keyword[obj.get("status").lower()].add(obj_id)

            # Index body text lightly (skip common words? keep simple).
            for token in self._tokens(body):
                self.by_keyword[token].add(obj_id)

            # Index links.
            for link in obj.get("links", []) or []:
                target = link.get("target")
                if target:
                    self.by_link[obj_id].add(target)
                    self.by_link[target].add(obj_id)

    def _tokens(self, text: str) -> list[str]:
        return [t.lower() for t in re.findall(r"[A-Za-z0-9_-]+", text)]

    def _has_reason(self, obj: dict, query_tokens: set[str], entity_refs: set[str]) -> bool:
        if not query_tokens:
            return True
        obj_id = obj["id"]
        title = (obj.get("title") or "").lower()
        if obj_id in entity_refs:
            return True
        for ref in entity_refs:
            if ref and ref.lower() == title:
                return True
        title_tokens = set(self._tokens(title))
        if query_tokens & title_tokens:
            return True
        for tag in obj.get("tags", []) or []:
            if query_tokens & set(self._tokens(str(tag))):
                return True
        if query_tokens & set(self._tokens(obj.get("schema", ""))):
            return True
        body = obj.get("_body", "").lower()
        for token in query_tokens:
            if token in body:
                return True
        return False

    def _score_object(self, obj: dict, query_tokens: set[str], entity_refs: set[str], recency_weight: float) -> float:
        score = 0.0
        obj_id = obj["id"]
        title = (obj.get("title") or "").lower()

        # Exact entity reference.
        if obj_id in entity_refs:
            score += 100
        for ref in entity_refs:
            if ref and ref.lower() == title:
                score += 90

        # Keyword matches.
        title_tokens = set(self._tokens(title))
        matched = query_tokens & title_tokens
        score += len(matched) * 15

        tag_tokens = set()
        for tag in obj.get("tags", []) or []:
            tag_tokens.update(self._tokens(str(tag)))
        matched = query_tokens & tag_tokens
        score += len(matched) * 20

        schema_tokens = set(self._tokens(obj.get("schema", "")))
        matched = query_tokens & schema_tokens
        score += len(matched) * 8

        body = obj.get("_body", "").lower()
        for token in query_tokens:
            if token in body:
                score += 2

        # Active / current preference.
        if _is_active(obj):
            score += 12

        # Recency.
        updated = _parse_date(obj.get("updated_at")) or _parse_date(obj.get("created_at"))
        if updated:
            days_old = (_now_utc() - updated).days
            if days_old < 30:
                score += recency_weight
            elif days_old < 90:
                score += recency_weight * 0.5

        return score

    def _follow_links(self, seed_ids: set[str], depth: int) -> set[str]:
        visited = set(seed_ids)
        frontier = set(seed_ids)
        for _ in range(depth):
            next_frontier = set()
            for obj_id in frontier:
                for linked in self.by_link.get(obj_id, set()):
                    if linked not in visited:
                        visited.add(linked)
                        next_frontier.add(linked)
            frontier = next_frontier
        return visited - seed_ids

    def _filter(self, domains: list[str] | None, object_types: list[str] | None, avoid_domains: list[str] | None, statuses: list[str] | None):
        result = list(self.objects.values())
        if avoid_domains:
            result = [o for o in result if o["_domain"] not in avoid_domains]
        if domains:
            result = [o for o in result if o["_domain"] in domains]
        if object_types:
            result = [o for o in result if o.get("schema") in object_types]
        if statuses:
            result = [o for o in result if o.get("status") in statuses]
        return result

    def retrieve(
        self,
        query: str = "",
        intent: str = "",
        domains: list[str] | None = None,
        avoid_domains: list[str] | None = None,
        object_types: list[str] | None = None,
        entity_refs: list[str] | None = None,
        statuses: list[str] | None = None,
        top_k: int = 15,
        depth: str = "direct",
        time_horizon: str = "now",
    ) -> list[dict]:
        """Return ranked retrieval results."""
        query_text = f"{query} {intent}".strip()
        query_tokens = set(self._tokens(query_text))

        if time_horizon in ("now", "today", "this_week"):
            statuses = statuses or [
                "active", "reading", "learning", "in_progress", "accepted", "current",
                "understood", "captured", "connected", "testing", "practicing", "internalized",
            ]

        candidates = self._filter(domains, object_types, avoid_domains, statuses)

        refs = set(entity_refs or [])
        scores = []
        recency_weight = 8.0
        for obj in candidates:
            score = self._score_object(obj, query_tokens, refs, recency_weight)
            if not query_tokens or self._has_reason(obj, query_tokens, refs):
                scores.append((obj, score))

        # Sort by score descending, then recency.
        scores.sort(key=lambda x: (x[1], _parse_date(x[0].get("updated_at")) or _parse_date(x[0].get("created_at")) or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)

        top_ids = {s[0]["id"] for s in scores[:top_k]}

        # Relationship traversal for deep mode.
        if depth == "deep" and top_ids:
            linked = self._follow_links(top_ids, depth=1)
            # Add linked objects with a base score.
            for linked_id in linked:
                if linked_id not in top_ids and linked_id in self.objects:
                    linked_obj = self.objects[linked_id]
                    if avoid_domains and linked_obj["_domain"] in avoid_domains:
                        continue
                    if domains and linked_obj["_domain"] not in domains:
                        continue
                    scores.append((linked_obj, 15.0))

            # Re-sort.
            scores.sort(key=lambda x: (x[1], _parse_date(x[0].get("updated_at")) or _parse_date(x[0].get("created_at")) or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)

        results = []
        seen = set()
        for obj, score in scores:
            if len(results) >= top_k:
                break
            if obj["id"] in seen:
                continue
            seen.add(obj["id"])
            results.append({
                "object_id": obj["id"],
                "title": obj.get("title"),
                "schema": obj.get("schema"),
                "domain": obj["_domain"],
                "status": obj.get("status"),
                "source_path": obj["_path"],
                "relevance_score": round(score, 2),
                "relevance_explanation": self._explain(obj, score, query_tokens, refs),
                "provenance": {
                    "source_path": obj["_path"],
                    "schema": obj.get("schema"),
                    "retrieved_at": _now_utc().isoformat(),
                },
            })

        return results

    def _explain(self, obj: dict, score: float, query_tokens: set[str], refs: set[str]) -> str:
        reasons = []
        if obj["id"] in refs:
            reasons.append("explicit entity reference")
        title = (obj.get("title") or "").lower()
        if title and any(r and r.lower() == title for r in refs):
            reasons.append("title matches entity reference")
        matched_title = set(self._tokens(title)) & query_tokens
        if matched_title:
            reasons.append("title matches query terms")
        for tag in obj.get("tags", []) or []:
            if set(self._tokens(str(tag))) & query_tokens:
                reasons.append("tag matches query")
                break
        if _is_active(obj):
            reasons.append("active/current state")
        if not reasons:
            reasons.append("text or metadata match")
        return f"Included because: {', '.join(reasons)}."

    def get_object(self, obj_id: str) -> dict | None:
        return self.objects.get(obj_id)


def build_retriever(demo_only: bool = False) -> UniversalRetriever:
    """Build a retriever using ethan-life and demo fixtures."""
    script_dir = Path(__file__).resolve().parent
    roots = []
    if not demo_only:
        life_root = script_dir.parent.parent.parent / "ethan-life" / "domains"
        roots.append(life_root)
    demo_root = script_dir.parent.parent / "config" / "demo-personality" / "fixtures" / "domains"
    roots.append(demo_root)
    return UniversalRetriever([r for r in roots if r.exists()])

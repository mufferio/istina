"""
File-based repository implementation (CLI v0 persistence).

Purpose:
- Persist Articles/BiasScores/Conflicts on disk for CLI usage.
- Simple storage format: JSON (single file) or JSONL (append-only logs).

Suggested layout:
- data/articles.jsonl
- data/bias_scores.jsonl
- data/conflicts.jsonl

Responsibilities:
- Serialize entities -> dict -> JSON lines
- Load entities on startup (or lazily)
- Ensure safe writes (atomic replace or append-only + rebuild index)

Important:
- Keep storage format versionable (include schema_version field if needed).
- Avoid mixing domain logic here; only persistence.
"""

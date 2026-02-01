"""
In-memory repository implementation.

Purpose:
- Fast, dependency-free storage for:
  - unit tests
  - local prototyping
- Acts as the reference implementation for repository behavior.

Implementation notes:
- Use dicts keyed by id: articles[id] = Article, scores[article_id] = BiasScore
- Provide simple filtering (by source/date) if needed by services.
- Deterministic behavior for tests (no randomness, stable ordering).
"""

"""
Repository interfaces (abstract base classes / protocols).

Defines:
- The contract for storing and retrieving entities like Article, Conflict, BiasScore.

Typical methods:
- add_article(article), get_article(id), list_articles(...)
- upsert_bias_score(score), get_bias_score(article_id)
- add_conflict(conflict), get_conflict(id), list_conflicts()
- optional: search/filter by source/date/conflict_id

Rules:
- No file/network logic here.
- Keep methods small and use-case driven.
- Return domain entities, not raw dicts.
"""

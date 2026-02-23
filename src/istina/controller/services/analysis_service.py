"""
AnalysisService (use case).

Workflow:
1) Select which Articles to analyze (unscored or filtered by params).
2) For each Article:
   - Run ScoringVisitor/Provider to produce BiasScore
   - Persist BiasScore via repository
3) Return summary stats + failures.

Reliability:
- Uses retry + rate limiting around provider calls.
- Handles provider failures gracefully (log and continue or stop based on config).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from istina.model.entities.article import Article
from istina.model.repositories.base_repository import BaseRepository


@dataclass(frozen=True)
class SelectionParams:
    limit: Optional[int] = None  # Max number of articles to analyze
    source: Optional[str] = None  # Filter by article source
    since: Optional[datetime] = None  # Filter articles published since this date


class AnalysisService:
    """
    Use-case service: decide which Articles should be analyzed next.

    Selection rules (Issue 5.3):
    - Only return articles that do NOT have a BiasScore yet.
    - Support optional limit.
    - Support optional source and since filters (delegated to repo.list_articles).
    """

    def __init__(self, repo: BaseRepository):
        self.repo = repo

    def select_unscored(self, params: Optional[SelectionParams] = None) -> List[Article]:
        """
        Select Articles that have no BiasScore yet.

        Implementation strategy:
        - Ask repo for articles (optionally filtered by source/since).
        - Filter out any article that already has a BiasScore in repo.
        - Apply limit after filtering so the count reflects truly unscored articles.

        Returns:
            list[Article]
        """
        if params is None:
            params = SelectionParams()

        # Pull a candidate set without a limit — we apply limit ourselves
        # after filtering so that "limit=N" means "N unscored articles", not
        # "check the first N articles for a score".
        candidates = self.repo.list_articles(
            source=params.source,
            since=params.since,
            limit=None,
        )

        unscored: List[Article] = []
        for a in candidates:
            if params.limit is not None and len(unscored) >= params.limit:
                break

            if self.repo.get_bias_score(a.id) is None:
                unscored.append(a)

        return unscored

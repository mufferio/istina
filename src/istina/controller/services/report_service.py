"""
ReportService (use case).

Workflow:
1) Load Articles + BiasScores (by filters).
2) Convert them into view-ready structures.
3) Delegate formatting to view renderers.

Output modes:
- summary: short stats
- full: per-article detailed report

Testing:
- Use snapshot tests for stable formatting output.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from istina.model.repositories.base_repository import BaseRepository
from istina.model.entities.article import Article
from istina.model.entities.bias_score import BiasScore


@dataclass
class SummaryReport:
    total_articles: int
    analyzed_count: int
    counts_by_source: Dict[str, int] = field(default_factory=dict)
    counts_by_overall_label: Dict[str, int] = field(default_factory=dict)


class ReportService:
    """
    Use-case service: produce summarized reporting stats for CLI views.

    Works with BaseRepository so it doesn't depend on storage details.
    """
    def __init__(self, repo: BaseRepository) -> None:
        self._repo = repo

    def get_summary(
        self,
        include_by_source: bool = True,
        include_by_overall_label: bool = True,
        limit: Optional[int] = None,
        source: Optional[str] = None,
        since: Optional[object] = None,  # keep loose: repo decides type (likely datetime)
    ) -> SummaryReport:
        """
        Summarize repo state.

        Args:
            include_by_source: if True, include counts grouped by Article.source
            include_by_overall_label: if True, include counts grouped by BiasScore.overall label
            limit/source/since: optional filters passed to repo.list_articles if supported

        Returns:
            SummaryReport
        """
        articles: List[Article] = self._repo.list_articles(limit=limit, source=source, since=since)
        total = len(articles)

        counts_by_source: Dict[str, int] = {}
        counts_by_label: Dict[str, int] = {}

        analyzed = 0

        for a in articles:
            if include_by_source:
                counts_by_source[a.source] = counts_by_source.get(a.source, 0) + 1

            score: Optional[BiasScore] = self._repo.get_bias_score(a.id)
            if score is not None:
                analyzed += 1
                if include_by_overall_label:
                    label = score.overall_bias_label
                    counts_by_label[label] = counts_by_label.get(label, 0) + 1

        return SummaryReport(
            total_articles=total,
            analyzed_count=analyzed,
            counts_by_source=counts_by_source if include_by_source else {},
            counts_by_overall_label=counts_by_label if include_by_overall_label else {},
        )
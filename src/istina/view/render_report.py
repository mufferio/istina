"""
CLI report renderer.

Purpose:
- Produce detailed, readable reports:
  - per-article bias breakdown
  - extracted claims with verdicts
  - rhetorical flags

Design:
- Pure functions: render_report(pairs) -> str
- Keep formatting stable for snapshot testing.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from istina.model.entities.article import Article
from istina.model.entities.bias_score import BiasScore

_DIVIDER = "-" * 60


def render_report(pairs: List[Tuple[Article, Optional[BiasScore]]]) -> str:
    """
    Render a detailed per-article report.

    Args:
        pairs: List of (Article, BiasScore | None) from ReportService.get_full_report()

    Returns:
        A multi-line formatted string ready to print to the terminal.

    Example output::

        === Istina Full Report (2 articles) ===

        ------------------------------------------------------------
        [1] Scientists discover new energy source
            URL    : https://example.com/energy
            Source : Science Daily
            Date   : 2026-01-10T09:00:00Z
            Bias   : center  (confidence: 0.82)
            Flags  : none
            Claims :
              • Mock claim derived from abc12345 — true

        ------------------------------------------------------------
        [2] Breaking news story (NOT ANALYZED)
            URL    : https://example.com/breaking
            Source : Wire
            Date   : 2026-01-11
    """
    if not pairs:
        return "No articles found."

    lines: list[str] = []
    lines.append(f"=== Istina Full Report ({len(pairs)} article{'s' if len(pairs) != 1 else ''}) ===")

    for idx, (article, score) in enumerate(pairs, start=1):
        lines.append("")
        lines.append(_DIVIDER)
        lines.append(f"[{idx}] {article.title}")
        lines.append(f"    URL    : {article.url}")
        lines.append(f"    Source : {article.source}")
        lines.append(f"    Date   : {article.published_at or 'unknown'}")

        if score is None:
            lines.append("    Bias   : NOT ANALYZED")
        else:
            lines.append(f"    Bias   : {score.overall_bias_label:<8} (confidence: {score.confidence:.2f})")

            flags = ", ".join(score.rhetorical_bias) if score.rhetorical_bias else "none"
            lines.append(f"    Flags  : {flags}")

            if score.claim_checks:
                lines.append("    Claims :")
                for claim in score.claim_checks:
                    text = claim.get("claim", "?")
                    verdict = claim.get("verdict", "?")
                    lines.append(f"      \u2022 {text} \u2014 {verdict}")
            else:
                lines.append("    Claims : none")

    return "\n".join(lines)

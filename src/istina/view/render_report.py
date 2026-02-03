"""
CLI report renderer.

Purpose:
- Produce detailed, readable reports:
  - per-article bias breakdown
  - extracted claims with verdicts + citations
  - rhetorical flags and examples

Design:
- Prefer pure functions: render_report(article, bias_score) -> str
- Keep formatting stable for snapshot testing.
"""

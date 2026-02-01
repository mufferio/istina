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

"""
SummarizeCommand.

Purpose:
- Implement: "istina summarize [--report full|summary] [--article-id ...]"
- Calls ReportService to:
  - load Articles + BiasScores
  - produce summary or detailed report text via view renderers

Output:
- Printed report text (or returned string) for CLI.
"""

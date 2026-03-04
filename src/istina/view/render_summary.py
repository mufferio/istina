"""
CLI summary renderer.

Purpose:
- Produce concise terminal output:
  - number of articles ingested
  - how many analyzed
  - top sources
  - quick bias distribution overview

Input:
- SummaryReport DTO from ReportService

Output:
- Formatted string (print-ready text block).
"""

from __future__ import annotations

from istina.controller.services.report_service import SummaryReport


def render_summary(report: SummaryReport) -> str:
    """
    Render a concise summary of repo state.

    Args:
        report: SummaryReport produced by ReportService.get_summary()

    Returns:
        A multi-line formatted string ready to print to the terminal.

    Example output::

        === Istina Summary ===
        Articles : 42
        Analyzed : 17 / 42

        Bias distribution:
          center  : 10
          left    :  4
          right    :  3

        By source:
          BBC News  : 20
          CNN       : 22
    """
    lines: list[str] = []
    lines.append("=== Istina Summary ===")
    lines.append(f"Articles : {report.total_articles}")
    lines.append(f"Analyzed : {report.analyzed_count} / {report.total_articles}")

    if report.counts_by_overall_label:
        lines.append("")
        lines.append("Bias distribution:")
        for label, count in sorted(report.counts_by_overall_label.items()):
            lines.append(f"  {label:<8}: {count}")

    if report.counts_by_source:
        lines.append("")
        lines.append("By source:")
        for source, count in sorted(report.counts_by_source.items()):
            lines.append(f"  {source:<20}: {count}")

    return "\n".join(lines)

## Goal
CLI command that prints summary or detailed report

## Tasks
- [ ] create src/controller/commands/summarize.py
- [ ] parse report mode (summary/full) and optional article_id
- [ ] call ReportService to get required data
- [ ] call view renderers to format output
- [ ] print or return formatted string

## Verify
Summarize prints correct counts and includes article titles/labels when available

## Done when
User can see CLI output for summary and full report

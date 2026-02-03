"""
CLI commands package.

Purpose:
- Each command encapsulates one user action in the CLI.
- Command pattern makes it easy to:
  - add new commands
  - test commands independently
  - later reuse commands as API endpoint handlers

Commands:
- ingest: fetch RSS -> store articles
- analyze: run provider -> store BiasScore
- summarize: render output to terminal
"""

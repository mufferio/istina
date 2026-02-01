"""
Istina CLI v0 entry point.

Responsibilities:
- Bootstrap the application from environment/config:
  - Load settings (src/config/settings.py)
  - Configure logging (src/utils/logger.py)
  - Construct dependencies (Repository, Provider, Services)
  - Wire up the CLI controller + commands
- Parse CLI arguments and dispatch to the appropriate Command.

How it evolves:
- v0: argparse-based CLI that supports commands like:
  - ingest (fetch RSS -> store Articles)
  - analyze (run bias/fact-check provider -> store results)
  - summarize (render a report)
- v1+: main becomes a thin wrapper around an app container/factory,
  reused by web API and later mobile backends.

Key invariants:
- No domain logic in main.py.
- All “real work” happens in services and providers.
"""

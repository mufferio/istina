"""
CLIController.

Purpose:
- Central dispatcher for CLI commands.
- Maps parsed CLI args -> Command objects -> execute()

Responsibilities:
- Register available commands (ingest, analyze, summarize)
- Provide shared dependencies (services, settings, logger)
- Execute commands and handle errors consistently (utils/error_handling.py)

Future:
- This controller maps 1:1 to an API controller in v1 (web).
"""

"""
Logging configuration.

Purpose:
- Configure Python logging consistently across the project:
  - format (timestamps, level, module)
  - handlers (stdout for CLI)
  - log levels controlled by Settings

Rules:
- Never log secrets (API keys).
- Keep output readable for CLI usage.
"""

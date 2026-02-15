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

import logging
from istina.config.settings import Settings

def configure_logger(settings: Settings):
    """
    Configure the root logger with a consistent format and level.
    Safe to call multiple times (won't duplicate handlers).
    """
    logger = logging.getLogger()
    if not getattr(logger, '_istina_configured', False):
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.handlers.clear()  # Remove any existing handlers
        logger.addHandler(handler)
        logger._istina_configured = True
    logger.setLevel(settings.log_level.upper())

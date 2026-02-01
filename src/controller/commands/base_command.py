"""
BaseCommand interface.

Purpose:
- Standardize how commands are executed.

Typical contract:
- execute() -> result (or None)
- accepts dependencies via constructor:
  - services
  - settings
  - output/renderers

Error handling:
- Commands should raise domain/app exceptions;
  controller handles final printing/logging.
"""

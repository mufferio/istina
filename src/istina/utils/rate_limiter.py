"""
Rate limiting helper.

Purpose:
- Enforce request-per-minute (or similar) limits for external APIs.
- Prevent accidental quota exhaustion and reduce 429 errors.

Used by:
- gemini_provider.py (and any future providers)
"""

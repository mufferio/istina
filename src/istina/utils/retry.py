"""
Retry helper.

Purpose:
- Provide a reusable retry mechanism for flaky operations:
  - network fetches (RSS)
  - provider calls (Gemini)
- Supports:
  - max attempts
  - exponential backoff
  - retryable exception types

Used by:
- rss_adapter.py
- gemini_provider.py
- analysis_service.py
"""

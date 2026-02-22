"""
RSS Adapter.

Purpose:
- Fetch and parse RSS feeds into Article entities.

Responsibilities:
- Accept feed URLs (single or list)
- Fetch content (requests/httpx)
- Parse RSS (feedparser)
- Map feed entries -> Article
- Handle errors:
  - unreachable feeds
  - malformed entries
  - missing fields

Output:
- List[Article] ready to be stored by repositories.

Future:
- Add caching, ETags, incremental fetching, more sources (APIs).
"""
from __future__ import annotations

import requests

from istina.model.adapters.adapter_error import AdapterError
from istina.utils.retry import retry

DEFAULT_TIMEOUT = 10  # seconds

def fetch_feed(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    Fetch RSS XML reliably from a feed URL.

    Requirements (Issue 4.2):
    - Uses HTTP via requests
    - Uses a timeout (default 10s)
    - Non-200 responses raise AdapterError
    - Integrates retry() for transient network failures (timeouts / connection errors)

    Returns:
        Response text (RSS XML) as a non-empty string.

    Raises:
        AdapterError: on non-200 responses, empty body, or any final failure after retries.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("url must be a non-empty string")
    
    url = url.strip()

    def _do_request() -> str:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code != 200:
            raise AdapterError(f"Failed to fetch feed: {url} (status code: {resp.status_code})")
        
        text = resp.text or ""
        if not text.strip():
            raise AdapterError(f"Empty response body for feed: {url}")
        
        return text
    
    try:
        return retry(
            _do_request,
            exceptions=(requests.RequestException, AdapterError),
            max_attempts=3,
            base_delay=0.0,
            backoff_factor=2.0,
        )
    except AdapterError:
        raise
    except Exception as e:
        raise AdapterError(f"Failed to fetch feed after retries: {url} (error: {e})") from e
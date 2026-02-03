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

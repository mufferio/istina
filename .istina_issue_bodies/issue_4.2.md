## Goal
Fetch RSS XML reliably from a feed URL

## Tasks
- [ ] create src/model/adapters/rss_adapter.py (if not already)
- [ ] implement fetch_feed(url) using requests/httpx
- [ ] add timeout (e.g., 10s)
- [ ] handle non-200 responses with AdapterError
- [ ] integrate retry() for transient network failures

## Verify
Calling fetch_feed(valid_rss_url) returns non-empty response text

## Done when
RSS feed fetching is reliable and errors are handled cleanly

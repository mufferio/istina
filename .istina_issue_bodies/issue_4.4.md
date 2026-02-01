## Goal
Fetch from multiple RSS URLs and return combined Articles

## Tasks
- [ ] implement fetch_articles(urls: list[str]) -> list[Article]
- [ ] for each URL: fetch_feed -> feedparser -> parse_entries
- [ ] continue on per-feed failure (collect/log error; do not crash whole ingest)
- [ ] optionally return or expose per-feed errors (v0 can log)

## Verify
With 2 feeds (1 valid, 1 invalid), function returns articles from valid feed and logs an error for invalid one

## Done when
Ingestion can tolerate flaky feeds without failing everything

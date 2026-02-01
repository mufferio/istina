"""
IngestService (use case).

Workflow:
1) Accept feed URLs.
2) Use RSSAdapter to fetch/parse -> List[Article].
3) Store articles via repository (dedupe by id).
4) Return ingestion result (counts, new vs existing).

Notes:
- Keep deduplication logic here (or in repo) but make it consistent.
- Should be easy to test with MemoryRepository + mocked RSSAdapter.
"""

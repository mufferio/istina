"""
IngestCommand.

Purpose:
- Implement: "istina ingest --feeds <...>"
- Calls IngestService to:
  - fetch RSS entries (via rss_adapter)
  - normalize into Articles
  - store them via repository

Output:
- Returns ingested count + list of new Article ids (optional)
- View layer can render summary of ingestion results
"""

## Goal
Create a use-case service that ingests RSS feeds into the repository

## Tasks
- [ ] create src/controller/services/ingest_service.py
- [ ] constructor accepts repo + rss_adapter
- [ ] implement ingest(feeds: list[str]) returning:
  - [ ] fetched_count
  - [ ] new_count
  - [ ] existing_count
  - [ ] errors (optional list)

## Verify
With a fake adapter that returns 3 Articles, repo receives them and counts match

## Done when
IngestService can be called by CLI command to ingest articles

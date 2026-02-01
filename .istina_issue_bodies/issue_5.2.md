## Goal
Prove ingest logic works without network

## Tasks
- [ ] create tests/test_services/test_ingest_service.py
- [ ] fake adapter returns known Articles
- [ ] assert repo counts new vs existing
- [ ] test dedupe behavior through service

## Verify
pytest -q passes for ingest service tests

## Done when
Ingest workflow is correct and stable

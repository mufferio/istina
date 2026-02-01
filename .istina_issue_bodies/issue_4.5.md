## Goal
Test RSS adapter without relying on live network

## Tasks
- [ ] create tests/test_adapters/test_rss_adapter.py
- [ ] mock HTTP response for fetch_feed()
- [ ] ensure parse_entries creates Articles with required fields
- [ ] test missing fields do not crash

## Verify
pytest -q passes for adapter tests

## Done when
RSS adapter behavior is validated offline and deterministic

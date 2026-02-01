## Goal
Prove repository behavior is correct and stable

## Tasks
- [ ] create tests/test_repositories/test_memory_repository.py (or similar)
- [ ] test add_articles() new vs existing counts
- [ ] test dedupe: inserting same id does not duplicate
- [ ] test get_article() returns correct item
- [ ] test upsert/get bias score behavior
- [ ] test list_articles() ordering is deterministic

## Verify
pytest -q passes for repository test suite

## Done when
Repository layer is trustworthy for services

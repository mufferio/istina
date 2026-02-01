## Goal
Prove file persistence works deterministically

## Tasks
- [ ] create tests/test_repositories/test_file_repository.py
- [ ] write articles + scores into a temp dir
- [ ] re-instantiate repository and verify data loaded
- [ ] verify latest-write-wins for upsert behavior

## Verify
pytest -q passes file repository tests

## Done when
File persistence is validated by automated tests

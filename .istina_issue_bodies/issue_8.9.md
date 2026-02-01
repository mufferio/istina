## Goal
End-to-end confidence that CLI wiring works

## Tasks
- [ ] create tests/test_controller/test_cli.py
- [ ] use MemoryRepository + MockProvider
- [ ] simulate running commands (call controller methods directly)
- [ ] assert stored articles and scores exist
- [ ] assert summarize output contains expected text

## Verify
pytest -q passes integration tests

## Done when
CLI workflow is verified end-to-end offline

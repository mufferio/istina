## Goal
Ensure MockProvider is stable and deterministic

## Tasks
- [ ] create tests/test_providers/test_mock_provider.py
- [ ] test determinism (same article => same output)
- [ ] test output structure fields exist
- [ ] test claim_checks list structure is consistent

## Verify
pytest -q passes for mock provider tests

## Done when
MockProvider is safe as default dev provider

## Goal
Prove analysis flow works without external APIs

## Tasks
- [ ] create tests/test_services/test_analysis_service.py
- [ ] seed repo with articles + some existing scores
- [ ] run analysis with MockProvider
- [ ] assert new BiasScores were inserted for unscored articles
- [ ] assert stats match expected

## Verify
pytest -q passes for analysis service tests

## Done when
Analysis service is correct, deterministic, and safe

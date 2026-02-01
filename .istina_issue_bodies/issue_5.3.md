## Goal
Select which Articles should be analyzed (unscored) with optional filters

## Tasks
- [ ] create src/controller/services/analysis_service.py
- [ ] implement selection logic:
  - [ ] only articles with no BiasScore yet
  - [ ] optional limit
  - [ ] optional source filter (if repo supports)
  - [ ] optional since date filter (if repo supports)

## Verify
Given 5 articles with 2 scored, selection returns the other 3

## Done when
Service can consistently identify what needs analysis

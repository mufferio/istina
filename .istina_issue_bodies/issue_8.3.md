## Goal
CLI command that analyzes unscored articles and stores BiasScores

## Tasks
- [ ] create src/controller/commands/analyze.py
- [ ] parse optional filters (limit/source/since)
- [ ] call AnalysisService.analyze(...)
- [ ] return analysis stats for rendering

## Verify
With MockProvider, running analyze produces BiasScores for unscored articles

## Done when
Analyze is callable from CLI with deterministic results

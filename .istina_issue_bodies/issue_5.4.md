## Goal
Analyze selected articles and persist BiasScores

## Tasks
- [ ] implement analyze(...) method that:
  - [ ] loops selected articles
  - [ ] calls provider.analyze_article(article) (or visitor later)
  - [ ] repo.upsert_bias_score(score)
  - [ ] collects stats (analyzed/skipped/failed)
- [ ] handle provider errors gracefully (record failure, continue)

## Verify
Using MockProvider, analyzed_count equals number of unscored articles

## Done when
Analysis results are stored and retrievable from the repository

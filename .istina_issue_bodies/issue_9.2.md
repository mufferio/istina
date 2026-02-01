## Goal
Persist Articles and BiasScores to disk

## Tasks
- [ ] create src/model/repositories/file_repository.py
- [ ] implement add_articles() appending to articles.jsonl
- [ ] implement upsert_bias_score() appending to bias_scores.jsonl
- [ ] ensure directory exists (create if missing)
- [ ] ensure writes are safe (flush + newline)

## Verify
After writing, files exist and contain valid JSON lines

## Done when
Data is written to disk reliably for both entity types

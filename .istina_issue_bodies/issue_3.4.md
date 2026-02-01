## Goal
Store and retrieve BiasScore objects (analysis results) in memory

## Tasks
- [ ] add internal storage (dict keyed by article_id)
- [ ] implement upsert_bias_score()
- [ ] implement get_bias_score()
- [ ] ensure upsert overwrites older score for same article_id (latest wins)

## Verify
Upsert a BiasScore then get_bias_score(article_id) returns it; upsert again replaces it

## Done when
BiasScores can be persisted and updated in memory deterministically

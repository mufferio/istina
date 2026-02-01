## Goal
Load persisted data on startup and serve queries efficiently

## Tasks
- [ ] on init, read JSONL files line-by-line
- [ ] rebuild indexes:
  - [ ] articles_by_id
  - [ ] scores_by_article_id (latest wins)
- [ ] implement get/list methods using indexes
- [ ] handle missing files gracefully (treat as empty)

## Verify
Restart app and previously written Articles/BiasScores are available

## Done when
FileRepository supports read operations correctly across restarts

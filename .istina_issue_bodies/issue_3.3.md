## Goal
Prevent duplicate Articles from being stored (by id)

## Tasks
- [ ] in add_articles(), skip insert if article.id already exists
- [ ] return (new_count, existing_count) accurately
- [ ] decide overwrite policy (recommended v0: do NOT overwrite existing Article)

## Verify
Adding the same Article twice returns (1 new, 1 existing) and storage count remains 1

## Done when
Duplicate inserts do not create duplicates and counts are correct

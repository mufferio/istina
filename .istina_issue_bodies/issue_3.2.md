## Goal
Store and retrieve Article objects in memory for fast dev/testing

## Tasks
- [ ] create src/model/repositories/memory_repository.py
- [ ] implement internal storage (dict keyed by article_id)
- [ ] implement add_articles()
- [ ] implement get_article()
- [ ] implement list_articles() with deterministic ordering (choose one: insertion order or published_at desc)

## Verify
Manually insert 2 Articles then list_articles() returns them in expected order

## Done when
Articles can be added, retrieved, and listed reliably in memory

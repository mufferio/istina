## Goal
Define a persistence contract that services can depend on (independent of storage type)

## Tasks
- [ ] create src/model/repositories/base_repository.py
- [ ] define method signatures for:
  - [ ] add_articles(articles) -> (new_count, existing_count)
  - [ ] get_article(article_id) -> Article | None
  - [ ] list_articles(limit=None, source=None, since=None) -> list[Article]
  - [ ] upsert_bias_score(score) -> None
  - [ ] get_bias_score(article_id) -> BiasScore | None
- [ ] ensure docstrings explain expected behavior (dedupe, ordering, filtering)

## Verify
MemoryRepository can implement all methods without ambiguity

## Done when
Services can be written against BaseRepository without knowing storage details

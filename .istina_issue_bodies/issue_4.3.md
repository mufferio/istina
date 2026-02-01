## Goal
Convert RSS feed entries into Article entities safely

## Tasks
- [ ] parse XML using feedparser
- [ ] map each entry to Article fields (title/url/source/published_at/summary)
- [ ] handle missing optional fields gracefully
- [ ] ensure compute_id() is used consistently
- [ ] avoid crashing on one bad entry (skip + log)

## Verify
Parsing a real feed produces a non-empty list[Article] with valid ids

## Done when
RSS parsing yields valid domain Articles consistently

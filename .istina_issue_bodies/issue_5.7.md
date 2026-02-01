## Goal
Provide detailed report data for CLI full report rendering

## Tasks
- [ ] implement get_full_report(limit=None, article_id=None, source=None)
- [ ] return list of (Article, BiasScore|None) pairs (BiasScore may be None if not analyzed)
- [ ] ensure deterministic ordering

## Verify
Requesting a specific article_id returns exactly one pair for that article

## Done when
CLI can request detailed report data reliably

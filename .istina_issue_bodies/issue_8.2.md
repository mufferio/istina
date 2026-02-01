## Goal
CLI command that ingests RSS feeds into repository

## Tasks
- [ ] create src/controller/commands/ingest.py
- [ ] parse feeds args passed by controller
- [ ] call IngestService.ingest(feeds)
- [ ] return a result suitable for rendering/logging

## Verify
Calling IngestCommand.execute() stores articles in MemoryRepository using a real feed (or fake adapter in test)

## Done when
Ingest is callable from CLI layer via command abstraction

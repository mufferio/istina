## Goal
Protect against future format changes

## Tasks
- [ ] include schema_version in each written record
- [ ] validate schema_version on load
- [ ] if mismatch: raise RepositoryError with helpful message (or implement migration later)

## Verify
Manually alter schema_version in a line and confirm load fails with clear error

## Done when
Format changes won’t silently corrupt data interpretation

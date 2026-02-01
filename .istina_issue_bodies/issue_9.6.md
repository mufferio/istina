## Goal
Confirm real user workflow persists across runs

## Tasks
- [ ] set ISTINA_REPO_TYPE=file
- [ ] run ingest on a real RSS feed
- [ ] run analyze with MockProvider
- [ ] run summarize
- [ ] stop program
- [ ] rerun summarize and confirm same results appear

## Verify
Second summarize run shows previously stored data without re-ingesting

## Done when
Persistence works in real CLI usage end-to-end

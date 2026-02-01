## Goal
Prove parsing and normalization works without live API calls

## Tasks
- [ ] create tests/test_providers/test_gemini.py
- [ ] feed several mocked response variants:
  - [ ] well-formed JSON
  - [ ] missing fields
  - [ ] malformed JSON-like text
- [ ] assert BiasScore still valid + safe fallbacks

## Verify
pytest -q passes for gemini parsing tests

## Done when
You trust the parser before spending API quota

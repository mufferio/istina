## Goal
Provide offline, deterministic analysis for dev/testing

## Tasks
- [ ] create src/model/providers/mock_provider.py
- [ ] implement analyze_article(article) returning BiasScore
- [ ] make outputs deterministic based on article.id
- [ ] include simple rhetorical flags (keyword heuristic)
- [ ] include stub claim_checks structure

## Verify
Same Article analyzed twice returns identical BiasScore fields

## Done when
You can run analysis end-to-end without network/API keys

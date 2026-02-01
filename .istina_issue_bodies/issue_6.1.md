## Goal
Standardize analysis provider API so it’s swappable later

## Tasks
- [ ] create src/model/providers/base_provider.py
- [ ] define BaseProvider with analyze_article(article) -> BiasScore
- [ ] document expected normalization requirements (BiasScore is provider-agnostic)

## Verify
MockProvider can implement BaseProvider without ambiguity

## Done when
Services depend on provider interface, not concrete vendor code

## Goal
Use visitor pattern in the analysis pipeline (clean separation)

## Tasks
- [ ] update AnalysisService to accept a visitor (or build it internally from provider)
- [ ] replace provider.analyze_article calls with visitor.visit(article)
- [ ] keep stats/error handling unchanged

## Verify
All AnalysisService tests still pass unchanged (or with minimal adjustments)

## Done when
Analysis pipeline uses visitor cleanly and remains testable

## Goal
Render detailed per-article report output

## Tasks
- [ ] create src/view/render_report.py
- [ ] implement render_report(article, bias_score) -> str
- [ ] show title/source/url
- [ ] show overall label + rhetorical flags
- [ ] show claim_checks with verdict + citations (if present)
- [ ] handle missing BiasScore gracefully

## Verify
Given fixed Article/BiasScore, output includes expected sections

## Done when
Full report is readable and stable for tests

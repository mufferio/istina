## Goal
Provide summarized reporting data for CLI views

## Tasks
- [ ] create src/controller/services/report_service.py
- [ ] implement get_summary(...) returning:
  - [ ] total articles
  - [ ] analyzed count
  - [ ] counts by source (optional)
  - [ ] counts by overall_label (optional)

## Verify
With known test data, summary numbers match exactly

## Done when
View layer can render a summary from ReportService output

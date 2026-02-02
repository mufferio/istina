#!/usr/bin/env bash
set -euo pipefail

# Creates Istina issues (3.1 -> 9.6) with:
# - Exact markdown body format (Goal / Tasks / Verify / Done when)
# - Automatic labels
# - Title format: "Issue X.X - <name>"

TMP_DIR=".istina_issue_bodies"
mkdir -p "$TMP_DIR"

create_issue () {
  local num="$1"
  local title="$2"
  local labels="$3"
  local file="$TMP_DIR/issue_${num}.md"

  # Body comes from stdin
  cat > "$file"

  gh issue create \
    -t "Issue ${num} - ${title}" \
    -F "$file" \
    -l "$labels"
}

########################################
# PHASE 3 — Repository Layer
########################################

create_issue "3.1" "Define BaseRepository interface" "phase:3-repository,type:feature" <<'MD'
## Goal
Define a persistence contract that services can depend on (independent of storage type)

## Tasks
- [ ] create src/model/repositories/base_repository.py
- [ ] define method signatures for:
  - [ ] add_articles(articles) -> (new_count, existing_count)
  - [ ] get_article(article_id) -> Article | None
  - [ ] list_articles(limit=None, source=None, since=None) -> list[Article]
  - [ ] upsert_bias_score(score) -> None
  - [ ] get_bias_score(article_id) -> BiasScore | None
- [ ] ensure docstrings explain expected behavior (dedupe, ordering, filtering)

## Verify
MemoryRepository can implement all methods without ambiguity

## Done when
Services can be written against BaseRepository without knowing storage details
MD

create_issue "3.2" "Implement MemoryRepository article storage" "phase:3-repository,type:feature" <<'MD'
## Goal
Store and retrieve Article objects in memory for fast dev/testing

## Tasks
- [ ] create src/model/repositories/memory_repository.py
- [ ] implement internal storage (dict keyed by article_id)
- [ ] implement add_articles()
- [ ] implement get_article()
- [ ] implement list_articles() with deterministic ordering (choose one: insertion order or published_at desc)

## Verify
Manually insert 2 Articles then list_articles() returns them in expected order

## Done when
Articles can be added, retrieved, and listed reliably in memory
MD

create_issue "3.3" "Implement MemoryRepository dedupe behavior" "phase:3-repository,type:feature" <<'MD'
## Goal
Prevent duplicate Articles from being stored (by id)

## Tasks
- [ ] in add_articles(), skip insert if article.id already exists
- [ ] return (new_count, existing_count) accurately
- [ ] decide overwrite policy (recommended v0: do NOT overwrite existing Article)

## Verify
Adding the same Article twice returns (1 new, 1 existing) and storage count remains 1

## Done when
Duplicate inserts do not create duplicates and counts are correct
MD

create_issue "3.4" "Implement MemoryRepository BiasScore storage" "phase:3-repository,type:feature" <<'MD'
## Goal
Store and retrieve BiasScore objects (analysis results) in memory

## Tasks
- [ ] add internal storage (dict keyed by article_id)
- [ ] implement upsert_bias_score()
- [ ] implement get_bias_score()
- [ ] ensure upsert overwrites older score for same article_id (latest wins)

## Verify
Upsert a BiasScore then get_bias_score(article_id) returns it; upsert again replaces it

## Done when
BiasScores can be persisted and updated in memory deterministically
MD

create_issue "3.5" "Repository unit tests (MemoryRepository)" "phase:3-repository,type:test" <<'MD'
## Goal
Prove repository behavior is correct and stable

## Tasks
- [ ] create tests/test_repositories/test_memory_repository.py (or similar)
- [ ] test add_articles() new vs existing counts
- [ ] test dedupe: inserting same id does not duplicate
- [ ] test get_article() returns correct item
- [ ] test upsert/get bias score behavior
- [ ] test list_articles() ordering is deterministic

## Verify
pytest -q passes for repository test suite

## Done when
Repository layer is trustworthy for services
MD

########################################
# PHASE 4 — RSS Adapter + Retry
########################################

create_issue "4.1" "Implement retry helper (exponential backoff)" "phase:4-adapter,type:feature" <<'MD'
## Goal
Provide a reusable retry utility for flaky network/provider calls

## Tasks
- [ ] create src/utils/retry.py
- [ ] implement retry(fn, exceptions, max_attempts, base_delay, backoff_factor)
- [ ] ensure it re-raises after final failure
- [ ] add docstring with example usage

## Verify
A test function that fails twice then succeeds returns successfully

## Done when
Retry can be used by RSS adapter and providers safely
MD

create_issue "4.2" "RSSAdapter: fetch_feed(url) with HTTP + timeouts" "phase:4-adapter,type:feature" <<'MD'
## Goal
Fetch RSS XML reliably from a feed URL

## Tasks
- [ ] create src/model/adapters/rss_adapter.py (if not already)
- [ ] implement fetch_feed(url) using requests/httpx
- [ ] add timeout (e.g., 10s)
- [ ] handle non-200 responses with AdapterError
- [ ] integrate retry() for transient network failures

## Verify
Calling fetch_feed(valid_rss_url) returns non-empty response text

## Done when
RSS feed fetching is reliable and errors are handled cleanly
MD

create_issue "4.3" "RSSAdapter: parse_entries(parsed) -> list[Article]" "phase:4-adapter,type:feature" <<'MD'
## Goal
Convert RSS feed entries into Article entities safely

## Tasks
- [ ] parse XML using feedparser
- [ ] map each entry to Article fields (title/url/source/published_at/summary)
- [ ] handle missing optional fields gracefully
- [ ] ensure compute_id() is used consistently
- [ ] avoid crashing on one bad entry (skip + log)

## Verify
Parsing a real feed produces a non-empty list[Article] with valid ids

## Done when
RSS parsing yields valid domain Articles consistently
MD

create_issue "4.4" "RSSAdapter: fetch_articles(urls) aggregates and continues on partial failures" "phase:4-adapter,type:feature" <<'MD'
## Goal
Fetch from multiple RSS URLs and return combined Articles

## Tasks
- [ ] implement fetch_articles(urls: list[str]) -> list[Article]
- [ ] for each URL: fetch_feed -> feedparser -> parse_entries
- [ ] continue on per-feed failure (collect/log error; do not crash whole ingest)
- [ ] optionally return or expose per-feed errors (v0 can log)

## Verify
With 2 feeds (1 valid, 1 invalid), function returns articles from valid feed and logs an error for invalid one

## Done when
Ingestion can tolerate flaky feeds without failing everything
MD

create_issue "4.5" "RSSAdapter unit tests (mock HTTP)" "phase:4-adapter,type:test" <<'MD'
## Goal
Test RSS adapter without relying on live network

## Tasks
- [ ] create tests/test_adapters/test_rss_adapter.py
- [ ] mock HTTP response for fetch_feed()
- [ ] ensure parse_entries creates Articles with required fields
- [ ] test missing fields do not crash

## Verify
pytest -q passes for adapter tests

## Done when
RSS adapter behavior is validated offline and deterministic
MD

create_issue "4.6" "RSSAdapter manual smoke test (real feed)" "phase:4-adapter,type:docs" <<'MD'
## Goal
Prove RSS adapter works against at least one real-world feed

## Tasks
- [ ] pick 1-2 RSS URLs (document them in README or a dev note)
- [ ] run a small script/snippet to fetch and print 3 titles
- [ ] confirm published_at parsing isn’t breaking

## Verify
Manual run prints real article titles and URLs

## Done when
You’ve confirmed real network + parsing works end-to-end
MD

########################################
# PHASE 5 — Services
########################################

create_issue "5.1" "IngestService: implement ingest(feeds) -> result" "phase:5-services,type:feature" <<'MD'
## Goal
Create a use-case service that ingests RSS feeds into the repository

## Tasks
- [ ] create src/controller/services/ingest_service.py
- [ ] constructor accepts repo + rss_adapter
- [ ] implement ingest(feeds: list[str]) returning:
  - [ ] fetched_count
  - [ ] new_count
  - [ ] existing_count
  - [ ] errors (optional list)

## Verify
With a fake adapter that returns 3 Articles, repo receives them and counts match

## Done when
IngestService can be called by CLI command to ingest articles
MD

create_issue "5.2" "IngestService unit tests (fake adapter + MemoryRepository)" "phase:5-services,type:test" <<'MD'
## Goal
Prove ingest logic works without network

## Tasks
- [ ] create tests/test_services/test_ingest_service.py
- [ ] fake adapter returns known Articles
- [ ] assert repo counts new vs existing
- [ ] test dedupe behavior through service

## Verify
pytest -q passes for ingest service tests

## Done when
Ingest workflow is correct and stable
MD

create_issue "5.3" "AnalysisService: select unscored articles (filtering/limit)" "phase:5-services,type:feature" <<'MD'
## Goal
Select which Articles should be analyzed (unscored) with optional filters

## Tasks
- [ ] create src/controller/services/analysis_service.py
- [ ] implement selection logic:
  - [ ] only articles with no BiasScore yet
  - [ ] optional limit
  - [ ] optional source filter (if repo supports)
  - [ ] optional since date filter (if repo supports)

## Verify
Given 5 articles with 2 scored, selection returns the other 3

## Done when
Service can consistently identify what needs analysis
MD

create_issue "5.4" "AnalysisService: run provider/visitor and persist BiasScores" "phase:5-services,type:feature" <<'MD'
## Goal
Analyze selected articles and persist BiasScores

## Tasks
- [ ] implement analyze(...) method that:
  - [ ] loops selected articles
  - [ ] calls provider.analyze_article(article) (or visitor later)
  - [ ] repo.upsert_bias_score(score)
  - [ ] collects stats (analyzed/skipped/failed)
- [ ] handle provider errors gracefully (record failure, continue)

## Verify
Using MockProvider, analyzed_count equals number of unscored articles

## Done when
Analysis results are stored and retrievable from the repository
MD

create_issue "5.5" "AnalysisService unit tests (MockProvider + MemoryRepository)" "phase:5-services,type:test" <<'MD'
## Goal
Prove analysis flow works without external APIs

## Tasks
- [ ] create tests/test_services/test_analysis_service.py
- [ ] seed repo with articles + some existing scores
- [ ] run analysis with MockProvider
- [ ] assert new BiasScores were inserted for unscored articles
- [ ] assert stats match expected

## Verify
pytest -q passes for analysis service tests

## Done when
Analysis service is correct, deterministic, and safe
MD

create_issue "5.6" "ReportService: summary stats output" "phase:5-services,type:feature" <<'MD'
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
MD

create_issue "5.7" "ReportService: full report pairs (Article + BiasScore)" "phase:5-services,type:feature" <<'MD'
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
MD

create_issue "5.8" "ReportService unit tests" "phase:5-services,type:test" <<'MD'
## Goal
Prove reporting logic is correct and stable

## Tasks
- [ ] create tests/test_services/test_report_service.py
- [ ] test summary totals
- [ ] test full report pair structure
- [ ] test filters (limit/article_id/source) if implemented

## Verify
pytest -q passes for report service tests

## Done when
ReportService is reliable for CLI output
MD

########################################
# PHASE 6 — Providers
########################################

create_issue "6.1" "Define BaseProvider interface" "phase:6-provider,type:feature" <<'MD'
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
MD

create_issue "6.2" "Implement MockProvider deterministic analysis" "phase:6-provider,type:feature" <<'MD'
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
MD

create_issue "6.3" "MockProvider unit tests" "phase:6-provider,type:test" <<'MD'
## Goal
Ensure MockProvider is stable and deterministic

## Tasks
- [ ] create tests/test_providers/test_mock_provider.py
- [ ] test determinism (same article => same output)
- [ ] test output structure fields exist
- [ ] test claim_checks list structure is consistent

## Verify
pytest -q passes for mock provider tests

## Done when
MockProvider is safe as default dev provider
MD

create_issue "6.4" "ProviderFactory selects provider from Settings" "phase:6-provider,type:feature" <<'MD'
## Goal
Instantiate the correct provider based on configuration

## Tasks
- [ ] create src/model/providers/provider_factory.py
- [ ] implement create_provider(settings) -> BaseProvider
- [ ] support: mock, gemini
- [ ] invalid provider raises ConfigError

## Verify
Switch ISTINA_PROVIDER=mock uses MockProvider instance

## Done when
Provider can be swapped by env change only
MD

create_issue "6.5" "Implement RateLimiter utility (RPM)" "phase:6-provider,type:feature" <<'MD'
## Goal
Prevent accidental quota exhaustion for real providers

## Tasks
- [ ] create src/utils/rate_limiter.py
- [ ] implement a simple RPM limiter (sleep when exceeding)
- [ ] ensure it is injectable/optional (MockProvider doesn’t need it)
- [ ] add basic tests if feasible

## Verify
A loop of N calls respects configured rate limit

## Done when
Provider calls can be throttled consistently
MD

create_issue "6.6" "GeminiProvider: scaffold client + prompt templates" "phase:6-provider,type:feature" <<'MD'
## Goal
Create the structure for Gemini integration without relying on perfect parsing yet

## Tasks
- [ ] create src/model/providers/gemini_provider.py
- [ ] read GEMINI_API_KEY from Settings
- [ ] define prompt templates for:
  - [ ] bias detection + rhetorical flags
  - [ ] claim extraction + verdict scaffolding
- [ ] implement a call wrapper function (no parsing perfection required yet)
- [ ] ensure secrets never logged

## Verify
Provider can be instantiated when API key exists (without crashing)

## Done when
GeminiProvider skeleton is ready for parsing + normalization
MD

create_issue "6.7" "GeminiProvider: parse/normalize response -> BiasScore" "phase:6-provider,type:feature" <<'MD'
## Goal
Convert Gemini output into your normalized BiasScore schema

## Tasks
- [ ] implement robust parsing logic
- [ ] handle invalid JSON or missing fields safely
- [ ] fill BiasScore fields consistently
- [ ] fallback: “insufficient evidence” for broken claim checks

## Verify
Given a mocked Gemini response, parser returns a valid BiasScore

## Done when
GeminiProvider returns normalized, safe BiasScores reliably
MD

create_issue "6.8" "GeminiProvider parsing unit tests (mocked responses)" "phase:6-provider,type:test" <<'MD'
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
MD

create_issue "6.9" "GeminiProvider live call smoke test (gated)" "phase:6-provider,type:docs" <<'MD'
## Goal
Confirm Gemini integration works end-to-end with a real API call

## Tasks
- [ ] add a dev-only CLI snippet or manual script to analyze 1 article
- [ ] enforce rate limiting + retry around call
- [ ] confirm returned BiasScore stores successfully in repo
- [ ] document steps in README (dev section)

## Verify
One real analysis run completes and produces a stored BiasScore

## Done when
Real provider can be used safely for CLI v0
MD

########################################
# PHASE 7 — Visitor Pattern
########################################

create_issue "7.1" "Create ArticleVisitor interface" "phase:7-visitor,type:feature" <<'MD'
## Goal
Introduce a visitor contract for operations over Articles

## Tasks
- [ ] create src/model/visitors/article_visitor.py
- [ ] define visit(article) method signature
- [ ] document intended usage (apply operations without bloating entities)

## Verify
ScoringVisitor can implement ArticleVisitor cleanly

## Done when
Visitor base is in place for scoring and future operations
MD

create_issue "7.2" "Implement ScoringVisitor wrapping provider" "phase:7-visitor,type:feature" <<'MD'
## Goal
Encapsulate scoring operation as a visitor

## Tasks
- [ ] create src/model/visitors/scoring_visitor.py
- [ ] constructor takes BaseProvider
- [ ] visit(article) returns BiasScore by calling provider

## Verify
Visiting an Article returns same BiasScore as provider directly

## Done when
Scoring can be treated as a modular operation
MD

create_issue "7.3" "Refactor AnalysisService to use ScoringVisitor" "phase:7-visitor,type:refactor" <<'MD'
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
MD

create_issue "7.4" "Visitor unit tests" "phase:7-visitor,type:test" <<'MD'
## Goal
Ensure visitors behave deterministically and integrate cleanly

## Tasks
- [ ] create tests/test_visitors/test_scoring_visitor.py
- [ ] test visit returns BiasScore
- [ ] test determinism with MockProvider

## Verify
pytest -q passes visitor tests

## Done when
Visitor layer is validated and safe
MD

########################################
# PHASE 8 — CLI + View
########################################

create_issue "8.1" "Define BaseCommand interface" "phase:8-cli,type:feature" <<'MD'
## Goal
Standardize CLI commands using Command pattern

## Tasks
- [ ] create src/controller/commands/base_command.py
- [ ] define execute() contract
- [ ] decide what commands return (string, result object, etc.) and document it

## Verify
IngestCommand can subclass BaseCommand cleanly

## Done when
Command interface exists and is consistent
MD

create_issue "8.2" "Implement IngestCommand" "phase:8-cli,type:feature" <<'MD'
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
MD

create_issue "8.3" "Implement AnalyzeCommand" "phase:8-cli,type:feature" <<'MD'
## Goal
CLI command that analyzes unscored articles and stores BiasScores

## Tasks
- [ ] create src/controller/commands/analyze.py
- [ ] parse optional filters (limit/source/since)
- [ ] call AnalysisService.analyze(...)
- [ ] return analysis stats for rendering

## Verify
With MockProvider, running analyze produces BiasScores for unscored articles

## Done when
Analyze is callable from CLI with deterministic results
MD

create_issue "8.4" "Implement SummarizeCommand" "phase:8-cli,type:feature" <<'MD'
## Goal
CLI command that prints summary or detailed report

## Tasks
- [ ] create src/controller/commands/summarize.py
- [ ] parse report mode (summary/full) and optional article_id
- [ ] call ReportService to get required data
- [ ] call view renderers to format output
- [ ] print or return formatted string

## Verify
Summarize prints correct counts and includes article titles/labels when available

## Done when
User can see CLI output for summary and full report
MD

create_issue "8.5" "Implement CLIController with argparse dispatch" "phase:8-cli,type:feature" <<'MD'
## Goal
Single entrypoint that routes subcommands to Command objects

## Tasks
- [ ] create src/controller/cli_controller.py
- [ ] build argparse parser with subcommands:
  - [ ] ingest --feeds <n+>
  - [ ] analyze --limit/--source/--since
  - [ ] summarize --report summary|full --article-id
- [ ] instantiate correct Command and call execute()
- [ ] handle exceptions using error formatter

## Verify
python main.py --help and python main.py ingest --help work correctly

## Done when
CLI routes input to the correct command cleanly
MD

create_issue "8.6" "Implement render_summary view" "phase:8-cli,type:feature" <<'MD'
## Goal
Render a concise CLI summary output

## Tasks
- [ ] create src/view/render_summary.py
- [ ] implement a pure function render_summary(summary_data) -> str
- [ ] include totals, analyzed count, and label distribution if available

## Verify
Given fixed input dict, output string matches expected structure

## Done when
Summary rendering is stable and snapshot-testable
MD

create_issue "8.7" "Implement render_report view (full report)" "phase:8-cli,type:feature" <<'MD'
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
MD

create_issue "8.8" "CLI error handling + friendly messages" "phase:8-cli,type:feature" <<'MD'
## Goal
Ensure CLI prints readable errors and exits with correct codes

## Tasks
- [ ] centralize exception handling in controller or main.py
- [ ] use format_exception(e) for user output
- [ ] optionally support debug mode for stack traces
- [ ] ensure non-zero exit codes on failure

## Verify
Trigger ConfigError and ensure CLI prints friendly message (no stack trace in normal mode)

## Done when
CLI failure modes are predictable and user-friendly
MD

create_issue "8.9" "CLI integration tests (ingest → analyze → summarize)" "phase:8-cli,type:test" <<'MD'
## Goal
End-to-end confidence that CLI wiring works

## Tasks
- [ ] create tests/test_controller/test_cli.py
- [ ] use MemoryRepository + MockProvider
- [ ] simulate running commands (call controller methods directly)
- [ ] assert stored articles and scores exist
- [ ] assert summarize output contains expected text

## Verify
pytest -q passes integration tests

## Done when
CLI workflow is verified end-to-end offline
MD

########################################
# PHASE 9 — File Persistence
########################################

create_issue "9.1" "Define file storage format (JSONL) for entities" "phase:9-persistence,type:feature" <<'MD'
## Goal
Decide a stable file persistence format for CLI v0

## Tasks
- [ ] decide files: data/articles.jsonl and data/bias_scores.jsonl
- [ ] define record schema fields (include schema_version)
- [ ] define “latest write wins” policy for updates
- [ ] document format in README or code docstring

## Verify
You can write one sample record and read it back manually

## Done when
Storage format is defined and documented clearly
MD

create_issue "9.2" "Implement FileRepository write operations (append JSONL)" "phase:9-persistence,type:feature" <<'MD'
## Goal
Persist Articles and BiasScores to disk

## Tasks
- [ ] create src/model/repositories/file_repository.py
- [ ] implement add_articles() appending to articles.jsonl
- [ ] implement upsert_bias_score() appending to bias_scores.jsonl
- [ ] ensure directory exists (create if missing)
- [ ] ensure writes are safe (flush + newline)

## Verify
After writing, files exist and contain valid JSON lines

## Done when
Data is written to disk reliably for both entity types
MD

create_issue "9.3" "Implement FileRepository load + index rebuild" "phase:9-persistence,type:feature" <<'MD'
## Goal
Load persisted data on startup and serve queries efficiently

## Tasks
- [ ] on init, read JSONL files line-by-line
- [ ] rebuild indexes:
  - [ ] articles_by_id
  - [ ] scores_by_article_id (latest wins)
- [ ] implement get/list methods using indexes
- [ ] handle missing files gracefully (treat as empty)

## Verify
Restart app and previously written Articles/BiasScores are available

## Done when
FileRepository supports read operations correctly across restarts
MD

create_issue "9.4" "Add schema version safety in FileRepository" "phase:9-persistence,type:feature" <<'MD'
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
MD

create_issue "9.5" "FileRepository unit tests (temp directory)" "phase:9-persistence,type:test" <<'MD'
## Goal
Prove file persistence works deterministically

## Tasks
- [ ] create tests/test_repositories/test_file_repository.py
- [ ] write articles + scores into a temp dir
- [ ] re-instantiate repository and verify data loaded
- [ ] verify latest-write-wins for upsert behavior

## Verify
pytest -q passes file repository tests

## Done when
File persistence is validated by automated tests
MD

create_issue "9.6" "Manual persistence acceptance test (restart workflow)" "phase:9-persistence,type:docs" <<'MD'
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
MD

echo "✅ Done. Created issue bodies in $TMP_DIR and attempted to create all issues via gh."
echo "If any issue creation failed, gh would have printed the error above."

# Istina

## License

This project is not open source.  
The code is publicly visible for transparency and learning purposes only.  
All rights reserved.



**Conflict-tracking and bias-aware news aggregator.**

Istina is a CLI-first prototype that ingests news articles, analyzes them for bias using external AI services (e.g. Google Gemini), and surfaces conflicting narratives across sources. Built with a clean Model-View-Controller (MVC) architecture and extensible design patterns (Command, Factory, Visitor), Istina is designed to grow into a full web + mobile platform.

## 🚀 Features

- 📰 Ingest articles from RSS feeds or files
- 🤖 Analyze articles using AI-based bias detection
- ⚖️ Track conflicting narratives across multiple sources
- 📊 Summarize or export bias/conflict reports
- 🧩 Swappable AI provider integration via factory pattern
- 💻 CLI-first design, built for eventual web + mobile expansion

## 🧱 Architecture

- **Model Layer:** Core domain objects (`Article`, `Conflict`, etc.)
- **Command Pattern:** CLI commands for ingesting, analyzing, summarizing
- **Factory Pattern:** AI provider selection (`Gemini`, `OpenAI`, `Mock`)
- **Visitor Pattern:** Traverse articles/conflicts to apply scoring/export logic
- **Repository Pattern:** Pluggable persistence (in-memory or file/DB)

## 🧪 Gemini Live Smoke Tests (Optional)

Istina includes gated live integration tests that call the real Google Gemini API
to verify end-to-end analysis (provider → parsing → repository storage).

These tests are **optional** and skipped automatically unless an API key is set.

👉 **Before running live tests, please check `docs/GEMINI_LIVE_TESTS.md` for full setup instructions.**

Example run:

```bash
pytest tests/test_providers/test_gemini_live_smoke.py -v
```

## 🔌 RSS Feeds (Issue 4 — smoke-tested 2026-02-22)

The following real-world feeds are used as reference fixtures for integration
smoke tests (`scripts/smoke_test_rss.py`):

| Outlet | RSS URL |
|---|---|
| BBC News | `http://feeds.bbci.co.uk/news/rss.xml` |
| Al Jazeera | `https://www.aljazeera.com/xml/rss/all.xml` |

Both feeds were confirmed to:
- Return HTTP 200 with non-empty XML
- Parse to `Article` objects with correct `title`, `url`, and `source` fields
- Produce valid ISO-8601 UTC `published_at` strings (`YYYY-MM-DDTHH:MM:SSZ`)

Run the smoke test manually at any time:

```bash
python3 scripts/smoke_test_rss.py
```

## �️ Storage Format (CLI v0)

Istina persists data as **newline-delimited JSON** (JSONL) in the `data/` directory.
Each line is one self-contained JSON object — never pretty-printed.

### Files

| File | Contents |
|---|---|
| `data/articles.jsonl` | One `Article` record per line |
| `data/bias_scores.jsonl` | One `BiasScore` record per line |

### Article record (`schema_version = 1`)

```json
{
  "schema_version":  1,
  "id":              "a3f8c2d...",
  "title":           "Gaza ceasefire talks resume in Cairo",
  "url":             "https://bbc.co.uk/news/world-middle-east-123456",
  "source":          "BBC News",
  "published_at":    "2026-03-04T12:00:00Z",
  "summary":         "Negotiators from both sides ..."
}
```

Nullable fields: `published_at`, `summary` may be `null`.

### BiasScore record (`schema_version = 1`)

```json
{
  "schema_version":      1,
  "article_id":          "a3f8c2d...",
  "provider":            "gemini",
  "overall_bias_label":  "center",
  "rhetorical_bias":     ["loaded_language"],
  "claim_checks": [
    {
      "claim_text": "The ceasefire was unconditional.",
      "verdict":    "contradicted",
      "evidence":   ["https://reuters.com/..."]
    }
  ],
  "confidence":    0.87,
  "timestamp":     "2026-03-04T14:05:00",
  "raw_response":  null
}
```

Nullable field: `raw_response` may be `null`.

### Update policies

| Entity | Policy |
|---|---|
| `Article` | **First write wins** — once an `id` is stored it is never overwritten. |
| `BiasScore` | **Latest write wins** — a new record for the same `(article_id, provider)` pair is appended; on load only the *last* occurrence is kept. Call `FileRepository.compact()` to collapse superseded lines. |

### Atomicity

Full-file rewrites (e.g. `compact()`) write to a temp file in the same directory
then use `os.replace()` so a crash mid-write never leaves a half-written file.

### Implementation

See [`src/istina/model/repositories/file_repository.py`](src/istina/model/repositories/file_repository.py)
for the full `FileRepository` implementation.  Smoke test: [`tests/test_file_repository_roundtrip.py`](tests/test_file_repository_roundtrip.py).

## ⚡ Quick Start

```bash
# 1. clone
git clone https://github.com/mufferio/istina.git
cd istina

# 2. create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. install dependencies and the package in editable mode
pip install -r requirements.txt
pip install -e .

# 4. run a full pipeline with the built-in mock provider (no API key needed)
python main.py ingest --feeds "http://feeds.bbci.co.uk/news/rss.xml"
python main.py analyze --limit 5
python main.py summarize
```

## 📦 Requirements

| Requirement | Version |
|---|---|
| Python | ≥ 3.11 |
| pip dependencies | `requirements.txt` |

## ⚙️ Configuration

All settings are controlled by **environment variables** (or a `.env` file in the project root).

| Variable | Default | Description |
|---|---|---|
| `ISTINA_REPO_TYPE` | `memory` | `file` — persist to disk; `memory` — in-process only |
| `ISTINA_DATA_DIR` | `./data` | Directory for JSONL storage files (used when `ISTINA_REPO_TYPE=file`) |
| `ISTINA_PROVIDER` | `mock` | AI provider: `mock`, `gemini` |
| `ISTINA_ENV` | `dev` | Runtime environment: `dev`, `test`, `prod` |
| `ISTINA_LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `ISTINA_RATE_LIMIT_RPM` | `60` | Max provider calls per minute |
| `ISTINA_GEMINI_API_KEY` | *(empty)* | Required only when `ISTINA_PROVIDER=gemini` |
| `ISTINA_GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model name |

Create a `.env` file in the project root to persist settings across sessions:

```dotenv
ISTINA_REPO_TYPE=file
ISTINA_PROVIDER=mock
ISTINA_DATA_DIR=./data
ISTINA_LOG_LEVEL=INFO
```

## 🖥️ CLI Commands

All commands are run via `python main.py <command> [options]`.

### `ingest` — fetch RSS feeds and store articles

```bash
python main.py ingest --feeds <URL> [<URL> ...]

# Examples
python main.py ingest --feeds "http://feeds.bbci.co.uk/news/rss.xml"
python main.py ingest --feeds "http://feeds.bbci.co.uk/news/rss.xml" \
                              "https://www.aljazeera.com/xml/rss/all.xml"
```

### `analyze` — run bias analysis on stored articles

```bash
python main.py analyze [--limit N] [--source SOURCE] [--since ISO_DATE]

# Examples
python main.py analyze                        # analyze all unscored articles
python main.py analyze --limit 10             # cap at 10 articles
python main.py analyze --source "BBC News"    # only articles from BBC News
python main.py analyze --since 2026-03-01     # only articles published after this date
```

### `summarize` — print a bias report

```bash
python main.py summarize [--report summary|full] [--source SOURCE] [--limit N] [--article-id ID]

# Examples
python main.py summarize                          # default summary view
python main.py summarize --report full            # per-article detail
python main.py summarize --report full --limit 5  # top 5 articles in full detail
```

### Global flags

| Flag | Effect |
|---|---|
| `--debug` | Print full stack traces instead of friendly error messages |
| `-h` / `--help` | Show usage for any command |

## 🧪 Running Tests

```bash
# run the full test suite
pytest

# run with verbose output
pytest -v

# run a specific test file
pytest tests/test_repositories/test_file_repository.py -v

# run only fast tests (skip live API tests)
pytest --ignore=tests/test_providers/test_gemini_live_smoke.py
```

The suite covers unit tests, integration tests, and round-trip persistence tests.
Live Gemini API tests are automatically skipped unless `ISTINA_GEMINI_API_KEY` is set —
see [`docs/GEMINI_LIVE_TESTS.md`](docs/GEMINI_LIVE_TESTS.md) for details.

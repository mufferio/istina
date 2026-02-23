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

## 📦 Installation

- *Coming soon ;)*

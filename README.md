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

## 📦 Installation

- *Coming soon ;)*

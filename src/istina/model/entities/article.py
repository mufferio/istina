"""
Article entity.

Represents:
- A single news item (from RSS or other sources).

Typical fields:
- id: stable unique id (hash of url/title+source+published_at)
- title, url, source, published_at
- author (optional), summary/description (optional)
- content_text (optional; may be fetched later)
- conflict_id (optional; later: clustering/assignment)
- bias_score (optional; later: attached analysis result)
- raw: original feed payload for debugging/auditing (optional)

Rules/validation:
- url and title should not be empty.
- published_at should be timezone-aware or consistently naive (pick one).
- Provide helper methods for stable id computation and serialization.

Used by:
- adapters/rss_adapter.py to create Article objects from feeds
- repositories to store/load Articles
- visitors to run analysis operations over Articles
"""

# v0.62.10 — Global Search Arc Episode Support

## Status

Planning

## Objective

Extend global search so arc-name searches can surface the episodes and chapter metadata associated with matching arcs.

The implementation must preserve:

- Thin frontend architecture
- Python-owned business logic
- Existing `/search` compatibility
- Certified v0.62.9 arc aggregation behavior
- Anime-scoped data separation
- Support for anime-only, manga-only, and shared arcs

## Evidence Questions

1. What does the current `/search` endpoint return?
2. Which repository owns global-search behavior?
3. Are episode arc names already searchable?
4. Are manga arc names already searchable?
5. Are matching episodes returned directly or nested under chapter results?
6. Can the existing response schema be extended compatibly?
7. Should arc results be a new response collection?
8. Can v0.62.9 arc-summary logic be reused without duplication?
9. How should anime-only arcs appear?
10. How should manga-only arcs appear?
11. How should shared anime/manga arcs avoid duplicate results?
12. What should the frontend display for an arc search result?

## Initial Constraints

- Do not normalize arc labels in React.
- Do not duplicate repository aggregation logic.
- Do not break existing title, episode-number, chapter-number, or chapter-title search.
- Do not add a new endpoint unless the current `/search` contract cannot be extended safely.
- Preserve exact episode and manga arc labels for downstream filtering.
- Validate with both One Piece and Naruto.

## Current Certified Baseline

- Backend tests: 245 passed
- Frontend lint: 0 errors
- Frontend production build: successful

## Planning Outcome

Pending runtime inspection and architecture review.

## Planning Conclusion

The existing global-search contract can support arc episode searching without adding a new endpoint or top-level response category.

The `/search` endpoint already returns separate episode and chapter metadata collections.

Chapter metadata search already supports manga arc labels through `ChapterMetadata.manga_arc`.

Episode search currently supports episode titles and episode numbers but does not search `Episode.arc`.

## Recommended Direction

Option B — Extend the existing episode search behavior.

Add `Episode.arc` to the filters used by `EpisodeRepository.search_episodes()`.

This mirrors the already-certified chapter metadata behavior:

- Anime arc matches return existing episode results.
- Manga arc matches return existing chapter metadata results.
- Shared arcs return both categories.
- Anime-only arcs return episodes and no chapter metadata.
- Manga-only arcs return chapter metadata and no episodes.
- Existing `/search` response fields remain unchanged.

A new arc-specific endpoint or explicit arc-result collection is not required for v0.62.10.

## Implementation Scope

Backend:

- Extend `EpisodeRepository.search_episodes()` to search episode arc labels.
- Preserve episode-title and numeric episode searches.
- Preserve deterministic anime and episode ordering.
- Preserve null-label behavior.

API:

- Keep the existing `/search` route and `SearchResponse` schema unchanged.
- Add compatibility coverage for shared, anime-only, and manga-only arc searches.

Frontend:

- No new API client function is required.
- No new result component is required.
- Existing episode results already display the episode arc.
- Existing chapter metadata results already display the manga arc.

## Validation Scope

Validate:

- One Piece shared arc search
- One Piece anime-only arc search
- Naruto shared arc search
- Naruto manga-only arc search
- Partial, case-insensitive matching
- Existing title search
- Existing numeric episode search
- Existing chapter-number search
- Existing response structure
- No duplicate episode results
- No unrelated null-arc episode matches

# v0.62.10 — Global Search Arc Episode Support

## Status

Implementation In Progress

## Backend Validation

Repository

- search_episodes() extended to include Episode.arc
- Existing ordering preserved
- Existing numeric search preserved

API

- Existing /search response contract preserved
- No schema changes
- No endpoint changes

Tests

- New Baratie shared-arc search: Passed
- New Egghead partial arc search: Passed
- New Naruto shared-arc search: Passed
- New anime-only arc search: Passed
- New manga-only arc regression: Passed

Search API

- test_search.py: 20 passed

Backend

- Full suite: 250 passed, 0 failed

Runtime

One Piece

- Shared arc search: Passed
- Partial arc search: Passed
- Anime-only arc search: Passed

Naruto

- Shared arc search: Passed
- Manga-only arc search: Passed

Regression

- Existing episode-title search: Passed
- Existing numeric search: Passed

Frontend

- Lint: 0 errors
- Production build: Successful

Backend

- Search API tests: 20 passed
- Full backend suite: 250 passed, 0 failed

## Certification

v0.62.10 — Global Search Arc Episode Support

Certified evidence

- Search API: 20 passed
- Backend suite: 250 passed, 0 failed
- Frontend lint: 0 errors
- Frontend production build: Successful
- Shared arc search validated
- Anime-only arc search validated
- Manga-only arc regression validated
- Existing title search preserved
- Existing numeric search preserved
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

Pending architecture decision after source inspection and runtime evidence collection.

## Recommended Direction

Pending.

## Implementation Scope

Pending.

## Validation Scope

Pending.
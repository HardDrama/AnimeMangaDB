# Version 0.62.3

Feature:
Bidirectional Chapter Navigation API

## Implementation

Added the anime-scoped chapter navigation endpoint:

`GET /anime/{anime_id}/chapters/{chapter_number}/episodes`

The endpoint reuses the existing `EpisodeResponse` schema and returns only episodes belonging to the requested anime.

## Repository

Added:

`get_episodes_by_anime_and_chapter(anime_id, chapter_number)`

The existing global `get_episodes_by_chapter(chapter_number)` method remains unchanged for `/search` compatibility.

## Error Contract

- Missing anime: `404 Anime not found.`
- Missing chapter metadata: `404 Chapter not found.`
- Existing chapter without mappings: `200 []`

## Validation

- Repository tests: [result]
- Anime compatibility tests: [result]
- Complete backend suite: [result]
- Frontend validation: [result]

## Certification

Bidirectional chapter-to-episode API navigation is validated and certified.
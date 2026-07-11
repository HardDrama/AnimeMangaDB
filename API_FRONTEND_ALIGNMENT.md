# API ↔ Frontend Alignment

## Existing Frontend Contract

GET /anime

GET /anime/{id}

GET /anime/{id}/episodes

GET /episodes/{id}

GET /episodes/{id}/chapters

GET /chapters/{chapter}/episodes

GET /search

---

## Current Scope v2 API

GET /health

GET /scope

GET /version

GET /series

GET /episodes

GET /episodes/count

GET /episodes/id/{id}

GET /episodes/{episode_number}

---

## Alignment Plan

Status

✔ System endpoints

✔ Episode endpoints

- [x] Episode detail by database ID

⬜ Anime endpoints

⬜ Chapter lookup

⬜ Reverse chapter lookup

- [x] Episodes adapting a chapter

⬜ Search

- [x] Global search

Goal

Restore the original frontend experience while preserving the Scope v2 backend architecture.

## Episode Route Semantics

- `GET /episodes/id/{episode_id}` retrieves an episode by database ID.
- `GET /episodes/{episode_number}` retrieves an episode by episode number.
- The frontend detail page uses the explicit database-ID route.

## Search Contract

`GET /search?query=...` returns:

- `anime`
- `episodes`
- `chapters`

Numeric queries may return chapter mappings in addition to matching anime and episode results.

## Numeric Search Semantics

Numeric global-search queries search both:

- Exact anime episode number
- Exact manga chapter number

Episode-title text matching remains active for numeric queries.

## Chapter Lookup Contract

`GET /chapters/{chapter_number}/episodes` returns every episode mapped to the requested manga chapter.

The response is a plain episode array for compatibility with the existing React Chapter Lookup component.

An unmapped chapter returns an empty array.

## API Base URL

The frontend reads the API base URL from:

`VITE_API_BASE_URL`

Local development defaults to:

`http://127.0.0.1:8000`

Example configuration is provided in:

`frontend/.env.example`
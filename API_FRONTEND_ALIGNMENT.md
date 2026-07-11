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

- [x] Global search

⬜ Anime endpoints

⬜ Chapter lookup

⬜ Reverse chapter lookup

⬜ Search

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
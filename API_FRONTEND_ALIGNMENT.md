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

⬜ Anime endpoints

⬜ Chapter lookup

⬜ Reverse chapter lookup

⬜ Search

Goal

Restore the original frontend experience while preserving the Scope v2 backend architecture.
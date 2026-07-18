# Version 0.62.9

Feature:
Series Arc Navigation

Status:
Planning In Progress

Purpose:

Introduce arc-level navigation for Anime Detail while preserving the certified REST architecture.

Feature Lifecycle

Build
→ Test
→ Document
→ Validate
→ Certify

## Backend Implementation

Added:

`GET /anime/{anime_id}/arcs`

The endpoint returns anime-scoped arc summaries with:

- Display name
- Exact episode arc label
- Exact manga arc label
- Episode count
- Chapter count

Arc aggregation is implemented in the Python repository layer.

Equivalent labels such as an anime arc name and a manga arc name ending in `Arc` are grouped into one response while their exact source labels remain available.

Blank and missing arc values are excluded.

## Backend Validation

Repository test file:

- 15 passed

Anime compatibility test file:

- 11 passed

Combined focused tests:

- 26 passed

OpenAPI registration:

- Passed

One Piece runtime endpoint:

- Passed
- Arc rows: [record actual number]
- Blank names: None
- Duplicate normalized names: None

Naruto runtime endpoint:

- Passed
- Arc rows: [record actual number]
- Blank names: None
- Duplicate normalized names: None

Missing-anime response:

- 404
- `{"detail":"Anime not found."}`

Full backend suite:

- [record exact result]
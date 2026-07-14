# Scope v3 API Specification

## Purpose

Expose certified Scope v3 chapter metadata through the REST API.

The API serves as the only data source for the frontend.

---

## Design Principles

- Thin frontend
- REST only
- JSON responses
- No duplicated business logic
- Backward compatible with Scope v2

---

## Supported Series

Initially:

- One Piece
- Naruto

Future:

- Additional certified Scope v3 datasets

---

## Chapter Metadata Fields

Each chapter exposes:

- chapter_number
- chapter_title
- manga_arc
- source_url
- last_updated

---

## Initial Endpoints

GET /anime/{id}/chapters

Returns:

- series information
- ordered chapter metadata

---

GET /anime/{id}/chapters/{chapter}

Returns:

Single chapter metadata.

---

Future Endpoints

- chapter search
- title search
- arc search

---

## Response Format

JSON

No HTML rendering.

---

## Compatibility

All existing Scope v2 endpoints remain unchanged.
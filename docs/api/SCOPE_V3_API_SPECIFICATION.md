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

---

## Chapter Metadata Response

Schema:

```json
{
  "chapter_number": 1,
  "chapter_title": "Romance Dawn",
  "manga_arc": "Romance Dawn Arc",
  "source_url": "https://onepiece.fandom.com/wiki/Chapter_1",
  "last_updated": "2026-07-14T12:30:00"
}
```

---

## Series Chapter List

### Endpoint

```http
GET /anime/{anime_id}/chapters
```

Returns every Scope v3 chapter metadata record for the requested anime.

### Response

```json
[
  {
    "chapter_number": 1,
    "chapter_title": "Romance Dawn",
    "manga_arc": "Romance Dawn Arc",
    "source_url": "https://onepiece.fandom.com/wiki/Chapter_1",
    "last_updated": "2026-07-14T12:30:00"
  }
]
```

### Ordering

Chapters are ordered numerically in ascending order.

### Empty Dataset

A valid anime with no chapter metadata returns:

```json
[]
```

### Missing Anime

An unknown anime ID returns:

```json
{
  "detail": "Anime not found."
}
```

with HTTP status `404`.

### Verified Null Metadata

Naruto Chapter 700 returns:

```json
"manga_arc": null
```

The API does not fabricate or replace verified non-applicable metadata.

### Compatibility

The endpoint follows the existing bare-list contract used by:

```http
GET /anime/{anime_id}/episodes
```

No existing Scope v2 route behavior changed.

---

## Individual Chapter Metadata

### Endpoint

```http
GET /anime/{anime_id}/chapters/{chapter_number}
```

Returns one Scope v3 chapter metadata record for the requested anime and chapter number.

### Successful Response

```json
{
  "chapter_number": 1,
  "chapter_title": "Romance Dawn",
  "manga_arc": "Romance Dawn Arc",
  "source_url": "https://onepiece.fandom.com/wiki/Chapter_1",
  "last_updated": "2026-07-14T12:30:00"
}
```

### Missing Anime

An unknown anime ID returns HTTP `404`:

```json
{
  "detail": "Anime not found."
}
```

### Missing Chapter

A chapter number that does not exist for a valid anime returns HTTP `404`:

```json
{
  "detail": "Chapter not found."
}
```

### Invalid Chapter Number

A non-integer chapter-number path value returns HTTP `422`.

### Nullable Manga Arc

Verified non-applicable manga arcs remain `null`.

Naruto Chapter 700 is the certified benchmark case.

### Contract Consistency

The individual response uses the same `ChapterMetadataResponse` schema as the series chapter-list endpoint.

---

## Chapter Metadata Search

### Endpoint

```http
GET /search?query={value}
```

The existing search endpoint includes a new response field:

```json
{
  "anime": [],
  "episodes": [],
  "chapters": [],
  "chapter_metadata": []
}
```

### Compatibility Fields

`chapters` retains the Scope v2 chapter-to-episode mapping contract.

`chapter_metadata` contains Scope v3 chapter metadata records.

### Supported Matches

Chapter metadata search matches:

- Chapter title
- Manga arc
- Exact numeric chapter number

Text matching is case-insensitive and partial.

Numeric chapter matching is exact.

### Response Item

Each `chapter_metadata` entry uses the shared chapter metadata response schema:

```json
{
  "chapter_number": 50,
  "chapter_title": "A Parting of Ways",
  "manga_arc": "Baratie Arc",
  "source_url": "https://...",
  "last_updated": "2026-07-14T12:30:00"
}
```

### Nullable Manga Arc

Verified non-applicable manga arcs remain `null`.

### Empty Result

When no Scope v3 chapter metadata matches:

```json
"chapter_metadata": []
```

Other search categories may still contain results.

---

## Certified One Piece API Contract

Certified dataset:

- Anime: One Piece
- Chapter range: 1–1188
- Chapter records: 1188

Validated endpoints:

- `GET /anime/{anime_id}/chapters`
- `GET /anime/{anime_id}/chapters/{chapter_number}`
- `GET /search?query={value}`

Validation result:

- Complete range returned: PASS
- Numerical ordering: PASS
- Required metadata completeness: PASS
- List/detail consistency: PASS
- Chapter-title search: PASS
- Manga-arc search: PASS
- Numeric chapter search: PASS
- Scope v2 compatibility: PASS

One Piece contains no approved null manga-arc exceptions in the certified range.

---

## Certified Naruto API Contract

Certified dataset:

- Anime: Naruto
- Chapter range: 1–700
- Chapter records: 700

Validated endpoints:

- `GET /anime/{anime_id}/chapters`
- `GET /anime/{anime_id}/chapters/{chapter_number}`
- `GET /search?query={value}`

Validation result:

- Complete range returned: PASS
- Numerical ordering: PASS
- Required metadata completeness: PASS
- List/detail consistency: PASS
- Chapter-title search: PASS
- Manga-arc search: PASS
- Numeric chapter search: PASS
- Spin-off exclusion: PASS
- Scope v2 compatibility: PASS

### Verified Exception

Naruto Chapter 700 is a standalone epilogue.

API response:

```json
{
  "chapter_number": 700,
  "manga_arc": null
}
```
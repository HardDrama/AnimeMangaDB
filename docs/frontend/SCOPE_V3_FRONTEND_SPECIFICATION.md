# Scope v3 Frontend Specification

## Purpose

Integrate certified Scope v3 chapter metadata into the AnimeMangaDB frontend.

The frontend consumes the REST API only.

No database access, scraping logic, metadata repair logic, or certification logic belongs in the frontend.

---

## Architecture

Frontend responsibilities:

- Request API data
- Display chapter metadata
- Handle loading states
- Handle empty states
- Handle errors
- Provide navigation
- Present nullable values clearly

Backend responsibilities:

- Data access
- Chapter ordering
- Search matching
- Metadata validation
- Scope v2 compatibility
- Certified dataset exposure

---

## Certified API Inputs

### Series Chapter List

`GET /anime/{anime_id}/chapters`

Returns an ordered list of chapter metadata.

### Chapter Detail

`GET /anime/{anime_id}/chapters/{chapter_number}`

Returns one anime-scoped chapter metadata record.

### Search

`GET /search?query={value}`

Scope v3 results are returned in:

`chapter_metadata`

The existing Scope v2 chapter-to-episode results remain in:

`chapters`

---

## Supported Series

Initial certified datasets:

- One Piece Chapters 1–1188
- Naruto Chapters 1–700

The frontend implementation must remain reusable for future certified series.

---

## Chapter Metadata Fields

- `chapter_number`
- `chapter_title`
- `manga_arc`
- `source_url`
- `last_updated`

---

## Nullable Manga Arc

`manga_arc` may be null.

Certified example:

- Naruto Chapter 700
- Standalone epilogue
- Manga arc not applicable

Frontend display:

`Not applicable`

The frontend must not fabricate or inherit an arc value.

---

## Series Chapter List

The anime or series view should support an ordered chapter list.

Each chapter entry should display:

- Chapter number
- Chapter title
- Manga arc
- Navigation to chapter detail

Optional secondary display:

- Last-updated timestamp
- External source link

The chapter list should support:

- Loading state
- Error state
- Empty state
- Responsive layout

---

## Chapter Detail

The chapter detail experience should display:

- Anime title
- Chapter number
- Chapter title
- Manga arc or `Not applicable`
- Canonical source link
- Last-updated timestamp
- Navigation back to the series chapter list

---

## Search Integration

Search results should keep separate sections for:

- Anime
- Episodes
- Episode adaptation chapter mappings
- Chapter metadata

Recommended labels:

- `Anime`
- `Episodes`
- `Episode Adaptation Matches`
- `Chapter Metadata`

The frontend must not merge Scope v2 chapter mappings with Scope v3 chapter metadata.

---

## Loading States

The frontend should show a visible loading state while requesting:

- Series chapter lists
- Chapter details
- Search results

---

## Error States

The frontend should handle:

- Network failure
- Anime not found
- Chapter not found
- Invalid chapter path
- Unexpected API response

Errors should be understandable to the user and should not expose raw stack traces.

---

## Empty States

A valid anime with no chapter metadata should display:

`No chapter metadata is currently available for this series.`

An empty chapter metadata search should not hide valid anime, episode, or adaptation-mapping results.

---

## Compatibility

Existing Scope v2 frontend behavior must remain available:

- Anime browsing
- Episode browsing
- Episode detail
- Episode-to-chapter mappings
- Existing search results

Scope v3 extends the frontend without replacing Scope v2 behavior.

---

## Accessibility

Required:

- Semantic headings
- Keyboard-accessible links and controls
- Descriptive link text
- Visible focus states
- Clear loading and error messages
- No information communicated by color alone

---

## Responsive Behavior

Required:

- Desktop
- Tablet
- Mobile

Chapter metadata must remain readable without horizontal overflow.

---

## Out of Scope

This release does not include:

- Editing chapter metadata
- Triggering ingestion
- Triggering audits
- Triggering certification
- Frontend database access
- New scraper behavior
- Volume metadata
- Release-date metadata
- Cover art

---

## Frontend API Client

The frontend API client remains implemented in JavaScript using native `fetch`.

API base URL:

`VITE_API_BASE_URL`

Fallback:

`http://127.0.0.1:8000`

### Chapter Metadata Contract

The client documents chapter metadata using a JSDoc contract:

- `chapter_number`: number
- `chapter_title`: string
- `manga_arc`: string or null
- `source_url`: string
- `last_updated`: ISO 8601 string

### Chapter List Request

Function:

`getChaptersForAnime(animeId)`

Endpoint:

`GET /anime/{anime_id}/chapters`

Return value:

Array of chapter metadata records.

### Chapter Detail Request

Function:

`getAnimeChapter(animeId, chapterNumber)`

Endpoint:

`GET /anime/{anime_id}/chapters/{chapter_number}`

Return value:

One chapter metadata record.

### Search Contract

`searchDatabase(query)` returns:

- `anime`
- `episodes`
- `chapters`
- `chapter_metadata`

The `chapters` field remains the Scope v2 episode-adaptation mapping result.

The `chapter_metadata` field contains Scope v3 chapter metadata.

### Error Handling

Chapter metadata requests follow the existing frontend client convention:

- non-successful HTTP responses throw an `Error`
- pages and components are responsible for displaying the error
- API response data is not transformed or repaired in the frontend
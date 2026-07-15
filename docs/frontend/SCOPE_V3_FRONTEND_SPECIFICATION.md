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

## Status

Implementation:

✅ Complete

Certified dataset validation:

- ✅ One Piece Chapters 1–1188
- ✅ Naruto Chapters 1–700

Final frontend validation:

⬜ Pending v0.60.9

Formal frontend certification:

⬜ Pending v0.60.10

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

---

## Series Chapter List Experience

The anime detail page loads certified chapter metadata from:

`GET /anime/{anime_id}/chapters`

The existing episode list remains visible.

### Displayed Chapter Fields

- Chapter number
- Chapter title
- Manga arc
- Canonical source link

### Local Filtering

Loaded chapter records may be filtered by:

- Chapter number
- Chapter title
- Manga arc

Filtering is local to the selected anime and does not replace global API search.

### Nullable Manga Arc

A null manga arc is displayed as:

`Not applicable`

The API value is not modified.

### States

Loading:

`Loading chapter metadata...`

Empty dataset:

`No chapter metadata is currently available for this series.`

No filter matches:

`No chapter metadata matches your search.`

Error:

The chapter section displays the existing client error message.

### Responsive Layout

Chapter metadata cards use a responsive grid and collapse to one column on narrow screens.

---

## Chapter Detail Experience

### Route

`/anime/:animeId/chapters/:chapterNumber`

### API Inputs

The page loads:

- `GET /anime/{anime_id}`
- `GET /anime/{anime_id}/chapters/{chapter_number}`

These requests run in parallel.

### Displayed Fields

- Anime title
- Chapter number
- Chapter title
- Manga arc
- Canonical source link
- Last-updated timestamp

### Nullable Manga Arc

A null manga arc is displayed as:

`Not applicable`

The underlying API value remains unchanged.

### Navigation

Chapter-list cards link to the chapter detail route.

The detail page includes:

- Breadcrumb navigation
- Back-to-anime navigation
- Canonical external source navigation

### Last-Updated Formatting

The ISO 8601 API timestamp is displayed using the browser’s local date and time format.

If the timestamp cannot be parsed, the original string is displayed.

### Error Behavior

Failed anime or chapter requests show the existing frontend client error message.

The page provides navigation back to the requested anime route.

### Responsive Behavior

Chapter metadata displays as:

- Two columns on larger screens
- One column on narrow screens

---

## Chapter Metadata Search Presentation

Global search displays separate result sections for:

- Anime
- Episodes
- Episode Adaptation Matches
- Chapter Metadata

`Episode Adaptation Matches` uses the existing Scope v2 `chapters` response field.

`Chapter Metadata` uses the Scope v3 `chapter_metadata` response field.

Chapter metadata search results display:

- Chapter number
- Chapter title
- Manga arc or `Not applicable`
- Canonical source link

### Current Search Identity Limitation

The certified Scope v3 chapter metadata response does not currently include:

- Anime ID
- Anime title

As a result, global chapter metadata search results cannot safely link to the anime-scoped chapter detail route.

The frontend must not infer series identity from source URLs, titles, or chapter numbers.

A future API enhancement should add series identity to chapter metadata search responses.

### Bidirectional Mapping Limitation

Chapter detail pages currently do not show adapted anime episodes.

The existing endpoint:

`GET /chapters/{chapter_number}/episodes`

is global and does not safely identify one anime series.

A future API enhancement should provide:

`GET /anime/{anime_id}/chapters/{chapter_number}/episodes`

The frontend should not perform cross-series filtering as presentation logic.

---

## Certified One Piece Frontend Contract

Certified dataset:

- One Piece Chapters 1–1188
- 1188 chapter metadata records

Validated experiences:

- Anime chapter list
- Local chapter filtering
- Chapter detail
- Chapter metadata search
- Canonical source navigation
- Responsive presentation
- Scope v2 compatibility

Validation result:

PASS

One Piece has no certified null manga-arc exceptions in the supported range.

---

## Implemented Experience

### Anime Detail

The anime detail page displays:

- Anime metadata
- Existing episode list
- Certified chapter metadata
- Local chapter filtering

Chapter filtering supports:

- Chapter number
- Chapter title
- Manga arc
- Case-insensitive partial matching

### Chapter Detail

Route:

`/anime/:animeId/chapters/:chapterNumber`

The detail page displays:

- Anime title
- Chapter number
- Chapter title
- Manga arc or `Not applicable`
- Canonical source link
- Last-updated timestamp
- Breadcrumb navigation
- Back-to-anime navigation

### Global Search

Global search contains separate sections for:

- Anime
- Episodes
- Episode Adaptation Matches
- Chapter Metadata

The Scope v2 `chapters` response remains distinct from the Scope v3 `chapter_metadata` response.

---

## Frontend API Functions

The frontend uses native `fetch` through:

`frontend/src/api/client.js`

### Anime and Episodes

- `getAnime()`
- `getAnimeById(animeId)`
- `getEpisodesForAnime(animeId)`
- `getEpisodeById(episodeId)`
- `getEpisodeChapters(episodeId)`
- `getEpisodesByChapter(chapterNumber)`

### Scope v3 Chapters

- `getChaptersForAnime(animeId)`
- `getAnimeChapter(animeId, chapterNumber)`

### Search

- `searchDatabase(query)`

The frontend consumes API field names without transforming them.

Chapter metadata fields:

- `chapter_number`
- `chapter_title`
- `manga_arc`
- `source_url`
- `last_updated`

---

## Nullable Manga Arc

The API may return:

```json
{
  "manga_arc": null
}
```

---

## Known API-Dependent Limitations

### Search Result Series Identity

Scope v3 `chapter_metadata` search results currently do not include:

- `anime_id`
- `anime_title`

Therefore global chapter metadata results cannot safely link to the anime-scoped chapter detail route.

The frontend does not infer series identity from:

- Chapter number
- Chapter title
- Manga arc
- Source URL

Recommended future API enhancement:

Include anime identity in chapter metadata search responses.

### Chapter-to-Episode Mapping

Chapter detail pages do not currently show adapted episodes.

The available endpoint:

`GET /chapters/{chapter_number}/episodes`

is global and can return results across series.

Recommended future API endpoint:

`GET /anime/{anime_id}/chapters/{chapter_number}/episodes`

The frontend must not implement cross-series filtering as presentation logic.

---

## Scope v2 Compatibility Matrix

| Existing Experience | Status |
|---|:---:|
| Anime browser | Preserved |
| Anime detail | Preserved |
| Episode browser | Preserved |
| Episode detail | Preserved |
| Episode-to-chapter mapping | Preserved |
| Chapter Lookup | Preserved |
| Anime search | Preserved |
| Episode search | Preserved |
| Episode Adaptation Matches | Preserved |

Scope v3 adds chapter metadata experiences without replacing existing Scope v2 functionality.

---

## Certified Dataset Validation

### One Piece

- Certified range: Chapters 1–1188
- Chapter-list display: PASS
- Local filtering: PASS
- Chapter-detail navigation: PASS
- Chapter metadata search: PASS
- Canonical source navigation: PASS
- Responsive behavior: PASS
- Accessibility review: PASS

### Naruto

- Certified range: Chapters 1–700
- Chapter-list display: PASS
- Local filtering: PASS
- Chapter-detail navigation: PASS
- Chapter metadata search: PASS
- Chapter 10 source isolation: PASS
- Chapter 700 `Not applicable` presentation: PASS
- Spin-off exclusion: PASS
- Responsive behavior: PASS
- Accessibility review: PASS

---

## Validation Commands

Backend regression:

```powershell
pytest
```

Frontend production build:

```powershell
Set-Location frontend
npm run build
Set-Location ..
```

Frontend lint:

```powershell
Set-Location frontend
npm run lint
Set-Location ..
```

Combined validation:

```powershell
pytest

Set-Location frontend
npm run build
npm run lint
Set-Location ..
```
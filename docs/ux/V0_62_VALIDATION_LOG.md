# v0.62 — Platform UX & Navigation Validation Log

## v0.62.1 — UX and Navigation Contract

### Objective

Define the unified series terminology, navigation, card design, arc behavior, and API requirements for Platform UX & Navigation.

### Series Terminology

Planned frontend terminology:

- `Available Anime` → `Available Series`
- `AnimeCard` → `SeriesCard`
- Anime-centric homepage language → Series-centric language

Stable backend `/anime` routes remain unchanged for compatibility.

### Series Card Contract

Each homepage Series Card will display:

- Series title
- Provider
- Available episode count
- Available chapter count
- Series-page navigation

Chapter counts must be supplied by the API rather than calculated through per-series frontend requests.

### Shared Card Design

Series, episode, and chapter cards will use a shared visual language:

- Consistent borders
- Consistent radius
- Consistent typography
- Consistent spacing
- Consistent hover and focus behavior

Layouts may differ according to content requirements.

### Bidirectional Navigation

Required flow:

- Episode detail → Chapter detail
- Chapter detail → Episode detail

Required API addition:

`GET /anime/{anime_id}/chapters/{chapter_number}/episodes`

### Search Identity

Chapter metadata search results must expose:

- Anime ID
- Anime title

This enables safe chapter-detail navigation.

### Arc Experience

Series pages will expose arc lists with:

- Arc name
- Episode count
- Chapter count

Initial interaction:

Arc selection filters the existing episode and chapter lists.

### Arc-Aware Search

Arc queries must return all matching:

- Episodes
- Chapter metadata

Existing search categories and Scope v2 mappings remain compatible.

### Baseline

- Backend tests: 231 passed
- Frontend production build: PASS
- Frontend lint: PASS

### Functional Changes

None.

### Result

v0.62 UX and navigation contract:

DEFINED
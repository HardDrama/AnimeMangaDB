# Chapter Metadata Source Review

## Goal

Identify reliable sources and selectors for Scope v3 chapter titles and manga arcs.

---

## One Piece

| Chapter | Source URL | Title Present? | Arc Present? | Notes |
|---------|------------|----------------|--------------|-------|
| 1 | https://onepiece.fandom.com/wiki/Chapter_1 | Yes | Yes | Title located below Chapter header, Arc located near the botton in "Site Navigation" |
| 50 | https://onepiece.fandom.com/wiki/Chapter_50 | Yes | Yes | Title located below Chapter header, Arc located near the botton in "Site Navigation" |
| Recent | https://onepiece.fandom.com/wiki/Chapter_1187 | Yes | Yes | Title located below Chapter header, Arc located near the botton in "Site Navigation" |

### Proposed Source

- Provider: https://onepiece.fandom.com/wiki/Chapters_and_Volumes
- Chapter URL pattern: https://onepiece.fandom.com/wiki/Chapter_####
- Title selector:
- Arc selector:
- Reliability notes:

---

## Naruto

| Chapter | Source URL | Title Present? | Arc Present? | Notes |
|---------|------------|----------------|--------------|-------|
| 1 | https://naruto.fandom.com/wiki/Naruto_Uzumaki!!_(chapter_1) | Yes | Yes | Chapter title is in the page header, Arc located in chapter info |
| 50 | https://naruto.fandom.com/wiki/I_Will%E2%80%A6!! | Yes | Yes | Chapter title is in the page header, Arc located in chapter info |
| 700 | https://naruto.fandom.com/wiki/Naruto_Uzumaki!!_(chapter_700) | Yes | Yes | Chapter title is in the page header, specific chapter has no arc |

### Proposed Source

- Provider: https://naruto.fandom.com/wiki/List_of_Volumes
- Chapter URL pattern: https://naruto.fandom.com/wiki/Chapter_Name_Chapter_###
- Title selector:
- Arc selector:
- Reliability notes:

---

## Findings

- [x] One Piece chapter title source verified
- [x] One Piece manga arc source verified
- [x] Naruto chapter title source verified
- [x] Naruto manga arc source verified
- [x] Source limitations documented
- [x] Provider strategy selected

## Provider Strategy

Chapter index pages are discovery sources.

Individual chapter pages are the authoritative source for:

- Chapter title
- Manga arc
- Source URL

One Piece supports predictable numbered chapter URLs.

Naruto uses title-based chapter URLs and therefore requires link discovery from the volume index.

The shared chapter metadata provider accepts a discovered source URL so both strategies can use the same extraction pipeline.

## Known Source Limitation

Some chapters, including Naruto Chapter 700, may not have a canonical manga arc listed.

These cases must be verified and represented through the existing metadata exception framework rather than assigned fabricated values.

## URL Discovery Strategy

One Piece chapter URLs are generated from the configured numbered pattern.

Naruto chapter URLs are discovered from the configured volume index because chapter links are title-based rather than number-based.

Discovery returns a canonical chapter page URL but does not extract or persist metadata.

## Verified Extraction Strategies

### One Piece

- Title: quoted title extracted from the chapter introduction sentence
- Manga arc: chapter category ending in `Arc Chapters`

### One Piece Chapter Titles

The canonical English chapter title is extracted from the infobox field:

`data-source="ename"`

This field is labeled `Viz Title` on the source page.

Descriptive introductory prose is not used because it may paraphrase rather than reproduce the official English title.

### Naruto

- Title: main page title with the `(chapter N)` suffix removed
- Manga arc: Semantic MediaWiki factbox property named `Arc`

Missing values remain null and are never fabricated.

## Controlled Ingestion Validation

The complete Scope v3 chapter metadata pipeline was validated using:

- One Piece Chapter 1
- Naruto Chapter 1

Validated flow:

```text
CLI
→ ChapterMetadataIngestionService
→ Chapter URL Discovery
→ Fandom Chapter Metadata Provider
→ Strategy-Based Extractor
→ Repository
→ Chapter Metadata Database Table

## Naruto Discovery Resolution

Naruto chapter discovery is scoped to the `Tankōbon` section of the volume index.

Chapter numbers are parsed from the leading numbered list-item prefix. This includes both Part I and Part II while excluding later spin-off manga sections such as Sasuke Retsuden.

## Controlled Batch Result

Validated:

- One Piece Chapters 1–5
- Naruto Chapters 1–5

Existing records were updated in place, incorrect discovery results were corrected, and no duplicates were created.
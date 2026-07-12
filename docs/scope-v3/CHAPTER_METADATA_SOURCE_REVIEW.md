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
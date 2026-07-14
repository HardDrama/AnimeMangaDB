# Naruto Scope v3 Manual Source Review

## Objective

Manually compare representative Naruto Scope v3 database records against their canonical Narutopedia source pages.

Fields reviewed:

- Chapter number
- English chapter title
- Manga arc
- Canonical source URL

---

## Dataset

- Anime: Naruto
- Target range: Chapters 1–700
- Expected records: 700
- Samples selected: 30

Manifest:

`reports/naruto_scope_v3_manual_validation.json`

---

## Sample Strategy

The representative sample includes:

- Early Part I chapters
- Regularly spaced chapters
- Chapter-number collision cases
- The Part I/Part II boundary
- Late Part II chapters
- The final main-series chapters
- Chapter 700, whose manga arc is verified as not applicable

Special validation targets:

| Chapter | Reason |
|---:|---|
| 10 | Multiple Naruto-related works use Chapter 10 |
| 244 | Final Part I chapter |
| 245 | First Part II chapter |
| 699 | Penultimate main-series chapter |
| 700 | Standalone epilogue and verified arc exception |

---

## Results

| Chapter | Title Match | Manga Arc Match | Source URL Valid | Notes |
|---:|:---:|:---:|:---:|---|
| 1 | PASS | PASS | PASS | PASS |
| 2 | PASS | PASS | PASS | PASS |
| 5 | PASS | PASS | PASS | PASS |
| 10 | PASS | PASS | PASS | PASS |
| 25 | PASS | PASS | PASS | PASS |
| 50 | PASS | PASS | PASS | PASS |
| 75 | PASS | PASS | PASS | PASS |
| 100 | PASS | PASS | PASS | PASS |
| 125 | PASS | PASS | PASS | PASS |
| 150 | PASS | PASS | PASS | PASS |
| 175 | PASS | PASS | PASS | PASS |
| 200 | PASS | PASS | PASS | PASS |
| 225 | PASS | PASS | PASS | PASS |
| 244 | PASS | PASS | PASS | PASS |
| 245 | PASS | PASS | PASS | PASS |
| 275 | PASS | PASS | PASS | PASS |
| 300 | PASS | PASS | PASS | PASS |
| 325 | PASS | PASS | PASS | PASS |
| 350 | PASS | PASS | PASS | PASS |
| 375 | PASS | PASS | PASS | PASS |
| 400 | PASS | PASS | PASS | PASS |
| 425 | PASS | PASS | PASS | PASS |
| 450 | PASS | PASS | PASS | PASS |
| 500 | PASS | PASS | PASS | PASS |
| 550 | PASS | PASS | PASS | PASS |
| 600 | PASS | PASS | PASS | PASS |
| 650 | PASS | PASS | PASS | PASS |
| 675 | PASS | PASS | PASS | PASS |
| 699 | PASS | PASS | PASS | PASS |
| 700 | PASS | PASS | PASS | Not Applicable |

---

## Review Procedure

For every selected chapter:

1. Open the stored `source_url`.
2. Confirm the source page belongs to the original Naruto manga.
3. Confirm the requested chapter number matches the source page.
4. Compare the stored chapter title with the source title.
5. Compare the stored manga arc with the source arc.
6. Confirm the stored source URL is canonical.
7. Record any discrepancy or ambiguity.

Allowed results:

- `PASS`
- `FAIL`
- `NOT APPLICABLE`

---

## Chapter 700 Review Rule

Chapter 700 is a standalone epilogue.

Expected database value:

```text
manga_arc = null
```

## Summary

- Samples reviewed: 30 / 30
- Chapter-number matches: 30 / 30
- Title matches: 30 / 30
- Manga-arc matches: 30 / 30
- Valid source URLs: 30 / 30
- Spin-off contamination records: 0
- Discrepancies: 0

Chapter 700:

- Title: validated
- Source URL: validated
- Manga arc: verified not applicable
- Stored null value: accurate

Status:

PASS
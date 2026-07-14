# Naruto Scope v3 Dataset

## Status

Implementation:

🚧 Source Verified

Certification:

⬜ Not Certified

---

## Dataset Definition

Anime:

Naruto

Expected chapter range:

- Start chapter: 1
- End chapter: 700

Expected records:

700

Included:

- Naruto Part I
- Naruto Part II

Excluded:

- Naruto Gaiden
- Boruto
- Sasuke Retsuden
- Other spin-off manga

The benchmark was verified from the canonical `Tankōbon` section of the Narutopedia volume index.

---

## Planned Metadata

- Chapter number
- Official English chapter title
- Manga arc
- Canonical source URL
- Last-updated timestamp

---

## Notes

This document will be expanded throughout the Naruto Scope v3 implementation.

---

## Ingestion Preflight

The complete Chapters 1–700 ingestion plan was validated before live ingestion.

Results:

- Chapters selected: 700
- Existing records: 5
- Would insert: 695
- Would update: 5
- Unresolved URLs: 0
- Database writes: 0
- Individual chapter pages fetched: 0

Naruto URL discovery fetched and cached the shared volume index while excluding unconfigured manga subsections.
# Scope v3 Specification

## Goal

Expand AnimeMangaDB with manga chapter metadata while preserving all certified Scope v2 capabilities.

Scope v3 adds:

- Manga Chapter Title
- Manga Arc

---

## Existing Scope v2

### Anime

- Episode Number
- Episode Title
- Anime Arc

### Manga

- Chapter Number

---

## Scope v3

### Anime

- Episode Number
- Episode Title
- Anime Arc

### Manga

- Chapter Number
- Chapter Title
- Manga Arc

---

## One Piece Scope v3 Dataset Implementation

Certified range:

- Chapters 1–1188
- Certified records: 1188

Certified metadata:

- Chapter number
- Official Viz title
- Manga arc
- Canonical source URL
- Last-updated timestamp

Certification evidence:

- Metadata audit: PASS
- Coverage audit: PASS
- Dataset audit: PASS
- Manual source validation: PASS
- Final validation: PASS
- Certification eligibility: ELIGIBLE
- Certification failures: 0

Status:

✅ Certified

---

## Naruto Scope v3 Dataset

Verified target:

- Chapters 1–700
- Expected records: 700
- Part I and Part II
- Main Naruto manga only

Excluded:

- Naruto Gaiden
- Boruto
- Spin-off manga

Canonical source:

Narutopedia `Tankōbon` volume-index section

Current status:

Source verified; ingestion preflight pending.
# Naruto Scope v3 Source Review

## Objective

Verify the canonical source, chapter boundary, and inclusion rules for the Naruto Scope v3 dataset before full ingestion.

---

## Canonical Source

Provider:

Narutopedia on Fandom

Index:

`https://naruto.fandom.com/wiki/List_of_Volumes`

Configured section:

`Tankōbon`

The `Tankōbon` section contains both:

- Part I
- Part II

The next top-level section ends the discovery scope.

---

## Verified Main-Series Range

- Start chapter: 1
- End chapter: 700
- Expected chapter records: 700
- Missing chapter numbers in source index: 0
- Duplicate chapter numbers in source index: 0

---

## Inclusion Rules

Included:

- Naruto main manga Part I
- Naruto main manga Part II
- Chapters 1–700

Excluded:

- Naruto Gaiden
- Boruto
- Sasuke Retsuden
- Other spin-offs
- Chapter identifiers using forms such as `700+1`

---

## Boundary Validation

| Entry | Classification | Included |
|---|---|:---:|
| Chapter 1 | Naruto main manga | Yes |
| Chapter 699 | Naruto main manga | Yes |
| Chapter 700 | Naruto main manga | Yes |
| Chapter 700+1 | Naruto Gaiden | No |

---

## Discovery Strategy

Chapter links are discovered by:

1. Locating the `Tankōbon` top-level section.
2. Searching through nested Part I and Part II content.
3. Parsing the leading numbered list-item prefix.
4. Comparing the parsed number exactly.
5. Stopping at the next top-level `h2`.
6. Excluding all later works and spin-offs.

---

## Evidence

Saved-source inspection:

`reports/naruto_scope_v3_source_inspection.json`

Live-source inspection:

`reports/naruto_scope_v3_live_source_inspection.json`

Saved fixture:

`tests/fixtures/naruto_list_of_volumes.html`

---

## Result

Canonical source verification:

PASS

Certified benchmark target:

Naruto Chapters 1–700

Status:

Ready for ingestion planning.
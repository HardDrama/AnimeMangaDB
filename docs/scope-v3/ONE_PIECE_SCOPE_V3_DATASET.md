# One Piece Scope v3 Dataset

## Status

Certification eligibility:

✅ ELIGIBLE

Formal dataset certification:

✅ CERTIFIED

---

## Dataset Definition

The One Piece Scope v3 dataset contains one chapter metadata record for every expected manga chapter in the certified target range.

Expected chapter range:

- Start chapter: 1
- End chapter: 1188
- Expected chapter records: 1188

Each record contains:

- Anime ID
- Chapter number
- Official Viz English chapter title
- Manga arc
- Canonical Fandom source URL
- Last-updated timestamp

---

## Source

Primary provider:

One Piece Wiki on Fandom

Chapter URL pattern:

```text
https://onepiece.fandom.com/wiki/Chapter_{chapter}
```

Chapter-title source:

```text
div[data-source="ename"] .pi-data-value
```

The source field is labeled:

```text
Viz Title
```

Manga-arc source:

Chapter category links ending with:

```text
Arc Chapters
```

The stored arc value removes the trailing:

```text
Chapters
```

---

## Canonical Metadata Rules

### Chapter Number

The chapter number is determined by the requested numbered chapter URL and stored as an integer.

### Chapter Title

The canonical English title is the source page’s official Viz title.

Descriptive introductory prose is not used because it may paraphrase the official English title.

### Manga Arc

The manga arc is derived from the verified chapter arc-category link.

### Source URL

The canonical source URL uses the configured numbered chapter path.

### Missing Metadata

Missing values are never fabricated.

No missing required metadata exists in the current One Piece Scope v3 dataset.

---

## Ingestion

The dataset was ingested through:

```text
Chapter Number
→ Numbered URL Discovery
→ Browser Client
→ Fandom Chapter Metadata Provider
→ Strategy-Based Extractor
→ ChapterMetadata Domain Model
→ Repository Upsert
→ chapter_metadata Table
```

The full range was processed in controlled batches.

Operational safeguards included:

- Dry-run preflight
- Complete-record skipping
- Partial-record update eligibility
- Per-chapter failure isolation
- Machine-readable batch reports
- Idempotent repository updates

---

## Ingestion Result

- Chapters selected: 1188
- Chapter records present: 1188
- Failed chapters: 0
- Missing chapter titles: 0
- Missing manga arcs: 0
- Missing source URLs: 0
- Missing last-updated timestamps: 0
- Duplicate chapter records: 0

---

## Automated Audit

Expected range:

```text
1–1188
```

Results:

- Metadata audit: PASS
- Coverage audit: PASS
- Dataset audit: PASS
- Coverage completion: 100.00%
- Missing chapter numbers: 0
- Duplicate chapter numbers: 0

Audit report:

```text
reports/one_piece_scope_v3_audit.json
```

---

## Manual Source Validation

Thirty representative chapters were reviewed across the complete dataset range.

The sample included:

- Early chapters
- Previously controlled chapters
- Regularly spaced chapters
- Recent chapters
- Final expected chapter

Fields reviewed:

- Chapter number
- Official Viz title
- Manga arc
- Source URL

Results:

- Samples reviewed: 30
- Chapter-number matches: 30
- Viz-title matches: 30
- Manga-arc matches: 30
- Valid source URLs: 30
- Discrepancies: 0
- Manual validation status: PASS

Manual review document:

```text
docs/scope-v3/ONE_PIECE_SCOPE_V3_MANUAL_REVIEW.md
```

Manual validation report:

```text
reports/one_piece_scope_v3_manual_validation.json
```

---

## Certification Eligibility

Evidence evaluated:

- Metadata audit
- Full-range coverage audit
- Dataset audit
- Representative manual source validation

Result:

- Certification failures: 0
- Certification status: ELIGIBLE

Certification eligibility report:

```text
reports/one_piece_scope_v3_certification.json
```

Eligibility means the evidence supports formal certification.

It does not itself change the dataset’s project status to certified.

---

## Reports

The following reports provide the machine-readable evidence for this dataset:

```text
reports/one_piece_scope_v3_audit.json
reports/one_piece_scope_v3_manual_validation.json
reports/one_piece_scope_v3_certification.json
reports/one_piece_scope_v3_ingest_0001_0100.json
reports/one_piece_scope_v3_ingest_0101_0200.json
reports/one_piece_scope_v3_ingest_0201_0300.json
reports/one_piece_scope_v3_ingest_0301_0400.json
reports/one_piece_scope_v3_ingest_0401_0500.json
reports/one_piece_scope_v3_ingest_0501_0600.json
reports/one_piece_scope_v3_ingest_0601_0700.json
reports/one_piece_scope_v3_ingest_0701_0800.json
reports/one_piece_scope_v3_ingest_0801_0900.json
reports/one_piece_scope_v3_ingest_0901_1000.json
reports/one_piece_scope_v3_ingest_1001_1100.json
reports/one_piece_scope_v3_ingest_1101_1188.json
```

---

## Scope Boundaries

This dataset certifies chapter metadata only.

Included:

- Chapter number
- Official Viz title
- Manga arc
- Source URL
- Last-updated timestamp

Not included in the current certification:

- Volume metadata
- Japanese chapter titles
- Release dates
- Cover art
- Color-page metadata
- API exposure
- Frontend chapter metadata integration
- Naruto Scope v3 dataset
- Platform Checkpoint v3

---

## Known Limitations

The dataset reflects the verified One Piece source state at the time of ingestion and validation.

One Piece is an ongoing manga. Future chapters require:

- New ingestion
- Updated expected range
- Coverage revalidation
- Manual validation sampling
- New certification evidence

The current target range remains fixed at Chapters 1–1188 for this certification cycle.

---

## Validation Commands

Full dataset audit:

```powershell
python -m tools.audit_scope_v3 `
    --anime "One Piece" `
    --expected-start 1 `
    --expected-end 1188 `
    --json-report reports/one_piece_scope_v3_audit.json
```

Certification eligibility audit:

```powershell
python -m tools.certify_scope_v3_dataset `
    --anime "One Piece" `
    --expected-start 1 `
    --expected-end 1188 `
    --audit-report reports/one_piece_scope_v3_audit.json `
    --manual-report reports/one_piece_scope_v3_manual_validation.json `
    --json-report reports/one_piece_scope_v3_certification.json
```

Regression validation:

```powershell
pytest

Set-Location frontend
npm run build
npm run lint
Set-Location ..
```

---

## Current Result

The complete One Piece Scope v3 dataset satisfies all automated and representative manual validation requirements.

Status:

Status:

✅ One Piece Scope v3 Dataset Certified

---

## Certification Scope

This certification applies to:

- One Piece
- Chapters 1–1188
- Chapter metadata defined by Scope v3

The certification does not automatically extend to chapters published after Chapter 1188.
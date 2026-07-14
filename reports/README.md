# AnimeMangaDB Reports

This directory contains machine-readable validation, ingestion, audit, and certification evidence.

Reports are committed when they serve as durable evidence for a feature checkpoint, dataset certification, or platform certification.

Temporary debugging output and browser caches should not be committed here.

---

## One Piece Scope v3

### Dataset Audit

```text
one_piece_scope_v3_audit.json
```

Contains:

- Metadata completion
- Expected range
- Coverage completion
- Missing chapter numbers
- Duplicate chapter numbers
- Dataset audit status

---

### Manual Validation

```text
one_piece_scope_v3_manual_validation.json
```

Contains:

- Representative chapter sample
- Stored metadata
- Manual title comparison
- Manual manga-arc comparison
- Manual source-URL validation
- Manual review result

---

### Certification Eligibility

```text
one_piece_scope_v3_certification.json
```

Contains:

- Audit evidence status
- Manual validation status
- Certification failures
- Certification eligibility result

---

### Ingestion Reports

```text
one_piece_scope_v3_ingest_0001_0100.json
one_piece_scope_v3_ingest_0101_0200.json
one_piece_scope_v3_ingest_0201_0300.json
one_piece_scope_v3_ingest_0301_0400.json
one_piece_scope_v3_ingest_0401_0500.json
one_piece_scope_v3_ingest_0501_0600.json
one_piece_scope_v3_ingest_0601_0700.json
one_piece_scope_v3_ingest_0701_0800.json
one_piece_scope_v3_ingest_0801_0900.json
one_piece_scope_v3_ingest_0901_1000.json
one_piece_scope_v3_ingest_1001_1100.json
one_piece_scope_v3_ingest_1101_1188.json
```

Each report contains:

- Selected chapter range
- Inserted records
- Updated records
- Skipped records
- Failed records
- Per-chapter result
- Elapsed time
- Import status

---

## Report Policy

A report should be regenerated when its underlying dataset or validation target changes.

A report should not be edited manually except for fields explicitly designed for manual review, such as:

```text
manual_title_match
manual_arc_match
manual_url_valid
manual_notes
validation_status
```

Certification reports should be generated from their source evidence rather than edited by hand.

## Naruto Scope v3

### Source Inspection

```text
naruto_scope_v3_source_inspection.json
naruto_scope_v3_live_source_inspection.json
```

### Ingestion Preflight

```text
naruto_scope_v3_preflight_0001_0010.json
naruto_scope_v3_preflight.json
```

### Naruto Ingestion Reports

```text
naruto_scope_v3_ingest_0001_0100.json
naruto_scope_v3_ingest_0101_0700.json
```

### Manual Validation

```text
naruto_scope_v3_manual_validation.json
```

### Certification Eligibility

```text
naruto_scope_v3_certification.json
```

---

## Standard Per-Series Evidence Policy

As AnimeMangaDB expands series support, the default durable Scope v3 report set is:

```text
<series>_scope_v3_audit.json
<series>_scope_v3_manual_validation.json
<series>_scope_v3_certification.json
```
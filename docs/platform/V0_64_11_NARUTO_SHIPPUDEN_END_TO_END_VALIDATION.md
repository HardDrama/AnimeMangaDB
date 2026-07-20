# v0.64.11 — Naruto Shippuden End-to-End Production Validation

## Purpose

Certify end-to-end production support for Naruto Shippuden after integrating the
dedicated episode-index crawler.

## Scope

In scope:

- Execute the production scraper using the Naruto Shippuden configuration.
- Verify episode discovery.
- Verify metadata extraction.
- Verify database persistence.
- Verify no regression for Naruto or One Piece.

Out of scope:

- Boruto production integration.

## Manual Validation

Run:

```powershell
python -m scraper.main --config configs/fandom/naruto_shippuden.json
```

Verify:

- Episode discovery succeeds.
- Episode URLs are valid.
- Titles populate.
- Chapter mappings populate.
- Arc metadata is extracted when present.
- Database records are written successfully.

## Regression Validation

Run:

```powershell
python -m pytest
```

Expected:

```text
750 passed
6 skipped
```

Run:

```powershell
npm run lint
npm run build
```

Expected:

```text
0 lint errors
Build successful
```

## Production Checklist

- Naruto still scrapes successfully.
- One Piece still scrapes successfully.
- Naruto Shippuden successfully completes production ingestion.
- No unexpected exceptions occur.

## Future Improvement

Current crawler selects the second table from
`List_of_Animated_Media`.

Observed evidence shows the table is introduced by the heading:

```html
<h3><span class="mw-headline" id="Naruto:_Shippūden">
Naruto: Shippūden
</span></h3>
```

Future revisions may locate the table by heading rather than index to improve
robustness without changing current behavior.
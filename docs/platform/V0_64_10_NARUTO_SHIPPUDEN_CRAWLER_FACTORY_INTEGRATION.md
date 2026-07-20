# v0.64.10 — Naruto Shippuden Crawler Factory Integration

## Feature Checkpoint

**Purpose:** Connect the certified Naruto Shippuden episode-index crawler to the production crawler factory while preserving existing Naruto and One Piece dispatch behavior.

## Scope

### In scope

- Import `NarutoShippudenEpisodeIndexCrawler` into the crawler factory.
- Dispatch `Naruto Shippuden` configurations to the dedicated crawler.
- Add regression coverage for Naruto and One Piece factory behavior.
- Validate that unrelated series retain their existing crawler selection.

### Out of scope

- Live Naruto Shippuden ingestion.
- Database, API, and frontend certification of Naruto Shippuden records.
- Provider or extractor changes.
- Changing the crawler's table-discovery implementation.

Those activities belong to v0.64.11.

## Evidence

Narutopedia identifies the Naruto Shippuden section with:

```html
<h3>
    <span id="Naruto:_Shipp.C5.ABden"></span>
    <span class="mw-headline" id="Naruto:_Shippūden">
        Naruto: Shippūden
    </span>
</h3>
```

The table visually follows the original Naruto table and is currently selected as the second table. Heading-based table discovery should be evaluated during v0.64.11 before final production certification.

## Files Changed

Update:

```text
scraper/crawlers/factory.py
```

Add:

```text
tests/crawlers/test_episode_index_factory.py
docs/platform/V0_64_10_NARUTO_SHIPPUDEN_CRAWLER_FACTORY_INTEGRATION.md
```

## Validation

Run the focused tests:

```powershell
python -m pytest tests/crawlers/test_episode_index_factory.py
```

Expected:

```text
3 passed
```

Run the complete suite:

```powershell
python -m pytest
```

Expected baseline:

```text
750 passed
6 skipped
```

Then run from the frontend directory:

```powershell
npm run lint
npm run build
```

Expected:

```text
0 lint errors
Build successful
```

## Certification Criteria

v0.64.10 is certified when:

- Naruto Shippuden selects `NarutoShippudenEpisodeIndexCrawler`
- Naruto still selects `NarutoEpisodeIndexCrawler`
- One Piece still selects `FandomEpisodeIndexCrawler`
- focused and complete Python tests pass
- frontend lint and build pass

## Commit

```text
v0.64.10 - Integrate Naruto Shippuden crawler factory
```

Suggested branch:

```text
feature/v0.64.10-naruto-shippuden-crawler-factory
```

## Discord Changelog

```text
v0.64.10 — Naruto Shippuden Crawler Factory Integration

Connected the dedicated Naruto Shippuden episode-index crawler to the production crawler factory.

Certified:
• Naruto Shippuden crawler dispatch
• Existing Naruto crawler dispatch
• Existing One Piece fallback
• Configuration-driven production selection
• Factory regression coverage

Validation:
• Focused crawler factory tests passed
• Complete Python test suite passed
• Frontend lint passed
• Frontend build passed

Next:
v0.64.11 — Naruto Shippuden End-to-End Production Validation
```

## Roadmap

### Completed

- v0.64.7 — Multi-Series Architecture Validation
- v0.64.8 — Naruto Shippuden Production Configuration
- v0.64.9 — Naruto Shippuden Episode Index Crawler
- v0.64.10 — Naruto Shippuden Crawler Factory Integration

### Next

- v0.64.11 — Naruto Shippuden End-to-End Production Validation

### Deferred

- Boruto production integration remains deferred until Naruto Shippuden production integration is certified.

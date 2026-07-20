# v0.64.7 — Multi-Series Architecture Validation

## Feature Checkpoint

**Purpose:** Validate and certify the existing multi-series production architecture before adding Naruto Shippuden production support.

This checkpoint introduces **no production behavior changes**. It documents and validates the current configuration-driven architecture and identifies the episode-index crawler as the remaining series-specific integration point.

---

## 1. Scope

### In scope

- Validate configuration-driven runtime selection.
- Validate shared Fandom provider behavior.
- Validate shared Fandom extractor behavior.
- Validate scraper service wiring.
- Confirm that episode-index discovery is the current series-specific layer.
- Preserve all certified One Piece and Naruto behavior.
- Record the production integration path for Naruto Shippuden.

### Out of scope

- Correcting `configs/fandom/naruto_shippuden.json`.
- Adding a Naruto Shippuden crawler.
- Updating crawler factory dispatch.
- Running Naruto Shippuden production ingestion.
- Adding Boruto production support.

Those changes belong to v0.64.8 through v0.64.11.

---

## 2. Architecture Validation

### Configuration loading

Production execution is driven by a JSON configuration file supplied through:

```text
--config
```

The configuration is loaded and validated as `ProviderConfig`.

**Certified conclusion:** Series behavior is selected through configuration rather than a central series registry.

### Provider factory

The provider factory always returns:

```python
FandomProvider(config)
```

**Certified conclusion:** One Piece, Naruto, Naruto Shippuden, and Boruto can share the same provider while they remain hosted on Fandom-compatible sites.

No series-specific provider dispatch is required.

### Extractor factory

The extractor factory always returns:

```python
FandomExtractor(config)
```

**Certified conclusion:** Episode metadata extraction is already configuration-driven through selectors and does not currently require series-specific factory dispatch.

### Episode-index crawler factory

The crawler factory currently selects:

```python
NarutoEpisodeIndexCrawler
```

only when:

```python
config.series == "Naruto"
```

All other series fall back to:

```python
FandomEpisodeIndexCrawler
```

The existing crawlers are structurally specialized:

- `NarutoEpisodeIndexCrawler` reads the original Naruto table from Narutopedia's animated-media list.
- `FandomEpisodeIndexCrawler` follows the One Piece Episode Guide hierarchy.

**Certified conclusion:** Episode discovery is the remaining production layer that requires explicit series-specific integration.

---

## 3. Certified Architecture

```text
JSON configuration
        ↓
ProviderConfig validation
        ↓
ScraperServices
        ├── provider factory
        │       └── shared FandomProvider
        ├── extractor factory
        │       └── shared FandomExtractor
        ├── crawler factory
        │       └── series-specific episode discovery
        └── repository
                └── shared persistence behavior
```

### Source-of-truth rule

Do not introduce `configs/series_registry.json`.

The existing configuration file supplied to `scraper.main` remains the single runtime source of truth.

### Future-series integration rule

A new Fandom-hosted series should first attempt to reuse:

- `FandomProvider`
- `FandomExtractor`
- existing repositories
- existing service wiring

A dedicated implementation should be added only where observed source structure requires it.

For Naruto Shippuden, current evidence requires a dedicated episode-index crawler.

---

## 4. Files Changed

Add this document:

```text
docs/platform/V0_64_7_MULTI_SERIES_ARCHITECTURE_VALIDATION.md
```

No Python, frontend, database, API, or configuration behavior is changed in this checkpoint.

---

## 5. Implementation Steps

### Step 1 — Add the validation document

Create:

```text
docs/platform/V0_64_7_MULTI_SERIES_ARCHITECTURE_VALIDATION.md
```

Use the complete contents of this file.

### Step 2 — Confirm no unintended production changes

Run:

```powershell
git status
```

Expected result:

- this validation document is the only intended new file
- `configs/fandom/naruto_shippuden.json` may remain uncommitted if it is still incomplete
- no Python production file should be modified for v0.64.7

### Step 3 — Run backend validation

```powershell
python -m pytest
```

Expected result:

```text
745 passed
6 skipped
```

A higher passing count is acceptable if additional valid tests have been added since v0.64.6.

### Step 4 — Run frontend lint validation

From the frontend directory:

```powershell
npm run lint
```

Expected result:

```text
No lint errors
```

### Step 5 — Run frontend build validation

From the frontend directory:

```powershell
npm run build
```

Expected result:

```text
Build successful
```

### Step 6 — Review the checkpoint diff

```powershell
git diff -- docs/platform/V0_64_7_MULTI_SERIES_ARCHITECTURE_VALIDATION.md
```

For an untracked file:

```powershell
git diff --no-index NUL docs/platform/V0_64_7_MULTI_SERIES_ARCHITECTURE_VALIDATION.md
```

Expected result:

- documentation-only checkpoint
- no production behavior changes
- architecture conclusions match the inspected factories and crawlers

---

## 6. Validation Record

```text
Python tests:
[enter result]

Frontend lint:
[enter result]

Frontend build:
[enter result]

Production files changed:
None

Configuration files changed:
None

Architecture conclusion:
Provider and extractor layers are reusable.
Episode-index discovery is the remaining series-specific integration point.
```

---

## 7. Certification Criteria

v0.64.7 is certified when:

- the validation document exists
- the complete Python test suite passes
- frontend lint passes
- frontend build succeeds
- no production behavior is changed
- the configuration file remains the runtime source of truth
- the crawler layer is formally identified as the Naruto Shippuden integration point

---

## 8. Commit

### Commit message

```text
v0.64.7 - Validate multi-series architecture
```

### Suggested branch

```text
feature/v0.64.7-multi-series-architecture-validation
```

### GitHub Desktop workflow

1. Confirm only the intended validation document is selected.
2. Enter the commit message above.
3. Commit to the current feature branch.
4. Push the branch.
5. Merge the branch into `main` after validation.
6. Pull `main` locally.
7. Delete the feature branch after confirming the merge.

---

## 9. Discord Changelog

```text
v0.64.7 — Multi-Series Architecture Validation

Validated the existing production architecture before beginning Naruto Shippuden integration.

Certified:
• Configuration-driven runtime selection
• Shared Fandom provider behavior
• Shared configuration-driven extractor behavior
• Existing scraper service wiring
• Configuration files as the single runtime source of truth

Confirmed:
• No series registry is required
• Provider and extractor factories require no Naruto Shippuden changes
• Episode-index discovery is the remaining series-specific integration layer
• Existing Naruto and One Piece production behavior remains unchanged

Validation:
• Complete Python test suite passed
• Frontend lint passed
• Frontend build passed

Next:
v0.64.8 — Naruto Shippuden Production Configuration
```

---

## 10. Updated Roadmap

### Completed

- v0.64.2 — Boruto fixture capture
- v0.64.3 — Boruto characterization foundation
- v0.64.4 — Boruto fixture observation
- v0.64.5 — Boruto metadata characterization
- v0.64.6 — Boruto mapping characterization
- v0.64.7 — Multi-Series Architecture Validation

### Next

- v0.64.8 — Naruto Shippuden Production Configuration
- v0.64.9 — Naruto Shippuden Episode Index Crawler
- v0.64.10 — Naruto Shippuden Crawler Factory Integration
- v0.64.11 — Naruto Shippuden End-to-End Production Validation

### Deferred

- Boruto production integration remains deferred until Naruto Shippuden production integration is certified.

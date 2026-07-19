# v0.63.3 — Third-Series Benchmark Selection

## Status

Complete

## Objective

Select the third AnimeMangaDB benchmark series using technical evidence rather than popularity or assumption.

The selected series must provide a meaningful test of the multi-series architecture while remaining achievable through the existing onboarding framework.

## Scope

This checkpoint evaluates candidate series only.

No scraper, configuration, database, API, frontend, fixture, or test changes are included.

## Benchmark Purpose

The third benchmark series should prove that AnimeMangaDB can onboard another series without duplicating benchmark-specific platform logic.

The benchmark should test:

- Configuration-driven episode URL construction
- Configurable episode selectors
- Chapter-number extraction
- Chapter URL discovery
- Chapter-title extraction
- Manga-arc extraction
- Exception handling
- Metadata overrides
- Database isolation by series
- Generic API behavior
- Generic frontend behavior
- Global search across three series

## Mandatory Criteria

A candidate must satisfy all mandatory criteria.

| Criterion | Requirement |
|---|---|
| Anime and manga relationship | The anime must adapt a numbered manga source |
| Episode metadata | Individual episode pages must be discoverable |
| Manga mapping | Episode pages must expose chapter adaptation information |
| Chapter metadata | Chapter titles must be discoverable |
| Stable numbering | Episodes and chapters must use stable numeric identifiers |
| Source accessibility | Required pages must be accessible through the current browser workflow |
| Series separation | Data must be distinguishable from existing benchmark series |
| Validation potential | The series must provide enough evidence for repeatable testing |

## Comparative Criteria

Candidates that satisfy the mandatory criteria will be compared using the following factors.

| Criterion | Weight |
|---|---:|
| Compatibility with existing Fandom provider | 20 |
| Episode-to-chapter metadata quality | 20 |
| Chapter metadata availability | 15 |
| Value as a multi-series architecture test | 15 |
| Source consistency | 10 |
| Reasonable initial benchmark size | 10 |
| Need for reusable platform extension | 5 |
| Availability of verifiable edge cases | 5 |
| Total | 100 |

## Candidate Shortlist

### Candidate: Naruto Shippuden (anime)

- Anime source: https://naruto.fandom.com/wiki/List_of_Animated_Media
- Manga source: n/a
- Provider: Fandom
- Episode page pattern: 
- Chapter discovery pattern:
- Episode chapter metadata:
- Chapter title metadata:
- Manga arc metadata:
- Estimated episode count:
- Estimated chapter count:
- Initial technical observations:

## Expected v0.63.4 Scope

Based on the selected benchmark, v0.63.4 is expected to include only confirmed requirements.

Potential work:

- Add the selected series configuration
- Add benchmark fixtures
- Add configuration validation tests
- Reuse existing provider behavior
- Reuse existing extraction strategies where evidence supports them
- Add a new reusable extraction strategy only if required
- Add exception or override configuration only for confirmed source defects
- Validate database isolation
- Validate API visibility
- Validate frontend rendering
- Validate cross-series search

## Automated Validation

- Backend: 250 passed, 0 failed
- Frontend lint: 0 errors
- Frontend production build: successful
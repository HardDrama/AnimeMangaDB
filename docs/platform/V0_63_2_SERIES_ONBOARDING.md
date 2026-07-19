# v0.63.2 — Series Onboarding Framework

## Status

Planning

## Objective

Define the standard process for onboarding a new series into AnimeMangaDB.

The onboarding process should be repeatable, evidence-driven, and require minimal platform changes.

## Onboarding Lifecycle

1. Research
2. Configuration
3. Scraping
4. Extraction
5. Metadata
6. Validation
7. Certification

## Required Configuration

configs/fandom/<series>.json

configs/exceptions/<series>.json

configs/overrides/<series>.json (optional)

## Acceptance Criteria

- Configuration complete
- Episode scraping succeeds
- Chapter metadata succeeds
- Overrides supported
- Exceptions supported
- Database imports successfully
- API endpoints function
- Frontend renders correctly
- Search functions correctly
- Tests pass

## Reusable Assets

- BaseProvider
- FandomProvider
- Repository
- Database
- API
- Frontend
- Selector engine
- Browser client
- Metadata providers
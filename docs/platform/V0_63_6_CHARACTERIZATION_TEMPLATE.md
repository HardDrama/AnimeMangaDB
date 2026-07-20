# v0.63.6 Characterization Template

## Purpose

This document defines the standard characterization process used when onboarding
a new benchmark series into AnimeMangaDB.

Characterization captures the observed structure of source pages before any
production parser or extractor is implemented.

Characterization tests must never depend on production code.

They exist solely to document and preserve observed source behavior.

## Required Metadata

Every characterization benchmark must define:

- BENCHMARK_NAME
- SOURCE_PROVIDER
- SOURCE_TYPE
- BENCHMARK_VERSION

## Required Metadata

Every characterization benchmark must define:

- BENCHMARK_NAME
- SOURCE_PROVIDER
- SOURCE_TYPE
- BENCHMARK_VERSION

## Required Selectors

Every characterization benchmark must define selectors for:

- infobox
- title
- chapter
- chapter_value
- arc
- arc_value

Selectors should target semantic HTML whenever possible.

Prefer attributes such as:

data-source="chapters"

instead of presentation classes.

## Required Characterization Fields

Every benchmark episode must include:

- classification
- mapping_shape
- expects_chapter_mapping
- expects_arc
- expected_title
- expected_chapter_text
- expected_arc
- notes

## Required Test Categories

Every characterization suite must contain:

- Fixture integrity
- Registry integrity
- Metadata validation
- Selector validation
- Structure validation
- Metadata value validation
- Regression protection

## Design Rules

Characterization suites must:

- Never import production extractors.
- Never import providers.
- Never access the database.
- Never call the REST API.
- Never parse business logic.

Characterization documents observations only.

## Reuse Rules

Characterization should only become reusable platform architecture after
multiple independent benchmark series demonstrate the same behavior.

Observed once
→ Document

Observed twice
→ Compare

Observed three or more times
→ Consider shared implementation

Do not generalize from a single benchmark.

## Future Benchmark Checklist

For every new benchmark:

- Select representative benchmark episodes.
- Capture HTML fixtures.
- Characterize page structure.
- Characterize metadata values.
- Validate registry.
- Validate selectors.
- Run characterization suite.
- Certify benchmark.

## Certification Requirements

A benchmark characterization is considered certified when:

- Characterization tests pass.
- Full backend test suite passes.
- Frontend lint passes.
- Frontend production build succeeds.
- Documentation is complete.
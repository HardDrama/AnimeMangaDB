# v0.65.0 — Shared Manga Production Plan

## Objective

Activate the already-certified shared manga runtime in a controlled, checkpoint-driven manner.

This release introduces **no new architecture**. All runtime composition, compatibility layers, factories, and validation infrastructure were completed during Platform Checkpoint v2.5.

The purpose of the v0.65 series is to activate that architecture safely.

## Development Branch

`feature/shared-manga-production-activation`

## Guiding Principles

- Evidence-driven architecture
- Build → Test → Document → Validate → Certify
- Thin frontend
- Stable REST API
- Controlled activation
- Small reversible checkpoints

## Scope

### Included

- Shared manga database migration
- Production runtime activation
- Compatibility cleanup
- Full certification
- Platform Checkpoint v3

### Not Included

- New REST endpoints
- New scraper providers
- New benchmark datasets
- Frontend feature work
- Scope v3 expansion
- Performance optimization unrelated to activation

## Activation Roadmap

### v0.65.1 — Migration Certification

- Register migration
- Validate clean database upgrade
- Validate populated database upgrade
- Verify data preservation
- Document migration results

**Certification Gate:** Migration succeeds without data loss.

### v0.65.2 — Production Runtime Activation

- Switch runtime composition default
- Legacy runtime available only for rollback if required
- REST API remains unchanged

**Certification Gate:** Existing API contract remains fully compatible.

### v0.65.3 — Compatibility Cleanup

- Remove temporary compatibility shims
- Remove duplicated staged implementations
- Preserve reusable runtime composition framework

**Certification Gate:** No behavior changes.

### v0.65.4 — Shared Manga Certification

Validate:

- Backend
- Database
- API
- Repositories
- Reports
- Benchmark datasets

**Certification Gate:** Full regression suite passes.

### v0.65.5 — Platform Checkpoint v3

Deliverables:

- Production shared runtime certified
- Legacy runtime retired
- Updated architecture documentation
- Updated roadmap

## Production Activation Sequence

1. Enable migration registry.
2. Execute migration.
3. Verify migrated database.
4. Switch production runtime default.
5. Execute full certification.
6. Remove legacy compatibility.
7. Certify Platform Checkpoint v3.

## Success Criteria

- Shared manga ownership is active.
- Existing REST API remains unchanged.
- Existing clients require no modifications.
- One Piece benchmark remains certified.
- Naruto benchmark remains certified.
- Full automated regression suite passes.
- Platform Checkpoint v3 is achieved.

## Risk Management

The runtime composition framework developed during Platform Checkpoint v2.5 remains in place throughout activation. Every activation checkpoint must leave the project in a fully working, certifiable state before advancing.

No checkpoint should combine architecture changes with production activation.

## Expected Outcome

At completion of the v0.65 series:

- Shared manga becomes the production ownership model.
- Runtime composition remains available as a long-term architectural capability.
- The platform is positioned for future multi-series expansion without requiring another structural redesign.

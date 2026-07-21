# v0.64.12 — Shared Manga Architecture Validation

## Feature Checkpoint

**Purpose:** Validate and certify the shared-manga architecture required for multiple anime series to reference one canonical manga chapter catalog.

This checkpoint is documentation and architecture validation only. It does not modify production runtime behavior.

## 1. Problem Statement

The current database model attaches `ChapterMetadata` directly to `Anime` through `anime_id`.

That works for a one-anime-to-one-manga structure such as One Piece, but it does not support franchises where multiple anime adapt the same manga.

Naruto exposes the limitation:

```text
Naruto
Naruto Shippuden
```

are separate anime series, but both adapt the Naruto manga.

The current implementation allows Naruto Shippuden episode mappings to contain correct chapter numbers while chapter metadata lookups fail because the chapter catalog belongs to the original Naruto anime record.

## 2. Certified Architectural Decision

Adopt a shared manga entity.

```text
Manga
├── id
├── title
├── provider
└── base_url

Anime
├── id
├── title
├── provider
├── base_url
└── manga_id

Episode
└── anime_id

EpisodeChapter
├── episode_id
└── chapter_number

ChapterMetadata
├── manga_id
├── chapter_number
├── chapter_title
├── manga_arc
├── source_url
└── last_updated
```

### Ownership Rules

- Anime owns episodes.
- Manga owns chapter metadata.
- Multiple anime may reference one manga.
- Episode-to-chapter mappings remain chapter-number based for v0.64.
- Chapter metadata remains a canonical single source of truth.

## 3. Naruto Target Relationship

```text
Manga: Naruto
├── Chapters 1–700
├── Anime: Naruto
└── Anime: Naruto Shippuden
```

Existing Naruto chapter metadata will move to the shared Naruto manga record.

Naruto Shippuden will reference the same manga record without duplicating chapter metadata.

## 4. One Piece Target Relationship

```text
Manga: One Piece
└── Anime: One Piece
```

One Piece keeps its existing behavior while adopting the same reusable model.

## 5. Rejected Alternatives

### Shared Anime ID

Rejected because Naruto and Naruto Shippuden are distinct anime series with separate episode numbering, counts, titles, arcs, source pages, and frontend detail pages.

### Split Manga Catalog

Rejected because it would duplicate Naruto chapter metadata across Naruto and Naruto Shippuden.

That would violate the single-source-of-truth requirement and complicate ingestion, repair, overrides, search, reports, and future franchise integrations.

## 6. Arc Navigation Compatibility

The existing arc navigation model remains valid.

The series detail page will continue to combine:

```text
episodes filtered by anime
+
chapters filtered by linked manga
```

Arc summaries remain structured as:

```text
name
episode_arc
manga_arc
episode_count
chapter_count
```

The repository will calculate:

```text
episode_count from Episode.anime_id
chapter_count from ChapterMetadata.manga_id
```

The frontend may continue filtering with:

```text
selectedArc.episode_arc
selectedArc.manga_arc
```

No visible arc-navigation redesign is required.

## 7. API Compatibility Strategy

Preserve the current compatibility routes during v0.64:

```text
/anime/{anime_id}/chapters
/anime/{anime_id}/chapters/{chapter_number}
/anime/{anime_id}/chapters/{chapter_number}/episodes
```

These routes will resolve chapter metadata internally through:

```text
anime_id
→ Anime.manga_id
→ ChapterMetadata.manga_id
```

Example:

```text
/anime/3/chapters/249
```

may represent Naruto Shippuden while resolving Chapter 249 from the shared Naruto manga catalog.

Canonical manga routes may be introduced later, but they are not required to complete Naruto Shippuden support.

## 8. Repository Strategy

The repository currently owns both episode and chapter behavior.

For v0.64, it may continue doing so while methods are updated to resolve manga identity.

Required behavior changes in later checkpoints include:

```text
get_chapter_metadata
list_chapter_metadata
count_chapters_for_anime
list_arc_summaries
create_or_update_chapter_metadata
save_chapter_metadata
search_chapter_metadata
```

Episode-scoped methods remain anime-specific:

```text
list_episodes_for_anime
get_episodes_by_anime_and_chapter
```

Global chapter lookup remains global:

```text
get_episodes_by_chapter
```

## 9. Chapter Ingestion Strategy

Chapter ingestion becomes manga-oriented.

Current conceptual flow:

```text
Anime
→ ChapterMetadata
```

Target flow:

```text
Manga
→ ChapterMetadata
```

The command-line interface should eventually use:

```powershell
python tools/ingest_chapter_metadata.py --manga "Naruto" ...
```

A temporary compatibility path for `--anime` may be retained, but Naruto Shippuden must not receive a duplicate chapter catalog.

## 10. Search Strategy

Chapter metadata search should expose manga identity rather than one arbitrary anime identity.

Target search metadata:

```text
manga_id
manga_title
chapter_number
chapter_title
manga_arc
source_url
last_updated
```

Associated anime may be added later where useful.

Episode and anime search behavior remains unchanged.

## 11. Migration Strategy

The project currently uses SQLAlchemy `create_all()` without a migration framework.

Therefore, v0.64.13 must include an explicit SQLite migration script.

The migration must:

1. Create the `manga` table.
2. Create one manga record for One Piece.
3. Create one manga record for Naruto.
4. Add `manga_id` to anime records.
5. Link One Piece anime to One Piece manga.
6. Link Naruto anime to Naruto manga.
7. Link Naruto Shippuden anime to Naruto manga.
8. Rebuild `chapter_metadata` with `manga_id`.
9. Copy existing One Piece chapter metadata.
10. Copy existing Naruto chapter metadata.
11. Preserve chapter row counts and metadata values.
12. Preserve foreign-key integrity.
13. Prevent duplicate `(manga_id, chapter_number)` rows.
14. Validate that Naruto Shippuden resolves Naruto chapter metadata.

Deleting and recreating the production database is not part of the approved migration strategy.

## 12. Testing Strategy

Future implementation checkpoints must add coverage for:

- creating and reusing manga records
- linking multiple anime to one manga
- preserving distinct anime episode catalogs
- shared chapter metadata lookup
- shared chapter counts
- shared arc summaries
- Naruto Shippuden chapter detail resolution
- Naruto and One Piece regression behavior
- chapter metadata search using manga identity
- migration row-count preservation
- migration foreign-key integrity

## 13. Scope Boundaries

### Included

- shared manga architecture
- chapter ownership model
- API compatibility plan
- arc preservation plan
- migration strategy
- ingestion direction
- search direction

### Excluded

- production model changes
- database migration execution
- API implementation
- frontend implementation
- Naruto Shippuden full ingestion
- episode-title cleanup

## 14. Certification Criteria

v0.64.12 is certified when:

- Manga is accepted as the canonical chapter owner.
- Anime remains the canonical episode owner.
- Naruto and Naruto Shippuden remain separate anime records.
- Both Naruto anime records are planned to share one Naruto manga.
- One Piece is planned to link to one One Piece manga.
- Arc filtering remains supported.
- Current anime chapter routes are preserved as compatibility routes.
- Chapter duplication is explicitly rejected.
- An explicit SQLite migration is required.
- No production behavior changes occur in this checkpoint.

## 15. Validation Commands

Run the complete Python suite:

```powershell
python -m pytest
```

Expected baseline:

```text
750 passed
6 skipped
```

Run frontend validation:

```powershell
npm run lint
npm run build
```

Expected:

```text
0 lint errors
Build successful
```

Because this checkpoint is documentation-only, no production behavior should change.

## 16. Commit

Suggested branch:

```text
feature/v0.64.12-shared-manga-architecture
```

Commit message:

```text
v0.64.12 - Validate shared manga architecture
```

## 17. Discord Changelog

```text
v0.64.12 — Shared Manga Architecture Validation

Validated the architecture required for multiple anime series to share one canonical manga chapter catalog.

Certified:
• Manga owns chapter metadata
• Anime owns episodes
• Multiple anime may share one manga
• Naruto and Naruto Shippuden remain separate anime series
• Naruto and Naruto Shippuden will share one Naruto manga catalog
• One Piece will link to one One Piece manga catalog
• Existing arc filtering will be preserved
• Existing anime chapter routes will remain compatible
• Explicit SQLite migration required
• Chapter duplication rejected

No production runtime behavior changed.

Next:
v0.64.13 — Shared Manga Database Foundation
```

## 18. Updated Roadmap

### Completed

- v0.64.7 — Multi-Series Architecture Validation
- v0.64.8 — Naruto Shippuden Production Configuration
- v0.64.9 — Naruto Shippuden Episode Index Crawler
- v0.64.10 — Naruto Shippuden Crawler Factory Integration
- v0.64.11 — Naruto Shippuden Initial Production Validation
- v0.64.12 — Shared Manga Architecture Validation

### Next

- v0.64.13 — Shared Manga Database Foundation
- v0.64.14 — Shared Manga Repository and API Integration
- v0.64.15 — Frontend Integration and Metadata Cleanup
- v0.64.16 — Full Naruto Shippuden Ingestion and Certification

### After v0.64

- Platform Checkpoint v3
- Next production series

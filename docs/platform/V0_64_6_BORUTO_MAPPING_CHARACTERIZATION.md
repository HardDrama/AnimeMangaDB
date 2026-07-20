# Mapping Categories

The Boruto benchmark currently contains the following observed mapping types:

- Single Boruto chapter
- Multiple consecutive Boruto chapters
- Multiple non-consecutive Boruto chapters
- Naruto side-story chapters

# Chapter Namespaces

Observed namespaces:

- Boruto Chapter
- Naruto Chapter

The benchmark intentionally preserves the namespace exactly as observed in the
source.

Characterization does not normalize chapter references.

# Non-Consecutive Mappings

Some benchmark episodes reference non-consecutive manga chapters.

Example:

Boruto Chapter #24
Boruto Chapter #26

Characterization records the observed values exactly as presented by the
source page.

# Missing Arc Metadata

Episode 39 does not contain an Arc field.

This is treated as observed source behavior rather than an error.

Characterization preserves this distinction.

# Mapping Shapes

Observed mapping shapes include:

- single
- multiple

No benchmark episode currently lacks chapter mappings.

# Characterization Rules

Characterization records:

- exact chapter text
- exact namespaces
- exact ordering
- exact comma placement after normalization

Characterization never attempts to infer missing chapters or ranges.

# Future Production Considerations

Future production code may normalize chapter references for database storage.

This normalization is outside the scope of characterization.

Characterization exists only to preserve the observed source values.
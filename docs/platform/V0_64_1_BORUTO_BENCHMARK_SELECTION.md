# v0.64.1 Boruto Benchmark Selection

## Purpose

Select the representative Boruto: Naruto Next Generations episode benchmark
that will be characterized before any production implementation begins.

This checkpoint selects benchmark cases only.

It does not add fixtures, characterization tests, providers, extractors,
database records, API behavior, or frontend behavior.

The benchmark follows the characterization contract documented in
`V0_63_6_CHARACTERIZATION_TEMPLATE.md`.

---

## Evidence Used

The Boruto anime consists of 293 episodes and contains several source
relationships:

- direct Boruto manga adaptation
- mixed manga and anime-original material
- anime-original material
- novel or Naruto side-story adaptation
- episodes without a Boruto manga chapter mapping

The selected benchmark must exercise these different page and mapping shapes
without attempting to represent every arc.

---

## Selection Principles

A benchmark episode should be selected only when it contributes a distinct
characterization case.

The benchmark should include:

- the first episode
- early manga adaptation
- a single-chapter mapping
- a multi-chapter mapping
- mixed adaptation
- anime-original content
- an arc boundary
- the beginning of a major late-series manga arc
- a late-series multi-chapter adaptation
- the final episode

Episodes should not be selected merely because they are popular.

The benchmark exists to exercise source structures and adaptation metadata.

---

## Selected Benchmark Episodes

| Episode | Benchmark role | Expected source relationship | Selection reason |
|---:|---|---|---|
| 1 | Series opening | Mixed | Tests the opening episode and a page that combines the manga flash-forward with anime-original material. |
| 19 | Early manga adaptation | Manga-derived | Begins the Sarada Uchiha material and tests an early adapted episode. |
| 39 | Standalone manga-derived case | Manga-derived | Tests a compact Mitsuki-focused adaptation outside a long consecutive manga arc. |
| 53 | Major manga arc start | Manga-derived | Begins the anime's direct movement into the Chūnin Exam and Momoshiki material. |
| 65 | Major manga arc climax | Manga-derived | Tests a high-density adaptation near the climax of the Versus Momoshiki material. |
| 148 | Manga arc transition | Manga-derived | Begins the Mujina Bandits adaptation and tests a later return to direct manga material. |
| 181 | Late manga arc start | Manga-derived | Begins the Vessel and Kara-related adaptation sequence. |
| 189 | Character introduction boundary | Manga-derived | Tests the Kawaki introduction portion of the late-series manga adaptation. |
| 192 | Mixed characterization case | Mixed | Tests an episode commonly separated from fully manga-derived surrounding episodes. |
| 220 | Major arc conclusion | Manga-derived | Tests the end of the Kawaki and Isshiki adaptation period and a late arc boundary. |
| 287 | Final manga arc start | Manga-derived | Begins the Code's Assault adaptation at the end of the animated series. |
| 293 | Series finale | Manga-derived with anime framing | Tests the final episode, late-series mapping, and closing-series behavior. |

---

## Benchmark Episode Registry

The selected episode inventory is:

```python
BENCHMARK_EPISODES = (
    1,
    19,
    39,
    53,
    65,
    148,
    181,
    189,
    192,
    220,
    287,
    293,
)
```

The ordering is intentional and must remain ascending.

---

## Characterization Targets

The selected benchmark is expected to reveal whether Boruto episode pages
provide stable values for:

- episode infobox
- episode title
- manga chapter field
- arc field
- single-chapter mappings
- multi-chapter mappings
- absent chapter mappings
- mixed-source episode descriptions
- late-series episode metadata

These expectations remain hypotheses until the fixtures are captured and
inspected.

Characterization must record the observed values rather than forcing the
source pages to match this selection document.

---

## Manga Fixture Strategy

Boruto has an independent manga dataset.

Unlike Naruto Shippuden, Boruto must not reuse the Naruto manga fixtures.

Manga chapter fixtures should be selected only after episode characterization
identifies the actual chapter references present in the chosen episode pages.

This prevents speculative chapter fixture collection.

---

## Out of Scope

This checkpoint does not:

- classify the entire Boruto anime
- determine a universal definition of canon
- create production mapping behavior
- assume every selected episode contains chapter metadata
- assume Boruto uses the same selectors as Naruto Shippuden
- create chapter fixtures
- create episode fixtures
- create characterization tests

---

## Next Checkpoint

The next checkpoint will capture the selected episode fixtures and record their
source URLs.

After the fixtures exist, characterization will determine:

- actual selectors
- actual title values
- actual chapter values
- actual arc values
- mapping shapes
- missing or unusual metadata

---

## Validation

Run:

```powershell
python -m pytest
```

Expected:

```text
462 passed
5 skipped
```

Run:

```powershell
cd frontend
npm run lint
npm run build
```

Expected:

```text
0 lint errors
Production build successful
```

---

## Certification Requirements

This selection checkpoint is complete when:

- the selected inventory is documented
- the selection reasons are documented
- no speculative fixtures or production behavior are added
- the full backend test suite passes
- frontend lint passes
- the frontend production build succeeds

# ND Oracle whole-site content inventory v0.2

Status date: 2026-08-12

Authoritative repository baseline: `6aa403dab31df00217f3bb1c22a60c95ee9b3904`

This inventory counts only material under `objects/` as authoritative knowledge. Files under `migration-candidates/` are explicitly excluded from authoritative totals until separately accepted and promoted.

## Executive summary

The public site is operational, but the authoritative knowledge corpus is still small and early-stage:

- 5 authoritative concept objects;
- 10 claim records;
- 10 source records;
- 10 open uncertainty records;
- 6 perspective records;
- 13 relation records;
- 19 ecosystem entry-point groups;
- 0 concepts with completed review;
- 0 concepts with a populated `last_reviewed` date;
- all 5 concepts are `status: seed` and `review_state: unreviewed_seed`;
- no separate authoritative first-class evidence objects currently exist: the active v0.1 concept schema represents evidence through claims bound to sources and uncertainties.

The main completion gap is therefore no longer the website shell. It is corpus breadth, review maturity, and systematic evidence maintenance.

## Authoritative knowledge inventory

| Concept | Claims | Sources | Open uncertainties | Perspectives | Relations | Ecosystem groups | Status | Review state | Last reviewed |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| ADHD | 2 | 2 | 2 | 1 | 3 | 4 | seed | unreviewed_seed | missing |
| Autism | 2 | 2 | 2 | 1 | 3 | 4 | seed | unreviewed_seed | missing |
| Executive function | 2 | 2 | 2 | 1 | 3 | 4 | seed | unreviewed_seed | missing |
| Neurodiversity | 2 | 2 | 2 | 2 | 2 | 3 | seed | unreviewed_seed | missing |
| Sensory processing | 2 | 2 | 2 | 1 | 2 | 4 | seed | unreviewed_seed | missing |
| **Total** | **10** | **10** | **10** | **6** | **13** | **19** |  |  |  |

## Every authoritative claim, source, uncertainty and perspective

| Concept | Claims | Sources | Uncertainties | Perspectives |
|---|---|---|---|---|
| ADHD | `adhd-claim-1`, `adhd-claim-2` | `adhd-source-nimh`, `adhd-source-cdc` | `adhd-uncertainty-lifespan`, `adhd-uncertainty-equity` | `adhd-perspective-developmental` |
| Autism | `autism-claim-1`, `autism-claim-2` | `autism-source-who`, `autism-source-neurobiology` | `autism-uncertainty-measurement`, `autism-uncertainty-sensory` | `autism-perspective-clinical` |
| Executive function | `executive-function-claim-1`, `executive-function-claim-2` | `executive-function-source-miyake`, `executive-function-source-karr` | `executive-function-uncertainty-model`, `executive-function-uncertainty-ecology` | `executive-function-perspective-unity-diversity` |
| Neurodiversity | `neurodiversity-claim-1`, `neurodiversity-claim-2` | `neurodiversity-source-singer`, `neurodiversity-source-botha` | `neurodiversity-uncertainty-origins`, `neurodiversity-uncertainty-boundaries` | `neurodiversity-perspective-paradigm`, `neurodiversity-perspective-collective` |
| Sensory processing | `sensory-processing-claim-1`, `sensory-processing-claim-2` | `sensory-processing-source-dunn`, `sensory-processing-source-autism` | `sensory-processing-uncertainty-construct`, `sensory-processing-uncertainty-intervention` | `sensory-processing-perspective-person-environment` |

## Source-type inventory

| Source kind | Count | Current use |
|---|---:|---|
| peer reviewed | 6 | Autism, executive function, neurodiversity, sensory processing |
| authoritative guidance | 3 | ADHD and autism |
| historical | 1 | Neurodiversity |

Current claim-confidence distribution:

- high: 3 claims;
- moderate: 6 claims;
- contested: 1 claim.

## Public surface inventory

### Canonical indexed reading routes

| Route | Purpose | State |
|---|---|---|
| `/` | Homepage / entry questions | present and live-verified |
| `/understand/` | Browse current concepts | present and live-verified |
| `/understand/neurodiversity/` | Concept page | present and live-verified |
| `/understand/autism/` | Concept page | present and live-verified |
| `/understand/adhd/` | Concept page | present and live-verified |
| `/understand/executive-function/` | Concept page | present and live-verified |
| `/understand/sensory-processing/` | Concept page | present and live-verified |
| `/how-it-works/` | Evidence/provenance explanation | present and live-verified |
| `/about/` | About ND Oracle | present and live-verified |
| `/accessibility/` | Accessibility statement | present and live-verified |
| `/privacy/` | Privacy statement | present and live-verified |

### Compatibility and metadata surfaces

| Route / resource | State |
|---|---|
| `/tools/` | present, compatibility route, `noindex, follow` |
| `/games/` | present, compatibility route, `noindex, follow` |
| `/resources/` | present, compatibility route, `noindex, follow` |
| `/community/` | present, compatibility route, `noindex, follow` |
| `/oracle/` | present, compatibility route, `noindex, follow` |
| unknown-route 404 | present, real HTTP 404, noindex |
| `/robots.txt` | present; site block preserved with Cloudflare-managed crawler/content-signal augmentation |
| `/sitemap.xml` | present; exact canonical public URL set |
| `www.ndoracle.org` | redirects to HTTPS apex while preserving path and query |

### Deliberately absent standalone public routes

The current site does not expose separate routes for individual claims/evidence records, uncertainties, perspectives, sources or provenance records. These are rendered inside concept pages instead. At the current five-concept scale this is a coherent design choice, not a broken route. It should be reconsidered when the corpus becomes large enough that cross-concept evidence browsing is useful.

There is also no public search route yet. With only five concepts, browsing remains sufficient.

## Candidate material excluded from authoritative totals

`migration-candidates/autism-neurodiversity/` contains schema experiments, migration state, owner-decision records, evidence-date work, relation-semantics work, Singer edition research and other candidate material. None of it is counted above merely because it exists in the repository.

This distinction matters because the repository currently contains materially more research and migration machinery than accepted public knowledge.

## Completion gaps exposed by this inventory

1. **Breadth:** only five concepts are authoritative and public.
2. **Review maturity:** all five remain unreviewed seeds.
3. **Review dates:** every `last_reviewed` field is null.
4. **Community review:** provenance on all five explicitly says no community review yet.
5. **Evidence architecture:** accepted v0.1 concept objects still embed claims/sources/uncertainties rather than using separate authoritative first-class evidence objects.
6. **Source diversity:** the corpus currently contains only ten source records and a narrow set of source types.
7. **Cross-cutting concepts:** many high-value lived-experience and support concepts are absent from the authoritative corpus.
8. **Maintenance system:** there is not yet a corpus-wide stale-evidence/re-review queue.

## Operational conclusion

The next expansion lane should work in batches and should measure progress by **accepted, reviewed concept coverage**, not by the number of research files, migration proofs or individual sources processed.

A sensible next batch is to define and rank missing concepts, then move several concepts through the same evidence/review pipeline together. This avoids returning to one-source-at-a-time work.
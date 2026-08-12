# ND Oracle whole-site content inventory v0.4

Status date: 2026-08-12

Review candidate base: `e665673556e5d32515896d0e2d29b15fb83f1f96`

This inventory describes the ten-topic corpus after the original five foundation concepts are brought through the same evidence/review discipline as Batch A.

## Corpus totals

| Measure | v0.3 | v0.4 candidate |
|---|---:|---:|
| Authoritative concepts | 10 | 10 |
| Claims | 27 | 36 |
| Sources | 32 | 47 |
| Open uncertainties | 28 | 38 |
| Perspectives | 11 | 21 |
| Relations | 23 | 26 |
| Ecosystem entry-point groups | 34 | 34 |
| Reviewed concepts | 5 | 10 |
| Concepts with `last_reviewed` | 5 | 10 |

No new public route is added by this review. The public surface remains ten concept pages; the change is evidence depth and review state, not breadth.

## Foundation Batch B

| Concept | Claims | Sources | Uncertainties | Perspectives | Relations | Review state |
|---|---:|---:|---:|---:|---:|---|
| Neurodiversity | 3 | 4 | 4 | 3 | 2 | editor_reviewed |
| Autism | 4 | 5 | 4 | 4 | 4 | editor_reviewed |
| ADHD | 4 | 5 | 4 | 3 | 4 | editor_reviewed |
| Executive function | 4 | 5 | 4 | 3 | 3 | editor_reviewed |
| Sensory processing | 4 | 6 | 4 | 3 | 3 | editor_reviewed |
| **Batch total** | **19** | **25** | **20** | **16** | **16** |  |

## Material repairs to the original seed corpus

- The old taxonomic `neurodiversity -> autism/ADHD` graph is removed. Neurodiversity relationships are now explicitly non-taxonomic ecosystem relations.
- Neurodiversity separates descriptive diversity from the paradigm/movement and preserves disagreement about disability, medicine and social explanation.
- Autism now combines current clinical guidance with evidence on heterogeneity, sensory experience, language preference and person-defined support; identity-first language is not universalised.
- ADHD now makes specialist multi-source assessment explicit and rejects rating scales or executive-function tests as standalone diagnosis.
- Executive function now distinguishes construct, factor model, laboratory measurement and real-world prediction, and treats EF differences as transdiagnostic rather than condition-specific signatures.
- Sensory processing is no longer given `sensory integration` or `sensory modulation` as exact aliases. Current cross-diagnostic evidence and the mixed, outcome-specific sensory-intervention evidence are represented explicitly.

## Preserved uncertainty

All five reviewed objects retain open questions rather than converting evidence gaps into conclusions. Important unresolved areas include representation of people with high support needs, inequity in ADHD recognition, ecological validity of executive-function measures, cross-disciplinary sensory constructs, and which supports improve person-defined outcomes with acceptable burden or harm.

## Promotion provenance

The five pre-promotion Batch B objects are preserved under `migration-candidates/foundation-review-batch-b/candidates/`. Each authoritative object records the exact preserved candidate blob from which its semantics were promoted. Promotion changes lifecycle/provenance only; regression tests require semantic equality between each preserved candidate and its authoritative reviewed counterpart.

## Completion meaning

If this candidate passes repository validation and is merged, all ten public ND Oracle concepts will have:

- `status: reviewed`;
- `provenance.review_state: editor_reviewed`;
- a non-null `last_reviewed` date;
- claim/source/uncertainty/perspective link validation;
- explicit review debt retained as open uncertainties rather than hidden in lifecycle metadata.

This does not mean the knowledge base is final or exhaustive. It means the current ten-topic corpus has crossed the same minimum evidence/review gate.

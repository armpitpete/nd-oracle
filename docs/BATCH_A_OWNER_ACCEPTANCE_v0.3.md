# ND Oracle Batch A owner acceptance v0.3

Accepted: 2026-08-12

Accepted against protected `main`: `46366ea5d14f2832e7df3a48c320719c6475376e`

This record freezes the exact five candidate concept blobs accepted by the owner after the Batch A evidence, terminology and editorial review lane.

| Concept | Accepted candidate path | Accepted blob SHA |
|---|---|---|
| Dyslexia | `migration-candidates/topic-expansion-batch-a/candidates/dyslexia.json` | `6609a1a100919003b541e22559f51031ca202031` |
| Developmental co-ordination disorder | `migration-candidates/topic-expansion-batch-a/candidates/developmental-coordination-disorder.json` | `885dbc3a8293c6fa615d3fcacf80fe8dc23802e1` |
| Tourette syndrome | `migration-candidates/topic-expansion-batch-a/candidates/tourette-syndrome.json` | `f49e8adfe9a2fecc92239c024a4ee17523aa2574` |
| Learning disability | `migration-candidates/topic-expansion-batch-a/candidates/learning-disability.json` | `a06995d02e7acf4022ff31069ea5bc7fc6da68fe` |
| Developmental language disorder | `migration-candidates/topic-expansion-batch-a/candidates/developmental-language-disorder.json` | `fc99e429d6464523b12e5aa8af804fe5523d20a1` |

## Accepted public positions

The owner accepted the following editorial positions in ordinary language:

1. **Dyslexia** — centre the definition on persistent word-reading and/or spelling difficulty; reject IQ-discrepancy gatekeeping; keep wider reported difficulties visible without declaring them all core dyslexia traits.
2. **Developmental co-ordination disorder (DCD)** — use DCD as the precise concept name; explain that `dyspraxia` is broader in UK use; focus on motor coordination, daily participation and lifespan effects rather than generic `clumsiness`.
3. **Tourette syndrome** — explain motor and vocal tics over time; explicitly reject swearing as a defining requirement; represent common co-occurrence and person-defined support priorities without assuming every tic needs treatment.
4. **Learning disability** — use the UK NHS meaning; distinguish it clearly from specific learning difficulties such as dyslexia; explain related international terminology without treating the labels as universally interchangeable; do not infer communication, independence or decision-making capacity from diagnosis alone.
5. **Developmental language disorder (DLD)** — explain persistent developmental language difficulty with everyday impact; state that multilingualism does not cause DLD; make the CATALISE framing explicit while preserving international terminology uncertainty.

The owner also accepted the graph rule that none of these concepts is to be asserted as a taxonomic child of `neurodiversity`. Evidence-backed associations may be represented with more precise relation types.

## Promotion rule

Promotion may change only lifecycle/provenance fields and wording that is mechanically necessary because an item is no longer a candidate (for example, replacing `candidate concepts` with `concepts`). It must not silently strengthen or weaken accepted claims, scope boundaries, uncertainties, perspectives or evidence routes.

The accepted candidate files remain in `migration-candidates/` as the immutable pre-promotion comparison source.

## Authority boundary

This acceptance authorises preparation of authoritative concept objects and a ten-topic public-site release candidate.

It does **not** by itself authorise:

- bypassing repository validation;
- deleting or rewriting the accepted candidate history;
- changing the accepted substantive positions without a new evidence/review cycle;
- merging a protected promotion PR without the repository's normal protected gate;
- deploying or publishing a new production release without the production release gate.

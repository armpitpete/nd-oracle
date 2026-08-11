# Autism v0.1 → v0.2 deterministic migration proof

**Status:** blocked pending owner decision  
**Proof scope:** non-authoritative migration analysis only  
**Source repository main:** `30b278cdbc4277f206b30c2c665f3d2a2b641983`  
**Authoritative source:** `objects/concepts/autism.json`  
**Source Git blob:** `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`  
**Target contract:** ND Oracle schema v0.2

## Purpose

Test the accepted staged-migration assumption against one existing v0.1 concept without changing the authoritative object.

This proof asks a strict question:

> Can Autism be transformed from the current v0.1 object into a schema-valid v0.2 representation by deterministic, provenance-preserving transformation alone?

The answer is **no under the current contract**.

That is a proof result, not a request to relax preservation requirements.

## Protected boundary

This branch does **not**:

- modify `objects/concepts/autism.json`;
- migrate any authoritative object;
- alter any existing claim ID or claim wording;
- add new authoritative neurodiversity knowledge;
- research or invent missing evidence-contribution semantics;
- deploy anything.

The machine-readable manifest is `docs/migration-proofs/autism-v0.1-to-v0.2.json`.

## Preservation accounting

The existing `v01_preservation_inventory()` contract emits **34 preservation units** for Autism.

The manifest classifies **all 34**. No preservation unit is unaccounted for.

Safe deterministic mappings include:

- object ID;
- aliases;
- summary;
- included/excluded scope;
- both claim IDs;
- exact claim wording;
- claim confidence;
- provenance and review state;
- claim → uncertainty routes, retained as local uncertainty rather than automatically promoted to standalone Questions.

The proof deliberately does not treat “accounted for” as “migratable”. A unit may be accounted for by an explicit unresolved mapping.

## Blocking findings

| ID | Finding | Why it blocks a lossless one-concept candidate |
|---|---|---|
| `evidence-contribution-semantics` | v0.1 source routes say which source supports which claim, but do not encode v0.2 contribution role, finding, population/context or methodology. | Filling those fields would require fresh evidential interpretation, not deterministic migration. |
| `evidence-required-metadata` | v0.2 Evidence requires structured title, date and authorship. v0.1 does not consistently provide those as structured values. | A mechanical converter must either enrich from external sources or use a transitional compatibility rule. |
| `perspective-required-fields` | v0.2 Perspective requires `held_by.scope`, reasoning, scope and disagreement references absent from v0.1. | Inventing values would alter meaning; omitting them fails schema. |
| `cross-version-structural-reciprocity` | Autism has `narrower_than → neurodiversity`. The v0.2 validator checks for a v0.2-shaped reciprocal `broader_than`. Neurodiversity remains v0.1 in a one-concept migration. | The accepted “one concept first” staged migration cannot validate this preserved structural relation as currently implemented. |
| `ecosystem-entry-successor` | v0.2 Concept has no `ecosystem_entry_points` field. | Dropping four entries loses knowledge; automatically turning their questions into Question objects is explicitly prohibited. |

## Owner-review findings

Three additional transformations are plausible but are not mechanical facts:

1. **`related_to` → `associated_with`** — v0.2 has no exact `related_to` token. This needs an accepted semantic mapping rule.
2. **Uncertainty reduction conditions** — v0.1 stores `what_would_reduce_it` as a list; v0.2 stores one `reopening_or_reduction_condition` string. A deterministic lossless encoding needs to be chosen.
3. **Migration unit size** — migrating Neurodiversity alongside Autism could solve the structural inverse shape for that relation, but it does not solve the Evidence, Perspective or ecosystem-entry blockers.

## Falsification result

The migration-plan assumption that one authoritative concept can be converted first has been **falsified under the current v0.2 contract** for Autism.

A schema-valid candidate cannot be produced solely by rearranging existing Autism data. Doing so would require at least one of:

- new evidential interpretation;
- new source metadata enrichment;
- invented Perspective fields;
- dropping ecosystem knowledge;
- weakening relation preservation; or
- changing staged-migration compatibility rules.

Each would cross a protected semantic boundary.

## Next protected decision

Before any authoritative migration candidate is prepared, choose the migration policy for the blockers above.

The narrowest route is to define a **transitional migration-compatibility contract** that preserves legacy information without pretending missing v0.2 semantics already exist. Any such change should be reviewed as schema/validator governance, not smuggled into the Autism migration.

Broader alternatives are to revise the v0.2 required fields or broaden the first migration unit, but neither should happen implicitly.

Until that decision is accepted:

> **Autism remains authoritative v0.1 and unchanged.**

# D15 — Embedded Uncertainty Lossless Representation Policy

Status: **owner policy direction accepted; implementation not authorised**.

Accepted on 2026-08-11 against protected repository `main`:

`a9bed79b827f6308cbaa8f2a11edda1b9c5d3da8`

Owner acceptance:

> Accept `nd-embedded-uncertainty-lossless-representation`: accept the native lossless embedded-Uncertainty policy direction — preserve one legacy uncertainty as one embedded uncertainty by default, preserve multiple reduction/reopening routes as distinct items, preserve lifecycle state explicitly, and avoid forced question-to-statement conversion; leave exact schema syntax for a separately reviewed implementation candidate.

## Source decision candidate

The accepted policy supersedes only the owner-decision candidate in:

`migration-candidates/autism-neurodiversity/uncertainty-shape-research.json`

Decision candidate:

`nd-embedded-uncertainty-lossless-representation`

The merged research record remains unchanged as a historical pre-D15 snapshot. Its `owner_decision_required` state describes the research state at the time it was prepared and is not rewritten retrospectively.

## Accepted policy direction

D15 accepts these principles:

1. One v0.1 legacy uncertainty remains one embedded uncertainty by default.
2. Multiple `what_would_reduce_it` routes remain distinct rather than being flattened into one prose string.
3. Uncertainty lifecycle state remains explicit rather than being discarded during migration.
4. Legacy interrogative uncertainty wording may remain verbatim; migration must not pretend a question has become a declarative statement merely to satisfy a field name.
5. Promotion to a standalone Question remains an explicit, separately justified semantic act rather than an automatic migration rule.

## What D15 does not decide

D15 does **not** select:

- exact v0.2 field names;
- a plural-array versus compatibility-union implementation;
- the final embedded-Uncertainty lifecycle vocabulary;
- mappings for `partially_resolved` or `none_identified`;
- any specific current uncertainty for standalone Question promotion.

These remain implementation or later semantic decisions.

## Current implementation boundary

The implemented `schema/common-v0.2.json` remains unchanged. It still uses a single `reopening_or_reduction_condition` string and has no embedded-Uncertainty `status` field.

Therefore D15 changes policy state, not schema state. The Autism/Neurodiversity migration remains blocked from authoritative replacement until a separately reviewed implementation candidate can satisfy D15 without fabricating or dropping semantics.

## Explicit non-authorisations

D15 does **not** authorise:

- schema mutation;
- validator mutation;
- authoritative v0.1 object mutation;
- authoritative v0.2 replacement;
- automatic Question promotion;
- splitting one legacy uncertainty into several records;
- flattening multiple reduction routes into one prose string;
- inventing or remapping lifecycle status;
- publication or deployment.

## Candidate-state consequence

The paired candidate now records the Autism and Neurodiversity uncertainty blockers as:

`accepted_policy_schema_implementation_pending`

This means the owner-level policy ambiguity is resolved, but the implementation gate is still closed.

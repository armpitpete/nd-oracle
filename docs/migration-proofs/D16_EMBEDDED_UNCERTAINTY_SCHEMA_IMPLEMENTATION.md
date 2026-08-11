# D16 — Embedded Uncertainty Schema Implementation

Status: **owner exact implementation accepted; authoritative migration not authorised**.

Accepted on 2026-08-11 against protected repository `main`:

`1bc63e07c7da026d2a2cba36bb05eb72980e7f19`

Owner acceptance:

> Accept `nd-embedded-uncertainty-schema-implementation`: accept the exact D15 embedded-Uncertainty schema implementation candidate — neutral `text`, canonical plural `reopening_or_reduction_conditions` preserving order and duplicates, direct legacy status vocabulary with identity-only mapping, and no compatibility union.

## Candidate superseded by D16

D16 accepts the exact implementation candidate recorded in:

`migration-candidates/autism-neurodiversity/embedded-uncertainty-schema-implementation-candidate.json`

Decision candidate:

`nd-embedded-uncertainty-schema-implementation`

The earlier D15 policy record and pre-D15 research remain historical snapshots and are not rewritten retrospectively.

## Exact accepted schema shape

The v0.2 embedded Uncertainty record requires:

```yaml
id: local-uncertainty-id
text: "..."
why_it_matters: "..."
reopening_or_reduction_conditions:
  - "..."
status: open
```

Accepted details:

1. `text` is a neutral non-blank field and may preserve a legacy interrogative `question` verbatim.
2. `reopening_or_reduction_conditions` is the canonical plural representation.
3. The conditions array requires at least one non-blank item.
4. The conditions array does not require uniqueness, so schema-valid duplicate legacy entries remain preservable.
5. Array order remains source order.
6. Embedded uncertainty status vocabulary is exactly `open`, `partially_resolved`, and `none_identified`.
7. Legacy status mapping is identity-only; no semantic remapping is accepted.
8. The superseded `statement` plus singular `reopening_or_reduction_condition` shape is not retained through a compatibility union.

## Deterministic v0.1 mapping

D16 accepts the following mechanical mapping for embedded uncertainties:

- `id` → `id` verbatim;
- `question` → `text` verbatim;
- `why_it_matters` → `why_it_matters` verbatim;
- `what_would_reduce_it` → `reopening_or_reduction_conditions` as the same ordered array;
- `status` → `status` verbatim;
- one legacy uncertainty remains one embedded uncertainty.

No standalone Question is created automatically.

## Why no compatibility union

There are currently no authoritative v0.2 knowledge objects depending on the superseded embedded-Uncertainty shape. Keeping both shapes valid would preserve only transient fixture history while making two structurally different uncertainty records canonical under the same schema version.

Historical schema/research state remains inspectable in the preserved research and proof files instead.

## Authorised by D16

D16 authorises the exact schema and schema-driven validation behaviour contained in PR #54 for this embedded-Uncertainty implementation.

## Explicit non-authorisations

D16 does **not** authorise:

- mutation of any authoritative v0.1 object;
- authoritative v0.2 replacement;
- automatic Question promotion;
- splitting one uncertainty into several records;
- flattening plural reduction routes;
- status remapping;
- new embedded-Uncertainty lifecycle meanings;
- publication or deployment.

## Paired-candidate consequence

The Autism and Neurodiversity uncertainty-shape entries move from:

`accepted_policy_schema_implementation_pending`

to:

`accepted_schema_implementation`

This resolves the schema-level uncertainty-shape blocker. Other independent blockers remain, including structural confidence and the separate Neurodiversity → ADHD structural dependency.

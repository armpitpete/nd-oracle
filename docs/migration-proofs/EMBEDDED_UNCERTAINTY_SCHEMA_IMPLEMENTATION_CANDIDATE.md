# Embedded Uncertainty Schema Implementation Candidate

Status: **separately reviewable implementation candidate; owner acceptance required**.

Prepared on 2026-08-11 against protected `main`:

`1bc63e07c7da026d2a2cba36bb05eb72980e7f19`

Governing accepted policy:

`d15-embedded-uncertainty-lossless-representation`

## Purpose

Implement the D15 lossless embedded-Uncertainty policy in the v0.2 schema without migrating authoritative knowledge or inventing semantic mappings.

The pre-candidate v0.2 uncertainty shape required:

```yaml
id: ...
statement: ...
why_it_matters: ...
reopening_or_reduction_condition: ...
```

That shape cannot preserve a v0.1 uncertainty's plural `what_would_reduce_it` list or lifecycle `status` directly, and `statement` implies a declarative form that is not neutral for legacy interrogative wording.

## Exact candidate shape

```yaml
id: stable-local-id
text: "Could this remain unresolved in another context?"
why_it_matters: "..."
reopening_or_reduction_conditions:
  - "First distinct route."
  - "Second distinct route."
status: open
```

Required fields are exactly:

- `id`
- `text`
- `why_it_matters`
- `reopening_or_reduction_conditions`
- `status`

### Neutral text

`text` is deliberately neutral between interrogative and declarative wording. A v0.1 `question` may therefore be copied verbatim without pretending that its grammatical or epistemic form changed.

### Plural conditions

`reopening_or_reduction_conditions` is an array with `minItems: 1` and non-blank string items.

The candidate deliberately does **not** use `uniqueItems: true`. The v0.1 schema does not prohibit duplicate list entries. Lossless migration must therefore be able to preserve both original order and any duplicates rather than silently normalising them.

### Lifecycle status

The embedded-Uncertainty status vocabulary is exactly the v0.1 uncertainty vocabulary:

- `open`
- `partially_resolved`
- `none_identified`

Migration is identity-only. This candidate does not reinterpret, collapse, rename, or infer statuses and does not add new embedded-Uncertainty lifecycle meanings.

## Deterministic v0.1 mapping

The candidate mapping is mechanical:

| v0.1 | v0.2 candidate |
|---|---|
| `id` | `id` verbatim |
| `question` | `text` verbatim |
| `why_it_matters` | `why_it_matters` verbatim |
| `what_would_reduce_it` | `reopening_or_reduction_conditions` as the same ordered array |
| `status` | `status` verbatim |

One legacy uncertainty remains one embedded uncertainty. No standalone Question is created automatically.

## Compatibility choice

The candidate uses **one canonical plural shape only**. It does not retain a union accepting the superseded `statement` plus single-string condition shape.

Reason: there are no authoritative v0.2 objects. Keeping both shapes would preserve only test-fixture history while making two representations valid inside the same schema. Historical research and proof files remain intact instead of being rewritten.

Schema version remains `0.2` because v0.2 is still in its compatibility/implementation-candidate phase and no authoritative v0.2 object depends on the superseded embedded shape.

## Proof obligations

Before owner review, the candidate must demonstrate:

1. all current authoritative v0.1 uncertainties map mechanically to the candidate record without changing text, list order, list entries, lifecycle state, or record count;
2. an interrogative `text` value validates;
3. multiple distinct reopening/reduction conditions validate as separate items;
4. all three schema-valid v0.1 status values validate without remapping;
5. the old single-string v0.2 uncertainty shape fails closed;
6. the full v0.2 fixture graph still validates;
7. all five authoritative v0.1 objects remain byte-identical;
8. prior research/proof snapshots remain historical rather than being rewritten.

## Explicit boundaries

This candidate does **not** authorise or perform:

- authoritative v0.1 object mutation;
- authoritative v0.2 replacement;
- automatic Question promotion;
- splitting one legacy uncertainty into multiple records;
- flattening plural conditions into prose;
- lifecycle status remapping;
- new lifecycle semantics;
- publication or deployment.

## Owner decision candidate

`nd-embedded-uncertainty-schema-implementation`

Recommended acceptance, if the exact implementation and validation hold:

> Accept the exact D15 embedded-Uncertainty schema implementation candidate: neutral `text`, canonical plural `reopening_or_reduction_conditions` preserving order and duplicates, direct legacy status vocabulary with identity-only mapping, and no compatibility union.

Acceptance should then be recorded as a new owner decision against the unchanged protected base before any guarded merge.

# Evidence date precision implementation

Status: **implementation candidate; owner review required**

Prepared against protected `main`:

`befc0a120f876850bfef5d91d4fcfc2e9cb8cf94`

Accepted design source: PR #61, **Design precision-aware Evidence publication dates**.

## Scope

This candidate implements the accepted publication/source date representation for v0.2 Evidence objects without migrating or mutating authoritative v0.1 knowledge.

The contract is:

```json
"date": "2016",
"date_precision": "year"
```

with allowed precision values:

- `year` — `YYYY`;
- `month` — `YYYY-MM` with a valid calendar month;
- `day` — full calendar date validated by JSON Schema `format: date`.

`date` remains a string. `accessed` remains an exact full date.

## Implementation

`schema/types/evidence-v0.2.json` now requires `date_precision` and validates the `date` value against the declared precision using JSON Schema conditionals.

No custom date-normalisation code is added to `scripts/validate.py`. The repository validator already loads the v0.2 Evidence schema with JSON Schema format checking, so keeping the rule in the schema avoids a second temporal authority.

The existing exact synthetic Evidence fixture keeps its original `date` value `2026-08-11` and gains only:

```json
"date_precision": "day"
```

The human-readable v0.2 schema contract is updated to state the same rule.

## Required proof

Dedicated tests cover:

1. `2016` + `year` validates;
2. `2016-07` + `month` validates;
3. `2016-07-03` + `day` validates;
4. the existing exact fixture date remains textually unchanged;
5. precision/value mismatches fail closed;
6. invalid months fail;
7. invalid full dates fail;
8. missing or unrecognised `date_precision` fails;
9. `accessed` still requires a full date;
10. the authoritative object count remains five and the fixture graph validates;
11. the Singer-required year-only shape can validate without storing `2016-07-03` as the source date.

## Singer 2016 consequence

This implementation makes the following future Evidence representation possible:

```json
"date": "2016",
"date_precision": "year"
```

It does **not** create or mutate the Singer Evidence object in this PR, and it does not accept `2016-07-03` as an exact publication fact.

The day-level value remains research metadata unless stronger evidence establishes it to the required standard.

## Boundaries

This implementation candidate does not authorise:

- authoritative v0.1 mutation;
- authoritative v0.2 migration or replacement;
- creation or mutation of the Singer 2016 Evidence object;
- acceptance of `2016-07-03` as an exact Singer publication date;
- Singer 2017 changes;
- new Evidence Contribution bindings;
- merge of PR #60;
- ADHD migration or Neurodiversity↔ADHD semantic disposition;
- publication or deployment.

## Protected review question

If exact-head validation passes, owner review should decide whether this implementation faithfully realises the already accepted PR #61 design. Acceptance of this implementation would authorise integration of the schema repair only; later Singer migration remains a separate protected action.

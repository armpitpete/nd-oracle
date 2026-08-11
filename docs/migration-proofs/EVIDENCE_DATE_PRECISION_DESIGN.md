# Evidence date precision design

Status: **design only; owner decision required; no schema change authorised**

Prepared against protected `main`:

`622da858f5803be32f409a54f7e0c6742f19e373`

Related unresolved research: PR #60, Singer 2016 Kindle publication date.

## Problem

The current v0.2 Evidence schema requires `date` to be a JSON Schema `format: date` string. That can represent a known day such as `2017-09-05`, but it cannot faithfully represent a source whose publication year is known while its month or day is unresolved.

For the Singer 2016 Kindle edition, the evidence strongly supports publication in **2016** and identifies ASIN `B01HY0QTEE`. `2016-07-03` remains the best day-level candidate, but current evidence is insufficient to place that date unqualified in the v0.2 `date` field.

The modelling requirement is therefore general:

> Store only the date precision the evidence actually establishes. Never manufacture missing month/day components merely to satisfy validation.

## Design goals

A precision-aware date representation should:

1. preserve exact existing dates without changing their textual value;
2. represent year-only and month-only bibliographic dates without false precision;
3. make the stored precision explicit and machine-checkable;
4. reject mismatches between the declared precision and the date string;
5. keep `accessed` as an exact full date because access is an event ND Oracle can record directly;
6. avoid mixing date precision with evidential confidence;
7. avoid encoding speculative day-level candidates inside authoritative Evidence objects;
8. remain bounded to bibliographic/source dates rather than becoming a general temporal-uncertainty system.

## Candidate representations considered

### A. Structured date object

Example:

```json
"date": {
  "value": "2016",
  "precision": "year"
}
```

This is explicit, but it changes the type and shape of every existing exact date. It creates unnecessary migration and consumer churn for a problem that can be solved additively.

**Disposition: not preferred.**

### B. String value plus explicit precision

Example:

```json
"date": "2016",
"date_precision": "year"
```

Exact-date example:

```json
"date": "2017-09-05",
"date_precision": "day"
```

This keeps `date` a string, preserves every existing exact date value verbatim, and makes reduced precision explicit.

**Disposition: preferred design.**

### C. Keep exact-only `date` and add fallback fields

Examples include `publication_year`, nullable `date`, sentinel dates such as `2016-01-01`, or parallel candidate-date fields.

These create duplicate temporal authorities, invite disagreement between fields, or encode invented precision.

**Disposition: reject.**

## Preferred contract

If accepted for implementation, Evidence should require both:

- `date`
- `date_precision`

Allowed precision values:

- `year`
- `month`
- `day`

The value must match the declared precision:

| `date_precision` | required `date` shape | example |
|---|---|---|
| `year` | `YYYY` | `2016` |
| `month` | `YYYY-MM` | `2016-07` |
| `day` | full calendar date | `2016-07-03` |

Validation must fail closed on mismatches such as:

- `date: "2016-07-03"` with `date_precision: "year"`;
- `date: "2016"` with `date_precision: "day"`;
- invalid months such as `2016-13`;
- invalid full dates such as `2016-02-30`.

For `day`, the existing JSON Schema `format: date` validation should remain in force. For `month` and `year`, bounded patterns should be used.

## Precision is not confidence

`date_precision` answers **how much of the calendar date is established**, not **how trustworthy the evidence is**.

A separate `date_confidence` field is not proposed here. Adding one would create a second epistemic scoring mechanism without first defining what it means, how it is reviewed, or how it interacts with provenance.

If the stored year itself is uncertain, that is outside this design and requires a separate uncertainty decision. This candidate solves only known reduced precision.

## Singer 2016 representation

Under this design, the future Singer 2016 Kindle Evidence candidate would use:

```json
"date": "2016",
"date_precision": "year"
```

It would **not** use `2016-07-03` in the Evidence object unless stronger evidence later establishes that day to the required standard.

The day-level candidate may remain in the research/provenance record as a candidate. Candidate metadata must not silently become source-identity fact.

## Existing exact dates

Existing exact v0.2 Evidence fixture dates should keep their current `date` strings unchanged and gain:

```json
"date_precision": "day"
```

No exact date should be rewritten merely because the precision field is introduced.

## `accessed` remains exact

This design does not change `accessed`.

An access date records when ND Oracle or its research process accessed the source. That event can normally be recorded as a full date and does not have the same bibliographic precision problem.

## Schema-version consequence

The repository currently treats v0.2 as one schema-version meaning, and no authoritative knowledge object has yet migrated to v0.2. The v0.2 contract also already permits fixture-only semantic repair before authoritative migration rather than retaining superseded compatibility unions.

Therefore the preferred implementation direction is an **in-place v0.2 schema repair before authoritative v0.2 migration**, not a new v0.3 object model solely for this field. That implementation must still be separately reviewed and must update the v0.2 contract, Evidence schema, fixtures, validator expectations, and tests atomically.

This document does not itself authorise that implementation.

## Required implementation tests if accepted

A later implementation candidate should prove at least:

1. `2016` + `year` validates;
2. `2016-07` + `month` validates;
3. `2016-07-03` + `day` validates;
4. existing exact Evidence values remain textually unchanged;
5. precision/value mismatches fail;
6. invalid month values fail;
7. invalid day-level calendar dates fail;
8. missing `date_precision` fails for v0.2 Evidence;
9. `accessed` still requires a full date;
10. all authoritative v0.1 objects remain byte/semantic unchanged;
11. Singer 2016 can be represented as year-only without inserting `2016-07-03` into the Evidence source-identity field.

## Boundaries

Acceptance of this design would not authorise:

- mutation of `schema/types/evidence-v0.2.json`;
- mutation of `schema/common-v0.2.json`;
- validator changes;
- authoritative v0.1 mutation;
- authoritative v0.2 migration or replacement;
- acceptance of `2016-07-03` as an exact Singer publication fact;
- Singer 2017 changes;
- ADHD migration or Neurodiversity↔ADHD semantic disposition;
- publication or deployment;
- merge of PR #60.

## Recommended protected decision

> Accept the string-plus-explicit-precision design direction for Evidence publication dates: retain `date` as a string, add required `date_precision: year | month | day`, validate the value against the declared precision, keep `accessed` exact, and represent Singer 2016 as `date: "2016"` with `date_precision: "year"`. Treat implementation as a separately reviewed v0.2 schema-repair candidate; this acceptance does not itself authorise schema mutation or acceptance of `2016-07-03` as an exact fact.

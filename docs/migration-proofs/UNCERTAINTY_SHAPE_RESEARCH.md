# Embedded Uncertainty shape research

Date: 2026-08-11

Prepared against protected `main`:

`a95a7772f6ca69d2c5b58cbcdcc6240110cc9ce8`

Status: **non-authoritative research only; owner decision required before any schema-policy change**.

Machine-readable record:

`migration-candidates/autism-neurodiversity/uncertainty-shape-research.json`

## Question tested

How can a v0.1 uncertainty containing multiple distinct reduction conditions be represented in v0.2 without flattening, inventing semantics, misleadingly splitting one uncertainty into several, or automatically promoting it to a standalone Question?

## Repository-wide finding

This is not a Neurodiversity-only edge case.

All five authoritative v0.1 Concepts contain two uncertainties each. All ten current uncertainties:

- contain an explicit `status`;
- contain exactly three separate `what_would_reduce_it` items.

The implemented v0.2 embedded Uncertainty schema instead requires:

- `id`;
- `statement`;
- `why_it_matters`;
- one string-valued `reopening_or_reduction_condition`.

It has no embedded-Uncertainty `status` field.

Therefore the current v0.2 shape cannot natively preserve two structural properties present in every current authoritative v0.1 uncertainty: plural reduction routes and lifecycle state. The `question` -> `statement` field change also needs a semantic policy if exact interrogative wording is to be retained without category conversion.

This strengthens the existing migration blocker: solving only the list/string mismatch would still leave lifecycle state unrepresented.

## Source inventory

Authoritative source blobs remain unchanged:

- Autism: `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`;
- Neurodiversity: `5a38bc4250079412dd3f4da1d598dfcab984ca66`;
- ADHD: `719f26a9af773cd1bcf670df4d12ed5f6bcf0a23`;
- Executive function: `f67e1a73e89245f9e6c6c2a34d4acc47169b8273`;
- Sensory processing: `7626d61a2844aae88ce6811760dfe97b5baa94bc`.

Schema anchors:

- v0.1: `schema/object-v0.1.json` blob `44d8c210d5a02afb3b53b8d1774a4209d0fd856d`;
- v0.2 common: `schema/common-v0.2.json` blob `2c0fc2344fcafde88340b8a5882e0d171246ea02`;
- v0.2 Question: `schema/types/question-v0.2.json` blob `cfde12cfdd35360b17f69f7174eb1f10fdb99d6c`.

## Alternatives tested

### 1. Flatten the list into one string

**Reject as the default migration rule.**

Keeping all words does not preserve list structure or the relationship among the entries. Joining three routes can silently imply that all are required, any one is sufficient, they form a sequence, or they are merely examples. The migration compatibility contract already rejects prose joining as automatically lossless.

It also does nothing to preserve v0.1 uncertainty `status`.

### 2. Split one legacy uncertainty into several embedded uncertainties

**Reject without a separately reviewed semantic change.**

This changes one epistemic record into several, duplicates the question and `why_it_matters`, changes identity/grouping, and can imply that v0.1 asserted several distinct uncertainties rather than one uncertainty with several possible reduction routes.

### 3. Promote the uncertainty to a standalone Question

**Do not use as a general migration rule.**

Question and embedded Uncertainty are deliberately different mechanisms. Promotion requires an explicit decision that the issue is independently useful, reusable, or researchable. In addition, the v0.2 Question schema requires `current_understanding`, which is not supplied deterministically by the v0.1 uncertainty record.

A specific uncertainty may later qualify for Question promotion, but that is a separate semantic/evidential act.

### 4. Retain the legacy record unmapped

**Safe interim state.**

This is the correct fail-closed behaviour while the policy remains unresolved. It preserves all source information in the migration package but deliberately leaves authoritative v0.2 replacement blocked.

### 5. Native embedded-Uncertainty repair

**Recommended for owner review.**

Adopt a separately reviewed policy direction in which embedded Uncertainty can natively preserve:

- one legacy uncertainty as one embedded uncertainty by default;
- multiple reduction/reopening routes as distinct items;
- lifecycle state explicitly;
- neutral uncertainty text capable of retaining interrogative legacy wording verbatim;
- explicit rather than automatic Question promotion.

This is the only assessed direction that addresses the repository-wide incompatibility without object-specific encoding tricks.

## Important dissent / reopening points

The recommendation does **not** establish the final schema syntax.

Serious alternatives remain at implementation level:

- canonical plural-array fields versus a transitional compatibility union;
- exact naming for uncertainty text and reduction/reopening routes;
- lifecycle vocabulary;
- how, if at all, `partially_resolved` and `none_identified` should map into a later vocabulary;
- whether individual current uncertainties qualify independently for standalone Question promotion.

Those issues should remain open after the policy-level decision rather than being hidden inside it.

## Decision candidate

`nd-embedded-uncertainty-lossless-representation`

Recommended owner decision:

> Accept the native lossless embedded-Uncertainty policy direction: preserve one legacy uncertainty as one embedded uncertainty by default, preserve multiple reduction/reopening routes as distinct items, preserve lifecycle state explicitly, and avoid forced question-to-statement conversion; leave exact schema syntax for a separately reviewed implementation candidate.

Acceptance would authorise **only the policy direction**.

It would **not** authorise:

- schema mutation;
- validator mutation;
- authoritative v0.1 mutation;
- authoritative v0.2 replacement;
- automatic Question promotion;
- uncertainty splitting;
- list flattening;
- status remapping;
- publication or deployment.

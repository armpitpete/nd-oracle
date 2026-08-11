# D13 — Singer edition-specific Contribution bindings

Date: 2026-08-11

Prepared against protected `main`:

`84087c7a86f0efda4db6fc1f0ff29c468dab82e8`

## Owner decision

Accepted:

> Accept `nd-singer-edition-specific-contribution-bindings`: accept the edition-specific `compatible` Evidence Contribution bindings for 2016 Kindle → Neurodiversity Claim 1, 2017 revised print → Claim 1, and 2017 revised print → Claim 2. Keep 2016 Kindle → Claim 2 pending stronger direct-text evidence. Do not copy Claim support automatically between editions, and preserve authoritative v0.1 unchanged.

Decision ID:

`d13-singer-edition-specific-contribution-bindings`

## Accepted bindings

The following future non-authoritative binding candidates are accepted:

1. `neurodiversity-source-singer-2016-kindle` → `neurodiversity#neurodiversity-claim-1` — role `compatible`.
2. `neurodiversity-source-singer-2017-revised-print` → `neurodiversity#neurodiversity-claim-1` — role `compatible`.
3. `neurodiversity-source-singer-2017-revised-print` → `neurodiversity#neurodiversity-claim-2` — role `compatible`.

## Explicitly pending

`neurodiversity-source-singer-2016-kindle` → `neurodiversity#neurodiversity-claim-2` remains pending stronger direct-edition text evidence.

Its proposed role remains `compatible`, but D13 does not accept that binding.

## Representation boundary

D13 accepts the edition-specific binding and role only. It does not manufacture a complete v0.2 Evidence Contribution record. Required fields such as claim-specific finding, population/context, methodology and limitations remain governed by the evidence record and must not be invented merely to satisfy schema.

Automatic cross-edition Claim-support copying remains forbidden.

## Preservation checks

- Authoritative `objects/concepts/neurodiversity.json` remains byte-identical at blob `5a38bc4250079412dd3f4da1d598dfcab984ca66`.
- `singer-edition-enrichment-research.json` remains the historical research-time snapshot and is not rewritten to make its former owner-review statuses appear retroactively accepted.
- The 2016 full date remains unresolved.
- No authoritative Evidence or Evidence Contribution object is created.
- No schema or validator change is authorised.
- No publication or deployment is authorised.

## Still unresolved

- 2016 Kindle full schema-valid publication date.
- 2016 Kindle → Claim 2 binding pending stronger direct text.
- Neurodiversity and Autism list-valued uncertainty representation.
- D6 structural relation confidence.
- Neurodiversity `broader_than -> adhd` structural dependency.
- Authoritative v0.2 replacement.

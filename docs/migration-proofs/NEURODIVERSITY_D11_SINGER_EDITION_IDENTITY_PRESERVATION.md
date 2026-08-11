# Neurodiversity D11 — Singer edition identity preservation

Status: **owner acceptance recorded; non-authoritative migration decision only**

Accepted against protected `main`:

`ae12681b8fb0d84348bda2347d805d8e44d2165c`

## Owner decision

D11 accepts the following bounded rule:

> Treat the legacy `neurodiversity-source-singer` record as conflating two identifiable editions. For future non-authoritative v0.2 migration work, preserve separate Evidence identity candidates for the 2016 Kindle edition and the revised 2017 print edition rather than selecting or combining them. Preserve the authoritative v0.1 source unchanged. Do not duplicate Claim-support semantics automatically; each Evidence Contribution must remain tied to evidence that the relevant content exists in that edition.

## Accepted identity split

Future non-authoritative migration work therefore preserves two separate candidate identities:

- `neurodiversity-source-singer-2016-kindle` — 2016 Kindle edition;
- `neurodiversity-source-singer-2017-revised-print` — revised 2017 print edition.

The split is recorded in:

`migration-candidates/autism-neurodiversity/singer-edition-candidates.json`

D11 does **not** select one edition as the canonical replacement for the other and does **not** combine the editions into one synthetic Evidence record.

## Claim-support boundary

The legacy v0.1 source carries Claim-support routing at the source-record level. D11 does not automatically copy those routes onto both future Evidence identity candidates.

Each future Evidence Contribution remains separately blocked until evidence establishes that the cited finding, methodology or relevant content is present in that specific edition.

This prevents a migration convenience rule from turning edition identity into unsupported evidential equivalence.

## Bibliographic boundary

D11 accepts the edition distinction represented by the years and formats in the owner decision: 2016 Kindle and revised 2017 print.

It does not independently accept every bibliographic field previously discussed during research. In particular, a full v0.2 schema-valid publication date remains an enrichment field unless separately evidenced and recorded. The candidate file therefore marks full schema dates as `not_accepted_by_d11`.

## Historical record preservation

The following remain unchanged:

- authoritative `objects/concepts/neurodiversity.json`;
- authoritative Neurodiversity blob `5a38bc4250079412dd3f4da1d598dfcab984ca66`;
- `neurodiversity-enrichment-research.json` as the historical research snapshot, including its former `owner_decision_required` state for Singer edition reconciliation.

D11 supersedes the research decision candidate through the owner-decision ledger rather than rewriting the historical proposal state.

## Still unresolved

D11 does not resolve:

- edition-specific Evidence Contribution assignment;
- full schema-valid date enrichment for either Singer candidate;
- Neurodiversity list-valued uncertainty representation;
- Autism list-valued uncertainty representation already deferred under D3;
- structural confidence under D6;
- Neurodiversity `broader_than -> adhd` structural dependency;
- authoritative v0.2 replacement;
- publication or deployment.

## Regression requirements

Tests must prove that:

1. D11 is bound to exact protected base `ae12681b8fb0d84348bda2347d805d8e44d2165c`;
2. two distinct non-authoritative Singer Evidence identity candidates exist;
3. neither single-edition selection nor edition combination is authorised;
4. Claim-support duplication is explicitly false;
5. each candidate requires edition-specific evidence before Contributions can be assigned;
6. the authoritative Neurodiversity blob remains unchanged;
7. the historical research snapshot remains unchanged;
8. unrelated uncertainty, structural-confidence and ADHD blockers remain open.

No authoritative mutation, replacement, schema change, publication or deployment is authorised by D11.

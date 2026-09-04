# UK Reference Baseline v1

Date: 2026-09-04

## Status

**FROZEN CONTENT BASELINE**

This record freezes the bounded UK-first ND Oracle reference corpus after completion of the UK breadth and Organisations & peer community slices.

The frozen governed-content snapshot is:

- source commit: `802e69b4437a276c234a036d9cd8f3f58f582b71`
- source tree: `8cf57114836ba4e5443d5bae3943531aa2f42722`
- 20 reviewed Concepts
- 136 reviewed Resources
- 148 reviewed practical Questions
- 3 normalized Evidence objects
- **307 governed objects**
- **391 canonical public routes**

This baseline identifies the UK reference content state. Administrative release-state records added after this snapshot do not change the baseline unless governed content or its public route contract changes.

## Acceptance basis

The baseline incorporates:

1. the accepted Relationships & family UK v1 bounded slice;
2. the merged UK breadth reference candidate from PR #139;
3. the merged Organisations & peer community UK reference slice from PR #140.

PR #139 exact-head validation passed at `f0312e47096bddbfcc28ca9c7c98cf9e62f2d99b` and hostile review passed before its protected merge.

PR #140 exact-head validation passed at `cc6cf04be2e390c9ec047692fa1c8b5b9f989f2a`; its merge commit is the frozen source commit above.

## Coverage boundary

This baseline means the repository has a strong bounded UK-first reference seed across all current need domains. It does **not** mean:

- every UK service, organisation, local authority or provider is catalogued;
- every condition or neurodivergent identity has equal depth;
- listed Resources are endorsed or quality-scored;
- local evidence can be generalized into UK-wide policy;
- clinical, legal, diagnostic or medication decisions are delegated to ND Oracle;
- the corpus is complete or permanently current.

Remaining UK work is maintenance and depth improvement rather than a prerequisite for the first reference baseline.

## Frozen system boundaries

The baseline preserves the existing controls for:

- provenance and reviewed-source identity;
- Claim ↔ Evidence ↔ uncertainty routes;
- jurisdiction and local-to-national containment;
- clinical diagnosis and medication authority;
- safeguarding and crisis routing;
- deterministic governed discovery;
- frozen ranking-policy boundaries;
- privacy-first local discovery;
- no query storage, profiling or analytics;
- no external-search or AI answer authority;
- static production deployment;
- exact-SHA protected release and immutable production evidence.

## Production boundary

Freezing this baseline is **not** a production deployment.

At the time this record was created, accepted production remained the 2026-09-03 Relationships & family release identified by `contracts/current-production.json`, with 208 governed objects and 292 canonical routes.

The UK Reference Baseline v1 becomes accepted production only after:

1. exact-current-main validation;
2. hostile review of the final release diff/state;
3. exact-SHA protected deployment;
4. fresh network-backed verification of all 391 canonical routes;
5. production-state reconciliation.

## Expansion rule

Systematic international expansion must not be treated as one undifferentiated "all countries" task.

Future expansion should proceed jurisdiction by jurisdiction, using the UK Assessment & diagnosis implementation as the precedent:

- explicit jurisdiction identity;
- national/local variation kept visible;
- local evidence cannot silently become national policy;
- first-party routes preferred for system/process claims;
- discovery scope is cryptographically or deterministically bound where appropriate;
- serious clinical/legal/efficacy claims retain governed Evidence and uncertainty;
- no provider endorsement is inferred from inclusion.

## Reopening conditions

Reopen the baseline version if a future change materially alters any of:

- governed object count or identity;
- canonical public-route contract;
- frozen discovery or authority boundaries;
- evidence semantics;
- jurisdiction model;
- production/publication architecture.

Ordinary freshness reviews, corrected access notes and bounded depth additions may proceed after v1, but they should be recorded as post-baseline evolution rather than rewriting this snapshot.

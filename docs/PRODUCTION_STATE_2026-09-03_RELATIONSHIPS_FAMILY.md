# ND Oracle production state — 2026-09-03 — Relationships & family

Accepted production state recorded on 2026-09-03 after exact-SHA deployment and fresh network-backed verification of the Relationships & family UK v1 release.

This document records an already completed production acceptance. It does not itself authorize or perform a deployment. It is the immutable human-readable evidence record referenced by `contracts/current-production.json` until a later accepted deployment replaces the current pointer.

The earlier `docs/PRODUCTION_STATE_2026-09-03.md` remains immutable historical evidence for the preceding accepted deployment and must not be rewritten into this state.

## Identity

- Canonical site: `https://ndoracle.org`
- Public-site builder contract: `v1.2`
- Accepted production source SHA: `5c05d775a5d548c0f4ad92f78e25008febe40d69`
- Accepted production source tree: `5861cd9ecbd33b2e465bbbd9027324182a9ef12b`
- Source merge: PR #137 — `ND Oracle: Relationships & family UK reference slice v1`
- Exact-head candidate validation: `33795297003` (run #331), job `100781648392`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33796135523` (run #22)
- Exact-main guard job: `100784510018`
- Direct Upload job: `100784550321`
- Generated artifact SHA-256: `4864e9a9aa56a3278ad46d4a32695354f25018b9ce9d2ccb46cf8fa68ba4ba2a`
- Cloudflare deployment identity: `https://7452fa61.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom-domain set verified by deployment workflow: `ndoracle.org`
- Fresh live-production verification run: `33796510768` (run #17)
- Fresh live-production verification job: `100785403728`

The accepted source tree is byte-for-byte identical to the exact PR #137 candidate tree that passed run #331. The merge commit therefore changed commit identity but not the reviewed content tree.

## Deployment proof

Deployment run #22 checked out exact source SHA `5c05d775a5d548c0f4ad92f78e25008febe40d69`, verified that it was still protected `main`, compiled the Python sources, validated all 208 authoritative objects and ran the complete 392-test regression suite before building the static artifact.

The deployment then enforced the static/no-runtime boundary, recorded artifact SHA-256 `4864e9a9aa56a3278ad46d4a32695354f25018b9ce9d2ccb46cf8fa68ba4ba2a`, verified pinned Wrangler `4.114.0`, verified the existing Direct Upload Cloudflare Pages project `nd-oracle`, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

Cloudflare completed the production deployment as `https://7452fa61.nd-oracle.pages.dev`. The workflow separately verified the project subdomain `nd-oracle.pages.dev`, production branch `main`, Direct Upload mode and the exact custom-domain set containing only `ndoracle.org` in addition to the project subdomain.

A duplicate dispatch produced workflow run `33796133637` (run #21), but repository concurrency cancelled it before any job executed. Run #22 is the sole successful deployment for this acceptance and the only deployment identity used here.

## Corpus at acceptance

The accepted production corpus contains exactly 208 governed objects:

- 20 reviewed Concept objects;
- 99 reviewed Resource objects;
- 86 reviewed Question objects;
- 3 normalized v0.2 Evidence objects.

The Evidence registry contains 60 governed source records across 49 governed Claims: 3 normalized Evidence objects plus 57 accepted legacy embedded source records. All 49 Claims are evidence-covered and the exact-head acceptance run reports 0 Evidence gaps.

Freshness at acceptance, proved on the identical accepted tree in exact-head run #331:

- 60 governed Evidence source records checked; 0 overdue as of 2026-09-03;
- 208 governed objects checked; 0 overdue as of 2026-09-03.

Resource inclusion remains **not endorsement**. Question routes retain the boundary **Relevant to inspect, not recommended**.

## Public contract

The accepted public site contains exactly 292 canonical indexable routes.

Fresh production verification run `33796510768` revalidated the 208-object repository and complete 392-test regression suite, then passed every one of the 292 canonical routes at `https://ndoracle.org` together with the v1.0 governed discovery/evidence and frozen compatibility contracts.

The verifier concluded:

`Verified 292 canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at https://ndoracle.org.`

## Relationships & family acceptance

The accepted corpus contains 13 Relationships & family Questions: the three earlier parent/relationship routes plus ten governed journeys covering friendship misunderstandings, partner communication/processing/sensory needs, boundaries, ordinary conflict and repair, intimacy/consent, parenting a neurodivergent child, disabled/neurodivergent parent service access, family-event sensory/social load, domestic-abuse/safeguarding routing, and an explicit no-authority leave/stay route.

Eight added Resources remain reviewed, claimless navigation records. Their inclusion does not establish efficacy, provider quality, legal entitlement or suitability for an individual.

Acceptance preserves these boundaries:

- parenting a neurodivergent child is distinct from support for a parent who is neurodivergent or disabled;
- ordinary relationship communication does not displace safeguarding where fear, control, violence or sexual pressure is present;
- consent remains necessary regardless of diagnosis or communication style;
- ND Oracle does not diagnose a partner or family member;
- ND Oracle does not decide who is right or decide whether a relationship should continue;
- disability-service access preserves the legal split between England, Scotland and Wales and Northern Ireland;
- the hard personal diagnosis and medication-decision boundaries remain unchanged;
- no ranking weights were changed to manufacture stronger relationship results;
- no accounts, analytics, query persistence, profiling, personalised ranking, external search service or AI answer authority were introduced.

## Discovery state

The accepted production preserves the frozen v1.1 discovery policy and the existing Assessment extension:

- frozen base scoped routes: 41;
- Assessment extension scoped routes: 29;
- total governed scoped routes: 70.

The Relationships & family release adds governed content and benchmark coverage without changing these scoped-route registries or the frozen ranking weights.

## Protected dispatch provenance

The connected GitHub integration available during this release did not expose a direct `workflow_dispatch` write action. The owner had explicitly authorized the exact production SHA after merge and post-merge proof.

A temporary unmerged branch, `ops/dispatch-release-5c05d775`, contained only an exact-SHA one-shot trigger that invoked the repository's existing guarded deployment workflow. The deployment workflow itself retained all production protections and Cloudflare secrets remained confined to the protected deployment environment. After dispatch, the temporary branch was reset to exact accepted source SHA `5c05d775a5d548c0f4ad92f78e25008febe40d69`; no temporary workflow entered protected `main`.

A separate temporary unmerged branch, `ops/live-verify-5c05d775`, invoked the existing read-only live-production verifier only after deployment succeeded. It too was reset to the exact accepted source SHA after dispatch. No temporary verification workflow entered protected `main`.

## Historical production evidence

`docs/PRODUCTION_STATE_2026-09-03.md` remains the immutable record of the preceding 2026-09-03 accepted deployment from source SHA `20926066e76e06beeef7d9ba87f24b88bada8658`, with 190 governed objects, 274 canonical routes and its own deployment/verification evidence.

`docs/PRODUCTION_STATE_v1.2.md` remains immutable historical evidence for the separately accepted 2026-09-01 v1.2 deployment. Earlier accepted production states remain frozen in their own documents. Historical evidence is never inferred to be current merely because its filename contains a semantic version or the same calendar date.

## Acceptance statement

The current accepted public production is the artifact generated from exact source SHA `5c05d775a5d548c0f4ad92f78e25008febe40d69`, tree `5861cd9ecbd33b2e465bbbd9027324182a9ef12b`, with SHA-256 `4864e9a9aa56a3278ad46d4a32695354f25018b9ce9d2ccb46cf8fa68ba4ba2a`, deployed as `https://7452fa61.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org` with all 292 canonical routes freshly verified.

Future current-production claims must resolve `contracts/current-production.json`, the referenced immutable production-state document, deployment identity and fresh live evidence together rather than inferring current state from an older production record.

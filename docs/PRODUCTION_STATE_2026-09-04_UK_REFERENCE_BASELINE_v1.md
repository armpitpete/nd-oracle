# ND Oracle production state — 2026-09-04 — UK Reference Baseline v1

Accepted production state recorded on 2026-09-04 after exact-SHA deployment and fresh network-backed verification of the frozen UK Reference Baseline v1.

This document records an already completed production acceptance. It does not itself authorize or perform a deployment. It is the immutable human-readable evidence record referenced by `contracts/current-production.json` until a later accepted deployment replaces the current pointer.

The earlier `docs/PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md` remains immutable historical evidence for the preceding accepted deployment and must not be rewritten into this state.

## Identity

- Canonical site: `https://ndoracle.org`
- Public-site builder contract: `v1.2`
- UK Reference Baseline v1 frozen-content source commit: `802e69b4437a276c234a036d9cd8f3f58f582b71`
- Frozen-content source tree: `8cf57114836ba4e5443d5bae3943531aa2f42722`
- Accepted production source SHA: `579c012cc9b31707409579da05b52a4d07efe61c`
- Accepted production source tree: `5d9dd369a9ddb271d4949e9d6d3f3bd0928d1d84`
- Baseline freeze PR: #141 — `ND Oracle: freeze UK Reference Baseline v1`
- Exact-head validation: `33878434853` (run #339), job `101040909793`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33880971901` (run #23)
- Exact-main guard job: `101049268139`
- Direct Upload job: `101049294282`
- Generated artifact SHA-256: `5357cc31658b37dc6c7d9f0ff4f0330894df8877a7869024ad6feefce8d4e0f4`
- Cloudflare deployment identity: `https://925a10c7.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom-domain set verified by deployment workflow: `ndoracle.org`
- Fresh live-production verification run: `33881392179` (run #340)
- Fresh live-production verification job: `101050648620`
- Temporary evidence PR: #142 — closed unmerged after evidence capture

The exact PR #141 head `b91a0a7b3ad8b6be533d10b4ee71d22bdbbbcf13` and merged production source `579c012cc9b31707409579da05b52a4d07efe61c` share tree `5d9dd369a9ddb271d4949e9d6d3f3bd0928d1d84`. The merge therefore changed commit identity but not the validated filesystem tree.

## Deployment proof

Deployment run #23 checked out exact source SHA `579c012cc9b31707409579da05b52a4d07efe61c`, verified that it was still current protected `main`, compiled the Python sources, validated all 307 authoritative objects and ran the complete 416-test regression suite before building the static artifact.

The deployment then enforced the static/no-runtime boundary, recorded artifact SHA-256 `5357cc31658b37dc6c7d9f0ff4f0330894df8877a7869024ad6feefce8d4e0f4`, verified pinned Wrangler `4.114.0`, verified the existing Direct Upload Cloudflare Pages project `nd-oracle`, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

Cloudflare completed the production deployment as `https://925a10c7.nd-oracle.pages.dev`. The workflow separately verified project subdomain `nd-oracle.pages.dev`, production branch `main`, Direct Upload mode and the exact custom-domain set containing only `ndoracle.org` in addition to the project subdomain.

## Corpus at acceptance

The accepted production corpus contains exactly 307 governed objects:

- 20 reviewed Concept objects;
- 136 reviewed Resource objects;
- 148 reviewed Question objects;
- 3 normalized v0.2 Evidence objects.

The Evidence registry contains 60 governed source records across 49 governed Claims: 3 normalized Evidence objects plus 57 accepted legacy embedded source records. All 49 Claims are evidence-covered and the acceptance run reports 0 Evidence gaps.

Freshness at acceptance:

- 60 governed Evidence source records checked; 0 overdue as of 2026-09-04;
- 307 governed objects checked; 0 overdue as of 2026-09-04.

Resource inclusion remains **not endorsement**. Question routes retain the boundary **Relevant to inspect, not recommended**.

## Public contract

The accepted public site contains exactly 391 canonical indexable routes.

Fresh production verification run `33881392179` revalidated the 307-object repository and complete 416-test regression suite, then passed every one of the 391 canonical routes at `https://ndoracle.org` together with the governed discovery/evidence and frozen compatibility contracts.

The verifier concluded:

`Verified 391 canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at https://ndoracle.org.`

## UK Reference Baseline v1 acceptance

The accepted corpus is the first frozen UK-first reference baseline. It includes the previously accepted Assessment & diagnosis, Relationships & family and Games & downtime work, the merged UK breadth slice, and the Organisations & peer community UK v1 slice.

The baseline preserves the documented limits:

- it is not a complete catalogue of every UK service or organisation;
- local evidence cannot silently become a UK-wide rule;
- Resource inclusion is not endorsement or a quality/safety score;
- ND Oracle does not diagnose, prescribe, make medication decisions, or replace clinical/legal authority;
- safeguarding and crisis boundaries remain explicit;
- no accounts, analytics, query persistence, profiling, personalised ranking, external search service or AI answer authority were introduced.

Remaining UK work is maintenance and depth improvement rather than a prerequisite for the first reference baseline.

## Discovery state

The accepted production preserves the frozen v1.1 discovery policy and existing Assessment extension:

- frozen base scoped routes: 41;
- Assessment extension scoped routes: 29;
- total governed scoped routes: 70.

The UK breadth and Organisations slices add governed content and benchmark coverage without changing these scoped-route registries or frozen ranking weights.

## Temporary live-verification provenance

The connected GitHub integration did not expose a direct `workflow_dispatch` write action for the existing live-production verification workflow.

Temporary PR #142 was rooted directly in accepted deployment source `579c012cc9b31707409579da05b52a4d07efe61c` and changed only the validation workflow on its disposable branch by appending the existing read-only command:

`python scripts/verify_live_site.py --origin https://ndoracle.org`

Run #340 passed all local gates and the full live production contract. PR #142 was then closed unmerged and its branch reset to exact accepted source SHA. No temporary verification workflow entered protected `main`.

## Historical production evidence

`docs/PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md` remains the immutable record of the preceding accepted production from source SHA `5c05d775a5d548c0f4ad92f78e25008febe40d69`, with 208 governed objects, 292 canonical routes and its own deployment/verification evidence.

`docs/PRODUCTION_STATE_2026-09-03.md`, `docs/PRODUCTION_STATE_v1.2.md` and earlier production-state documents remain immutable historical evidence. Historical evidence is never inferred to be current merely because its filename contains a semantic version or calendar date.

## Acceptance statement

The current accepted public production is the artifact generated from exact source SHA `579c012cc9b31707409579da05b52a4d07efe61c`, tree `5d9dd369a9ddb271d4949e9d6d3f3bd0928d1d84`, with SHA-256 `5357cc31658b37dc6c7d9f0ff4f0330894df8877a7869024ad6feefce8d4e0f4`, deployed as `https://925a10c7.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org` with all 391 canonical routes freshly verified.

**UK REFERENCE BASELINE v1 — FINAL PASS** is warranted once this production-state reconciliation itself passes exact-head CI, hostile review and protected merge.

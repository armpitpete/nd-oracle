# ND Oracle production state — 2026-09-04 — Republic of Ireland Assessment & diagnosis v1

Accepted production state recorded on 2026-09-04 after exact-SHA deployment and fresh network-backed verification of the first non-UK jurisdiction package, **Republic of Ireland Assessment & diagnosis v1**, on top of the frozen UK Reference Baseline v1.

This document records an already completed production deployment and verification. It does not itself authorize or perform a deployment. It is the immutable human-readable evidence record intended to be referenced by `contracts/current-production.json` after this reconciliation passes its own protected merge gate.

The preceding `docs/PRODUCTION_STATE_2026-09-04_UK_REFERENCE_BASELINE_v1.md` remains immutable historical evidence for the prior accepted production and must not be rewritten into this state.

## Identity

- Canonical site: `https://ndoracle.org`
- Public-site builder contract: `v1.2`
- Republic of Ireland implementation PR: #146 — `ND Oracle: Republic of Ireland Assessment & diagnosis v1`
- Exact tested PR head: `8bc379e2434384dbc3b5b2a0a447bb6ab639ca8e`
- Accepted production source SHA: `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197`
- Accepted production source tree: `bce34c6908a409daefce1ba24ce06349fa24cac2`
- Exact-head candidate validation: `33892517335` (run #347), job `101087480396`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33896144673` (run #24)
- Exact-main guard job: `101099134040`
- Direct Upload job: `101099176328`
- Generated artifact SHA-256: `4967f8a711aefeb8bf878de7dba5a18063cd57d0b1ca54e53d6022d9cfe5f033`
- Cloudflare deployment identity: `https://325a78a3.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom-domain set verified by deployment workflow: `ndoracle.org`
- Fresh live-production verification run: `33896431576` (run #18)
- Fresh live-production verification job: `101100054619`

The exact tested PR #146 head `8bc379e2434384dbc3b5b2a0a447bb6ab639ca8e` and merged production source `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197` share tree `bce34c6908a409daefce1ba24ce06349fa24cac2`. The merge therefore changed commit identity but not the tested filesystem tree.

## Deployment proof

Deployment run #24 was dispatched on `main` with exact release SHA `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197`. Its protected guard independently confirmed that the requested SHA was still current protected `main` and that the pre-existing `cloudflare-pages-production` environment remained restricted to protected branches.

The Direct Upload job checked out that exact SHA, verified a clean checkout, compiled the Python sources, validated all **319 authoritative objects**, and ran the complete **439-test regression suite** before building the static artifact.

The deployment then enforced the static/no-runtime boundary, recorded artifact SHA-256 `4967f8a711aefeb8bf878de7dba5a18063cd57d0b1ca54e53d6022d9cfe5f033`, verified pinned Wrangler `4.114.0`, verified the existing Direct Upload Cloudflare Pages project `nd-oracle`, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

Cloudflare completed the production deployment as `https://325a78a3.nd-oracle.pages.dev`. The workflow separately verified project subdomain `nd-oracle.pages.dev`, production branch `main`, Direct Upload mode and the exact custom-domain set containing only `ndoracle.org` in addition to the project subdomain.

## Corpus at acceptance

The accepted production corpus contains exactly **319 governed objects**:

- 20 reviewed Concept objects;
- 144 reviewed Resource objects;
- 152 reviewed Question objects;
- 3 normalized v0.2 Evidence objects.

The increase from the frozen UK Reference Baseline v1 is exactly the bounded Republic of Ireland package:

- 4 new governed Questions;
- 8 reviewed, claimless HSE Resources;
- no new Evidence object;
- no core schema change.

The Evidence registry remains at 60 governed source records across 49 governed Claims. All 49 Claims remain evidence-covered and the exact-tree acceptance run reports 0 Evidence gaps.

Freshness on the tested tree:

- 60 governed Evidence source records checked; 0 overdue as of 2026-09-04;
- 319 governed objects checked; 0 overdue as of 2026-09-04.

Resource inclusion remains **not endorsement**. Question routes retain the boundary **Relevant to inspect, not recommended**.

## Public contract

The accepted public site contains exactly **403 canonical indexable routes**.

Fresh production verification run `33896431576` revalidated the 319-object repository and complete 439-test regression suite, then passed every one of the 403 canonical routes at `https://ndoracle.org` together with the governed discovery/evidence and frozen compatibility contracts.

The verifier concluded:

`Verified 403 canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at https://ndoracle.org.`

The live verifier also confirmed:

- Concept contract: 20;
- Question contract: 152;
- Resource contract: 144;
- frozen public compatibility: PASS;
- governed navigation/discovery contract: PASS.

## Republic of Ireland package acceptance

The first international package remains deliberately bounded to Assessment & diagnosis.

Accepted governed journeys:

1. adult autism assessment in the Republic of Ireland;
2. child autism assessment in the Republic of Ireland;
3. adult ADHD assessment in the Republic of Ireland;
4. HSE Assessment of Need versus clinical diagnostic assessment.

The package preserves these limits:

- Republic-of-Ireland HSE routes do not inherit Northern Ireland HSC/NHS rules;
- Northern Ireland HSC/NHS routes do not inherit Republic-of-Ireland HSE rules;
- England Right to Choose cannot surface as a Republic-of-Ireland entitlement;
- the HSE Adult ADHD Model of Care is not treated as proof of universal current specialist-team availability;
- current adult autism private-access facts do not become provider endorsement;
- Assessment of Need is kept distinct from clinical autism/ADHD diagnosis;
- diagnosis is kept distinct from medication initiation, titration, prescribing and treatment decisions;
- child ADHD remains deliberately deferred because the current evidence does not support a strong uniform national access route.

This deployment does **not** claim comprehensive Republic-of-Ireland neurodivergence coverage.

## Discovery state

The accepted production preserves the frozen v1.1 policy file and uses additive jurisdiction packages:

- frozen base scoped routes: 41;
- UK Assessment extension scoped routes: 29;
- Republic of Ireland Assessment extension scoped routes: 12;
- total governed scoped routes: **82**.

The frozen `discovery/routing-policy-v1.1.json` remains unchanged. The Republic-of-Ireland extension is loaded as a separate sidecar and preserves the existing ranking weights and clinical refusal boundaries.

## Temporary dispatch provenance

The connected GitHub integration does not expose a direct `workflow_dispatch` write action. Two disposable helper branches were therefore used only to dispatch the existing protected workflows; neither entered `main`.

### Deployment dispatcher

- Branch: `release/temp-dispatch-ireland-v1-production`
- Temporary commit: `ec4e3bca4357b615d72f59f8616e32307bcf1214`
- Helper run: `33896104483`
- Helper job: `101099001632`

The helper verified that current `main` exactly equalled the authorized release SHA, then dispatched the existing protected `deploy-cloudflare-pages.yml` workflow on `main` with that exact SHA. The protected deployment workflow then performed its own independent guards.

### Live-verification dispatcher

- Branch: `release/temp-dispatch-ireland-v1-live-verify`
- Temporary commit: `7a9e8ae9927a738008f346347b37b52353fbdd61`
- Helper run: `33896422762`
- Helper job: `101100013185`

The helper verified successful deployment run `33896144673` against the exact authorized main SHA, then dispatched the existing read-only `live-production-verify.yml` workflow on `main`.

After the helper runs completed, both temporary branches were reset to exact production source SHA `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197`. No temporary helper workflow remains on those branch tips and no helper workflow entered protected `main`.

## Historical production evidence

`docs/PRODUCTION_STATE_2026-09-04_UK_REFERENCE_BASELINE_v1.md` remains the immutable record of the immediately preceding accepted production from source SHA `579c012cc9b31707409579da05b52a4d07efe61c`, with 307 governed objects, 391 canonical routes and artifact SHA-256 `5357cc31658b37dc6c7d9f0ff4f0330894df8877a7869024ad6feefce8d4e0f4`.

`docs/PRODUCTION_STATE_2026-09-03_RELATIONSHIPS_FAMILY.md`, `docs/PRODUCTION_STATE_2026-09-03.md`, `docs/PRODUCTION_STATE_v1.2.md` and earlier production-state documents remain immutable historical evidence. Historical evidence is never inferred to be current merely because its filename contains a semantic version or calendar date.

## Acceptance statement

The deployed public production is the artifact generated from exact source SHA `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197`, tree `bce34c6908a409daefce1ba24ce06349fa24cac2`, with SHA-256 `4967f8a711aefeb8bf878de7dba5a18063cd57d0b1ca54e53d6022d9cfe5f033`, deployed as `https://325a78a3.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org` with all **403 canonical routes freshly verified**.

**REPUBLIC OF IRELAND ASSESSMENT & DIAGNOSIS v1 — PRODUCTION FINAL PASS** is warranted once this production-state reconciliation itself passes exact-head CI, hostile review and protected merge.

# ND Oracle production state — 2026-09-04 — NHS bulletin promotion v1

Accepted production state recorded on 2026-09-04 after exact-SHA deployment and fresh network-backed verification of the three post-baseline NHS bulletin additions promoted through PR #149.

This document records an already completed production deployment and verification. It does not itself authorize or perform a deployment. It becomes the human-readable evidence record referenced by `contracts/current-production.json` after this reconciliation passes its protected merge gate.

The preceding `docs/PRODUCTION_STATE_2026-09-04_IRELAND_ASSESSMENT_DIAGNOSIS_v1.md` remains immutable historical evidence for the immediately preceding accepted production.

## Identity

- Canonical site: `https://ndoracle.org`
- Public-site builder contract: `v1.2`
- Promotion PR: #149 — `ND Oracle: promote NHS bulletin guidance into active corpus`
- Exact tested PR head: `75ba390cf83df6423b3b6749649188daa1f27e97`
- Exact-head validation run: `33922482003` (#359), job `101183678148`
- Accepted production source SHA: `94d1ab0d8df5699b1316e64d70c28fe11b25b7cf`
- Accepted production source tree: `9270919d26d3529889db498b202b8132bc3316b7`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33924992354` (run #25)
- Exact-main guard job: `101191460345`
- Direct Upload job: `101191493014`
- Generated artifact SHA-256: `2899f9c214f6eecded51c8cf64aa356fd76674b32bdd1b801dfa2ae5521aedbb`
- Cloudflare deployment identity: `https://99fd62e1.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom-domain set verified by deployment workflow: `ndoracle.org`
- Fresh live-production verification run: `33925184354` (run #19)
- Fresh live-production verification job: `101192042604`

The exact tested PR #149 head `75ba390cf83df6423b3b6749649188daa1f27e97` and merged production source `94d1ab0d8df5699b1316e64d70c28fe11b25b7cf` share tree `9270919d26d3529889db498b202b8132bc3316b7`. The protected merge therefore changed commit identity but not the tested filesystem tree.

## Deployment proof

Deployment run #25 was dispatched on `main` with exact release SHA `94d1ab0d8df5699b1316e64d70c28fe11b25b7cf`. Its protected guard independently confirmed that the requested SHA was still current protected `main` and that the pre-existing `cloudflare-pages-production` environment remained restricted to protected branches.

The Direct Upload job checked out that exact SHA, verified a clean checkout, compiled the Python sources, validated all **325 authoritative objects**, and ran the complete **451-test regression suite** before building the static artifact.

The workflow then enforced the static/no-runtime boundary, recorded artifact SHA-256 `2899f9c214f6eecded51c8cf64aa356fd76674b32bdd1b801dfa2ae5521aedbb`, verified pinned Wrangler `4.114.0`, verified the existing Direct Upload Cloudflare Pages project `nd-oracle`, rechecked current `main`, and uploaded the exact artifact.

Cloudflare completed the production deployment as `https://99fd62e1.nd-oracle.pages.dev`. The workflow preserved the existing `ndoracle.org` attachment and made no project-creation, DNS, custom-domain, secret, or other production-configuration change.

## Corpus at acceptance

The accepted production corpus contains exactly **325 governed objects**:

- 20 reviewed Concept objects;
- 147 reviewed Resource objects;
- 155 reviewed Question objects;
- 3 normalized v0.2 Evidence objects.

Relative to the immediately preceding Ireland production state, this release adds exactly six governed objects:

- 3 reviewed, claimless Resources;
- 3 bounded Questions;
- no new Concept;
- no new Evidence object;
- no schema change.

The promoted additions are:

1. NHS England learning-disability register / annual-health-check guidance — Healthcare access;
2. Autism Central school-attendance guidance — Education & study;
3. NHS England person-centred suicide-safety policy — Mental wellbeing.

The Evidence registry remains at 60 governed source records across 49 governed Claims. **All 49 Claims remain evidence-covered.** Exact-head acceptance run #359 proved **49/49 Claims covered** and **0 Evidence gaps**.

Freshness on the exact accepted tree:
- 60 governed Evidence source records checked; 0 overdue;
- 325 governed objects checked; 0 overdue.

Resource inclusion remains **not endorsement**. Question routes retain the boundary **Relevant to inspect, not recommended**.

## Safety and authority boundaries

The deployment preserves the promoted content boundaries:

- GP learning-disability register identification is not presented as formal diagnosis;
- register inclusion is not presented as establishing specialist-service eligibility;
- autism, ADHD, dyslexia or another specific learning difficulty is not treated as automatic learning-disability-register eligibility;
- autistic school-attendance difficulty is framed as possible barriers and support approaches, not as a diagnosis or a single-cause explanation;
- school-attendance content does not become safeguarding adjudication or legal attendance advice;
- suicide-safety content explains NHS England policy/practice framing only;
- ND Oracle does not classify an individual as low, medium or high suicide risk, decide that someone is safe, provide crisis counselling, or replace urgent human services.

## Public contract

Fresh live-production verification run `33925184354` revalidated all 325 governed objects and the complete 451-test regression suite, then passed every one of the **409 canonical routes** at `https://ndoracle.org`.

The live verifier concluded:

`Verified 409 canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at https://ndoracle.org.`

It also confirmed:

- Concept contract: 20;
- Question contract: 155;
- Resource contract: 147;
- frozen public compatibility: PASS;
- governed navigation/discovery contract: PASS.

## Discovery state

The release does not change discovery scope architecture:

- frozen base scoped routes: 41;
- UK Assessment extension scoped routes: 29;
- Republic of Ireland Assessment extension scoped routes: 12;
- total governed scoped routes: **82**.

The frozen `discovery/routing-policy-v1.1.json` and ranking weights remain unchanged. The three new Questions are added to their public navigation groups without altering the frozen routing-policy file.

## Temporary dispatch provenance

The connected GitHub integration does not expose direct `workflow_dispatch` writes. Two disposable helper branches were used only to dispatch the already-existing protected workflows. Neither entered `main`.

### Deployment dispatcher

- Branch: `release/temp-dispatch-nhs-bulletin-2026-09-04-production`
- Temporary commit: `782097b26fcf11050c23b0670663390bdcee63f8`
- Helper run: `33924984240`
- Helper job: `101191432067`

The helper verified that current `main` exactly equalled the authorized release SHA, then dispatched the existing protected `deploy-cloudflare-pages.yml` workflow on `main` with that exact SHA.

### Live-verification dispatcher

- Branch: `release/temp-dispatch-nhs-bulletin-2026-09-04-live-verify`
- Temporary commit: `09a62940ab1e1dba917c89cd46f01954981d0adc`
- Helper run: `33925177269`
- Helper job: `101192018186`

The helper verified successful deployment run `33924992354` against the exact authorized main SHA, then dispatched the existing read-only `live-production-verify.yml` workflow on `main`.

After the helper runs completed, both temporary branches were reset to exact production source SHA `94d1ab0d8df5699b1316e64d70c28fe11b25b7cf`. No temporary helper workflow remains on their branch tips and no helper workflow entered protected `main`.

## Historical production evidence

`docs/PRODUCTION_STATE_2026-09-04_IRELAND_ASSESSMENT_DIAGNOSIS_v1.md` remains the immutable record of the immediately preceding accepted production from source SHA `10fe0a0bc1f1a075e420dd0bc432d0a69cc15197`, with 319 governed objects, 403 canonical routes and artifact SHA-256 `4967f8a711aefeb8bf878de7dba5a18063cd57d0b1ca54e53d6022d9cfe5f033`.

The UK Reference Baseline and earlier production-state documents also remain immutable historical evidence.

## Acceptance statement

The deployed public production is the artifact generated from exact source SHA `94d1ab0d8df5699b1316e64d70c28fe11b25b7cf`, tree `9270919d26d3529889db498b202b8132bc3316b7`, with SHA-256 `2899f9c214f6eecded51c8cf64aa356fd76674b32bdd1b801dfa2ae5521aedbb`, deployed as `https://99fd62e1.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org` with all **409 canonical routes freshly verified**.

**NHS BULLETIN PROMOTION v1 — PRODUCTION FINAL PASS** is warranted once this production-state reconciliation itself passes exact-head CI, hostile review and protected merge.

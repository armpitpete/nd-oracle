# ND Oracle production state v1.0

Accepted production state recorded on 2026-08-31 after exact-SHA deployment and fresh network-backed verification.

## Release identity

- Canonical site: `https://ndoracle.org`
- Accepted release SHA: `a0081e7d879e23568792ad5a468250eeb21dd20b`
- v1.0 implementation: PR #107 — `ND Oracle v1.0 governed discovery`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33383848729` (run #15)
- Deployment guard job: `99461927898`
- Direct Upload job: `99461949316`
- Generated artifact SHA-256: `e8155159a1f439e5d8a17e65e1bb960430207ad43e1836959fdb1d48737ded51`
- Cloudflare deployment identity: `https://9c561434.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom domain set verified by the deployment workflow: `ndoracle.org`
- Fresh live-production verification run: `33384188012` (run #15)
- Fresh live-production verification job: `99462984077`

The deployment workflow checked out the exact release SHA, verified a clean exact identity, validated all 119 governed objects, ran the 305-test regression suite, built the v1.0 static artifact, enforced the static/no-runtime boundary, recorded the deterministic artifact digest, verified pinned Wrangler 4.114.0 and the existing Direct Upload Cloudflare Pages project, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

## Pre-deployment validation

Fresh exact-release-tree validation was also recorded before deployment in workflow run `33365699311`, attempt 2, job `99423438259`.

It passed:

- Python compilation;
- validation of all 119 authoritative objects;
- governed freshness checking with 0 overdue objects as of 2026-08-31;
- the complete 305-test regression suite;
- frozen public compatibility fixtures;
- the v1.0 Question contract.

## Corpus at release

The authoritative corpus contains exactly 119 governed objects:

- 20 reviewed Concept objects;
- 58 reviewed Resource objects;
- 38 reviewed Question objects;
- 3 governed Evidence objects supporting the bounded claim-bearing Resource pilot.

Resource inclusion remains explicitly not endorsement. Claim-bearing pilot Resources expose bounded claim wording, scope/applicability, evidence routes, uncertainty and limitations. Claimless Resources remain listings rather than efficacy, safety, legal or diagnostic conclusions.

Question routes use the boundary **Relevant to inspect, not recommended**. They expose governed material relevant to an ordinary-language problem without converting discovery results into personalised recommendations.

## Public contract

The accepted public site exposes exactly 142 canonical indexable routes.

v1.0 adds governed ordinary-language discovery on top of the accepted reading/navigation surface:

- 20 Concept detail routes;
- 58 Resource detail routes;
- 38 Question detail routes;
- need-led navigation through `/needs/` plus eight life-area hubs;
- browse-by-content-type at `/types/`;
- geographic-scope navigation at `/places/`;
- governed-content A–Z at `/a-z/`;
- deterministic local discovery at `/find/`;
- explicit no-answer behaviour for unsupported or unsafe requests;
- a frozen 50-case ordinary-language discovery benchmark with top-three route and decision-depth gates;
- bounded claim/evidence presentation for the Resource pilot;
- explicit UK/Great Britain/England/Scotland/Wales/Northern Ireland applicability where systems differ;
- preservation of the frozen historical public compatibility contracts.

`/find/` uses a same-origin local JavaScript enhancement only. Typed query text remains in browser memory and is not submitted in a URL or form request. The route retains a useful no-script fallback. The accepted surface adds no accounts, analytics, query storage, external search service, AI answer authority, personalised ranking or recommendation scoring.

## Builder and verifier architecture

v1.0 flattened the active publication path. `scripts/build_site.py` is the current self-contained builder and `scripts/verify_live_site.py` is the current production verifier. Current runtime execution no longer chains through the v0.6/v0.8/v0.9 builders or verifiers. Historical compatibility is retained as explicit fixtures/contracts and preserved historical source where required rather than as the active release dependency chain.

## Post-deployment verification

Fresh production verification was executed from a GitHub-hosted runner against `https://ndoracle.org` using the current v1.0 production verifier from exact source SHA `a0081e7d879e23568792ad5a468250eeb21dd20b`.

Verification evidence:

- Workflow: `ND Oracle live production verification`
- Run: `33384188012` (run #15)
- Job: `99462984077`
- Source SHA checked out: `a0081e7d879e23568792ad5a468250eeb21dd20b`
- Regression tests before the live probe: 305, all passing
- Canonical live routes verified: 142

Verified live at `https://ndoracle.org`:

- all 142 canonical routes;
- all 20 Concept routes;
- all 58 Resource routes;
- all 38 Question routes;
- v1.0 navigation/discovery contract;
- v1.0 governed evidence presentation;
- inherited v0.6 public-reading and resource compatibility contracts;
- frozen public compatibility fixture;
- production HTTP/security requirements;
- passive/static surface requirements;
- canonical-link and route identity requirements;
- noindex and not-found compatibility behaviour covered by the current verifier.

The live verifier concluded:

> Verified 142 canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at https://ndoracle.org.

## Acceptance statement

v1.0 is the accepted production release. The accepted deployment artifact is the artifact generated from exact release SHA `a0081e7d879e23568792ad5a468250eeb21dd20b` with SHA-256 `e8155159a1f439e5d8a17e65e1bb960430207ad43e1836959fdb1d48737ded51`, deployed as `https://9c561434.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org`.

Future production claims must re-resolve repository `main`, deployment identity and fresh live verification rather than assuming this state remains current.

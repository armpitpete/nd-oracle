# ND Oracle production state v1.2

Accepted production state recorded on 2026-09-01 after exact-SHA deployment and fresh network-backed verification.

This document records an already completed production acceptance. It does not itself authorize or perform a deployment.

## Release identity

- Canonical site: `https://ndoracle.org`
- Accepted release SHA: `fad8e560979ba67bf94104d02f3b5100db8572cf`
- Accepted release tree: `8d7d0eeea74af359435469660acf76526c6423a0`
- v1.2 content implementation: PR #124 — `ND Oracle v1.2: need coverage expansion v0.1`
- v1.2 builder identity implementation: PR #122 — `ND Oracle v1.2: builder release identity`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33490134037` (run #18)
- Deployment guard job: `99799419491`
- Direct Upload job: `99799448834`
- Generated artifact SHA-256: `b88c462115434d3ce9929f1e62ec29d0fb0095c13c05ec17c87b813afea426a1`
- Cloudflare deployment identity: `https://600ea685.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom-domain set verified by the deployment workflow: `ndoracle.org`
- Fresh live-production evidence run: `33490631672`
- Fresh live-production evidence job: `99801014835`
- Temporary evidence PR: #129 — closed unmerged after verification; branch reset to the accepted production SHA.

The deployment workflow checked out exact release SHA `fad8e560979ba67bf94104d02f3b5100db8572cf`, verified its clean identity, compiled the Python sources, validated all 125 authoritative objects, ran the complete 335-test permanent regression suite, built the static artifact, enforced the static/no-runtime boundary, recorded the deterministic artifact digest, verified pinned Wrangler 4.114.0 and the existing Direct Upload Cloudflare Pages project, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

The Direct Upload completed as `https://600ea685.nd-oracle.pages.dev`. The deployment workflow separately verified the existing `nd-oracle.pages.dev` project subdomain and the exact custom-domain set containing only `ndoracle.org` in addition to that project subdomain.

A first manual deployment-dispatch attempt, run `33489980961` (run #17), contained leading spaces in the `release_sha` input. The exact-SHA guard rejected that input before deployment and the Direct Upload job did not run. It is therefore recorded as a successful safety rejection, not a production deployment.

## Corpus at release

The authoritative corpus is exactly 125 governed objects:

- 20 reviewed Concept objects;
- 61 reviewed Resource objects;
- 41 reviewed Question objects;
- 3 governed Evidence objects supporting the bounded claim-bearing Resource pilot.

v1.2 adds a bounded devolved higher-education disability-support parity slice without changing schemas. The six new governed objects are:

Questions:

- `disabled-student-support-scotland`;
- `disabled-student-support-wales`;
- `disabled-student-support-northern-ireland`.

Resources:

- `saas-disabled-students-allowance`;
- `student-finance-wales-disabled-students-allowance`;
- `northern-ireland-disabled-students-allowance`.

The new Resources are navigation/access records with no claim authority. Resource inclusion remains explicitly not endorsement, and Question routes retain the boundary **Relevant to inspect, not recommended**.

## Public contract

The accepted public site contains exactly 148 canonical indexable routes.

v1.2 preserves the accepted v1.1 discovery architecture and privacy/static boundaries while adding the six governed Scotland/Wales/Northern Ireland higher-education support routes and a bounded human-facing builder release identity.

The preserved discovery contract includes:

- a compositional hard boundary for personal diagnosis and medication decisions;
- explicit query jurisdiction extraction without inferred location;
- complete requested-set containment for jurisdiction compatibility;
- meaningful lexical eligibility before ranking;
- high-specificity governed identity and routing-phrase paths for valid narrow queries;
- route-scope provenance bound to exact governed field values and SHA-256 fingerprints;
- deterministic final-reason states and decision traces;
- algorithmic Python/browser decision-trace parity;
- orientation disabled because ablation showed it was unnecessary.

The release adds no external search, accounts, analytics, query persistence, profiling, personalised ranking, LLM classification or AI answer authority. Typed `/find/` query text remains local to browser memory.

The v1.2 builder identity `PUBLIC_SITE_RELEASE = "v1.2"` is a human-facing repository/build contract label. It does not alter governed content, rendering authority, discovery decisions or production evidence semantics. Repository `VERSION` and `CHANGELOG.md` remain on their existing independent line.

## Frozen acceptance carried forward

The v1.2 release preserves the accepted v1.1 safety and discovery architecture. The frozen regression evidence remains green, including the personal clinical-decision boundary, jurisdiction containment, informational/action controls, unrelated-benign controls, Python/browser parity, governed scope provenance and privacy/static constraints.

The v1.2 need-coverage benchmark additionally proves the Scotland, Wales and Northern Ireland disabled-student support queries route first to the matching national Question while the existing England route remains unchanged and incompatible national scoped routes are excluded.

These discovery fixtures are regression evidence, not new knowledge authority. Governed objects and their evidence/uncertainty routes remain the source of truth.

## Post-deployment verification

The repository contains a dedicated manual read-only workflow, `ND Oracle live production verification`, whose production step is:

`python scripts/verify_live_site.py --origin https://ndoracle.org`

The connected GitHub integration used for this acceptance could inspect but could not create a new `workflow_dispatch`. To avoid weakening the release gate, the exact verifier command was therefore executed from a temporary evidence-only pull request rooted directly in accepted production source SHA `fad8e560979ba67bf94104d02f3b5100db8572cf`.

Verification evidence:

- Temporary PR: #129 — `TEMP: v1.2 live production acceptance probe`
- Base/source SHA: `fad8e560979ba67bf94104d02f3b5100db8572cf`
- Temporary test-only head: `51087ad753ca2e252a1b661fcf4f2b4633bae06d`
- Validation run: `33490631672` (run #256)
- Job: `99801014835`
- Permanent regression tests represented by production source: 335
- Test count in the evidence run: 336, all passing (335 permanent tests plus one temporary read-only live-probe wrapper)
- Authoritative objects validated: 125
- Freshness: 125 checked, 0 overdue as of 2026-09-01
- Canonical live routes verified: 148

Verified live at `https://ndoracle.org`:

- all 148 canonical routes;
- all 20 Concept routes;
- all 61 Resource routes;
- all 41 Question routes;
- the new Scotland, Wales and Northern Ireland Disabled Students' Allowance Resource routes;
- the new Scotland, Wales and Northern Ireland disabled-student support Question routes;
- v1.1 bounded governed discovery carried into v1.2;
- governed evidence presentation;
- navigation and route identity;
- frozen public compatibility contracts;
- production HTTP/security requirements;
- passive/static surface requirements;
- canonical-link, noindex and not-found compatibility behaviour covered by the current verifier.

The verifier concluded: `Verified 148 canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at https://ndoracle.org.`

Temporary PR #129 was closed unmerged after evidence capture and its branch was reset to exact accepted production SHA `fad8e560979ba67bf94104d02f3b5100db8572cf`. No temporary test entered protected `main`.

Successful upload alone is therefore not being treated as production acceptance: v1.2 has deterministic exact-SHA deployment evidence and a separate fresh network-backed proof against the canonical domain.

## Acceptance statement

v1.2 is the accepted production release. The accepted deployment artifact is the artifact generated from exact release SHA `fad8e560979ba67bf94104d02f3b5100db8572cf`, tree `8d7d0eeea74af359435469660acf76526c6423a0`, with SHA-256 `b88c462115434d3ce9929f1e62ec29d0fb0095c13c05ec17c87b813afea426a1`, deployed as `https://600ea685.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org`.

Future production claims must re-resolve repository `main`, deployment identity and fresh live verification rather than assuming this state remains current. Historical v1.1 and earlier production evidence remains frozen separately in versioned production-state documents.

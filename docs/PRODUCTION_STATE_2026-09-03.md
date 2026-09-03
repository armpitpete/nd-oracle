# ND Oracle production state — 2026-09-03

Accepted production state recorded on 2026-09-03 after exact-SHA deployment and fresh network-backed verification.

This document records an already completed production acceptance. It does not itself authorize or perform a deployment. It is the immutable human-readable evidence record referenced by `contracts/current-production.json` until a later accepted deployment replaces the current pointer.

## Identity

- Canonical site: `https://ndoracle.org`
- Public-site builder contract: `v1.2`
- Accepted production source SHA: `20926066e76e06beeef7d9ba87f24b88bada8658`
- Accepted production source tree: `e19ef7a180a1ad5b31849763aa00b516f384d53e`
- Source merge: PR #134 — `ND Oracle: UK Assessment & Diagnosis reference implementation v1`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33784220017` (run #19)
- Exact-main guard job: `100744979763`
- Direct Upload job: `100745012361`
- Generated artifact SHA-256: `166bab6dc89dd02d119dbba23035f948666a5b3e3ee39cd179f71a45d3289c71`
- Cloudflare deployment identity: `https://4651e0b6.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom-domain set verified by deployment workflow: `ndoracle.org`
- Fresh live-production verification run: `33785057163` (run #316)
- Fresh live-production verification job: `100747694338`
- Temporary evidence PR: #135 — closed unmerged after verification; disposable branch reset to the accepted production source SHA.

The deployment workflow checked out exact source SHA `20926066e76e06beeef7d9ba87f24b88bada8658`, verified that it was still exact protected `main`, compiled the Python sources, validated all 190 authoritative objects, ran the complete 380-test permanent regression suite, built the static artifact, enforced the static/no-runtime boundary, recorded the deterministic artifact digest, verified pinned Wrangler 4.114.0 and the existing Direct Upload Cloudflare Pages project, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

The Direct Upload completed as `https://4651e0b6.nd-oracle.pages.dev`. The workflow separately verified the existing `nd-oracle.pages.dev` project subdomain and the exact custom-domain set containing only `ndoracle.org` in addition to that project subdomain.

## Corpus at acceptance

The accepted production corpus contains exactly 190 governed objects:

- 20 reviewed Concept objects;
- 91 reviewed Resource objects;
- 76 reviewed Question objects;
- 3 normalized v0.2 Evidence objects.

The Evidence registry contains 60 governed source records across 49 governed Claims: 3 normalized Evidence objects plus 57 accepted legacy embedded source records. All 49 Claims are evidence-covered and the acceptance run reports 0 Evidence gaps.

Freshness at acceptance:

- 60 governed Evidence source records checked; 0 overdue as of 2026-09-03;
- 190 governed objects checked; 0 overdue as of 2026-09-03.

Resource inclusion remains **not endorsement**. Question routes retain the boundary **Relevant to inspect, not recommended**.

## Public contract

The accepted public site contains exactly 274 canonical indexable routes.

Fresh production verification passed all 274 canonical routes and the current governed discovery/evidence and frozen compatibility contracts at `https://ndoracle.org`.

The corpus includes the UK Assessment & diagnosis reference implementation: adult/child × autism/ADHD × England/Scotland/Wales/Northern Ireland, plus cross-cutting Questions for private assessment, waiting/support, refusal or disagreement, after-assessment outcomes, communication/sensory adjustments, co-occurring autism/ADHD and other neurodevelopmental assessments.

## Discovery and safety acceptance

The accepted production preserves the frozen v1.1 discovery policy and extends it additively:

- frozen base scoped routes: 41;
- Assessment extension scoped routes: 29;
- total governed scoped routes: 70.

`discovery/routing-policy-v1.1.json` remains unchanged. The Assessment extension cannot replace a frozen v1.1 intent or scope route and each new scope binding is cryptographically bound to an exact governed field value.

The accepted production preserves:

- deterministic Python/browser discovery parity;
- the hard personal diagnosis and medication-decision boundary;
- the additional child/third-person diagnosis-request hardening introduced by the Assessment implementation;
- explicit requested jurisdiction containment without inferred location;
- England-only Right to Choose containment;
- Scottish health-board variation, Welsh health-board/local-service variation and Northern Ireland Trust/service-development variation;
- separation of ADHD diagnosis from medication initiation, titration, prescribing and shared-care decisions;
- support routes that do not silently require formal diagnosis where the relevant system does not require it;
- claimless status for the 15 added Assessment Resources;
- Evidence browsing excluded from ordinary `/find/` ranking;
- no accounts, analytics, query persistence, profiling, personalised ranking, external search service or AI answer authority.

The deployment changed no schemas, ranking weights, privacy/query-handling rules or deployment topology.

## Fresh network-backed verification

Because the connected GitHub integration could inspect but not dispatch the repository's manual live-production workflow, the exact read-only command `python scripts/verify_live_site.py --origin https://ndoracle.org` was appended temporarily to the ordinary validation workflow on disposable PR #135 rooted directly in accepted production source SHA `20926066e76e06beeef7d9ba87f24b88bada8658`.

Evidence run `33785057163` (run #316), job `100747694338`, passed:

- compile;
- validation of all 190 authoritative objects;
- Evidence coverage: 49/49 Claims covered, 0 gaps, 60 governed source records;
- Evidence-source freshness: 60 checked, 0 overdue;
- governed-content freshness: 190 checked, 0 overdue;
- the complete 380-test permanent regression suite;
- the read-only live-production contract.

The verifier concluded:

`Verified 274 canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at https://ndoracle.org.`

Temporary PR #135 was then closed unmerged and its disposable branch was reset to exact accepted production source SHA. No temporary workflow modification entered protected `main`.

## Historical production evidence

`docs/PRODUCTION_STATE_v1.2.md` remains an immutable historical record of the separately accepted 2026-09-01 deployment from SHA `fad8e560979ba67bf94104d02f3b5100db8572cf`. Its 125-object, 148-route and 335-test figures remain historically correct for that deployment and must not be rewritten into current-state values.

Earlier accepted production states remain frozen in their own versioned documents. Historical evidence is never inferred to be current merely because its filename contains the highest semantic version.

## Acceptance statement

The current accepted production is the artifact generated from exact source SHA `20926066e76e06beeef7d9ba87f24b88bada8658`, tree `e19ef7a180a1ad5b31849763aa00b516f384d53e`, with SHA-256 `166bab6dc89dd02d119dbba23035f948666a5b3e3ee39cd179f71a45d3289c71`, deployed as `https://4651e0b6.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org`.

Future current-production claims must resolve `contracts/current-production.json`, the referenced immutable production-state document, deployment identity and fresh live evidence together rather than inferring current state from a historical versioned filename.

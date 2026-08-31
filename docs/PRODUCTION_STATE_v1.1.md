# ND Oracle production state v1.1

Accepted production state recorded on 2026-08-31 after exact-SHA deployment and fresh network-backed verification.

This document records an already completed production acceptance. It does not itself authorize or perform a deployment.

## Release identity

- Canonical site: `https://ndoracle.org`
- Accepted release SHA: `3032305dd81d48b2c6cc777b72f038267f995819`
- v1.1 implementation: PR #114 — `ND Oracle v1.1: bounded discovery policy`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33425750168` (run #16)
- Deployment guard job: `99598770894`
- Direct Upload job: `99598811900`
- Generated artifact SHA-256: `84f6ac3e76d07d26367794b87cf6f85736aa4d8e976865d2d79a806bd429dfb7`
- Cloudflare deployment identity: `https://29c88484.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom-domain set verified by the deployment workflow: `ndoracle.org`
- Fresh live-production verification run: `33426342672` (run #16)
- Fresh live-production verification job: `99600728836`

The deployment workflow checked out exact release SHA `3032305dd81d48b2c6cc777b72f038267f995819`, verified its clean identity, compiled the Python sources, validated all 119 authoritative objects, ran the complete 322-test regression suite, built the static artifact, enforced the static/no-runtime boundary, recorded the deterministic artifact digest, verified pinned Wrangler 4.114.0 and the existing Direct Upload Cloudflare Pages project, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

The Direct Upload completed as `https://29c88484.nd-oracle.pages.dev`. The deployment workflow separately verified the existing `nd-oracle.pages.dev` project subdomain and the exact custom-domain set containing only `ndoracle.org` in addition to that project subdomain.

## Corpus at release

The authoritative corpus remained exactly 119 governed objects:

- 20 reviewed Concept objects;
- 58 reviewed Resource objects;
- 38 reviewed Question objects;
- 3 governed Evidence objects supporting the bounded claim-bearing Resource pilot.

v1.1 made no knowledge-object or schema changes. Resource inclusion remains explicitly not endorsement, and Question routes retain the boundary **Relevant to inspect, not recommended**.

## Public contract

The accepted public site remains exactly 142 canonical indexable routes. v1.1 preserves the v1.0 reading, navigation and evidence surfaces while replacing the bounded discovery decision policy with the accepted v1.1 architecture.

The v1.1 discovery contract adds:

- a compositional hard boundary for personal diagnosis and medication decisions;
- explicit query jurisdiction extraction without inferred location;
- complete requested-set containment for jurisdiction compatibility;
- meaningful lexical eligibility before ranking;
- high-specificity governed identity and routing-phrase paths for valid narrow queries;
- route-scope provenance bound to exact governed field values and SHA-256 fingerprints;
- deterministic final-reason states and decision traces;
- algorithmic Python/browser decision-trace parity;
- orientation ablation, with orientation remaining disabled because the other bounded mechanisms passed the frozen informational/action controls without it.

The release adds no external search, accounts, analytics, query persistence, profiling, personalised ranking, LLM classification or AI answer authority. Typed `/find/` query text remains local to browser memory.

## Frozen v1.1 acceptance

The exact v1.1 candidate preserved the v1.0 50-case discovery benchmark and satisfied the v1.1 rejection corpus, including:

- 40/40 personal clinical-decision probes reaching the explicit clinical boundary;
- 0/16 educational controls incorrectly refused by that boundary;
- 0/70 jurisdiction-conflict probes returning an incompatible scoped top result;
- 20/20 informational/action orientation controls passing under ablation, so orientation remained disabled;
- 20/20 unrelated benign controls returning no governed result;
- frozen public compatibility, governance/provenance checks and Python/browser parity remaining green.

These discovery fixtures are regression evidence, not new knowledge authority. Governed objects and their evidence/uncertainty routes remain the source of truth.

## Post-deployment verification

Fresh production verification was executed from a GitHub-hosted runner against `https://ndoracle.org` using exact source SHA `3032305dd81d48b2c6cc777b72f038267f995819`.

Verification evidence:

- Workflow: `ND Oracle live production verification`
- Run: `33426342672` (run #16)
- Job: `99600728836`
- Source SHA checked out: `3032305dd81d48b2c6cc777b72f038267f995819`
- Regression tests before the live probe: 322, all passing
- Authoritative objects validated: 119
- Canonical live routes verified: 142

Verified live at `https://ndoracle.org`:

- all 142 canonical routes;
- all 20 Concept routes;
- all 58 Resource routes;
- all 38 Question routes;
- v1.1 bounded governed discovery;
- governed evidence presentation;
- navigation and route identity;
- frozen public compatibility contracts;
- production HTTP/security requirements;
- passive/static surface requirements;
- canonical-link, noindex and not-found compatibility behaviour covered by the current verifier.

The live verification workflow completed successfully. Successful upload alone is therefore not being treated as production acceptance; the release has both deterministic deployment evidence and a separate fresh network-backed proof against the canonical domain.

## Acceptance statement

v1.1 is the accepted production release. The accepted deployment artifact is the artifact generated from exact release SHA `3032305dd81d48b2c6cc777b72f038267f995819` with SHA-256 `84f6ac3e76d07d26367794b87cf6f85736aa4d8e976865d2d79a806bd429dfb7`, deployed as `https://29c88484.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org`.

Future production claims must re-resolve repository `main`, deployment identity and fresh live verification rather than assuming this state remains current. Historical v1.0 production evidence remains frozen separately in `docs/PRODUCTION_STATE_v1.0.md`.
# ND Oracle production state v0.7

Accepted production state recorded on 2026-08-28.

## Release identity

- Canonical site: `https://ndoracle.org`
- Accepted release SHA: `a074b6da26f95f58f15f38e44ae2b7a43fe6383c`
- Question corpus foundation: PR #85
- Public question-led discovery: PR #86
- Direct-script deployment entrypoint repair: PR #87
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33174604415` (run #11)
- Generated artifact SHA-256: `f987e707af2df3551a3a8657d03c8b67be91209b09d948206d2c0963557e923b`
- Cloudflare deployment identity: `https://b7b9549a.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom domain set verified by the deployment workflow: `ndoracle.org`

The workflow checked out the exact release SHA, revalidated the knowledge graph, ran the 293-test pre-deployment regression suite, built the static artifact using the same direct-script entrypoint that failed in the earlier attempt, enforced the static/no-runtime boundary, recorded the artifact digest, verified the existing Direct Upload Cloudflare Pages project, rechecked `main`, and uploaded the exact artifact.

## Corpus at release

The authoritative corpus contains 30 objects:

- 10 reviewed v0.1 Concept objects.
- 15 reviewed v0.2 Resource objects.
- 5 reviewed v0.2 Question objects.

Resource inclusion remains explicitly not endorsement. Question routes identify material relevant to inspect; they are not personalised recommendations and do not convert Resource listings into efficacy or safety claims.

The public site exposes 42 canonical indexable routes. v0.7 adds:

- `/questions/`
- `/questions/task-starting-and-organisation/`
- `/questions/low-time-pressure-games/`
- `/questions/workplace-support-great-britain/`
- `/questions/autism-information-and-support/`
- `/questions/autism-anxiety-tools/`

Each Question page exposes the current bounded understanding, related governed Concepts/Resources, evidence still needed, recorded dissent, reopening conditions, provenance, and the boundary **Relevant to inspect, not recommended**.

`/oracle/` remains a compatibility `noindex` route. v0.7 adds no free-text question submission, AI/chat answer authority, accounts, query storage, analytics, recommendation scores or personalised ranking.

## Post-deployment verification

The runtime used by the controller could not resolve external DNS reliably, so fresh production verification was executed on a GitHub-hosted runner without changing production code.

Temporary non-merge PR #88 was based on the exact deployed source SHA `a074b6da26f95f58f15f38e44ae2b7a43fe6383c`. Its only change was a test that invoked the unchanged `scripts/verify_live_site.py` against `https://ndoracle.org`. The PR was closed without merge after evidence capture.

Verification evidence:

- Validation workflow run: `33174896417` (run #149)
- Validation job: `98860851937`
- Total tests including the live-proof wrapper: 294
- Canonical live routes verified: 42

Verified live at `https://ndoracle.org`:

- all 42 canonical routes;
- all 10 Concept reading routes;
- `/resources/`, `/tools/`, `/games/`, `/community/`;
- all 15 Resource detail routes;
- `/questions/` and all 5 Question detail routes;
- v0.6 public-reading contract;
- v0.6 15-resource contract;
- v0.7 five-question discovery contract;
- canonical/indexability requirements;
- 404 behaviour;
- `robots.txt`;
- exact sitemap contract;
- `/oracle/` compatibility `noindex` behaviour;
- `www` redirect with path/query preservation;
- passive/static public-surface and production HTTP/security requirements inherited from the v0.6 verifier.

Verifier terminal result:

`Verified 42 canonical routes plus v0.6 reading/resource and v0.7 question-led discovery production contracts at https://ndoracle.org.`

## Earlier failed deployment attempt

Deployment run `33172730697` (run #10) targeted the previous exact main `b161bf73700d17fd9fb3be475ae910daaac0b4c5`. The protected-main guard, checkout identity, compilation, 30-object validation and 291 regression tests passed, but `python scripts/build_site.py` failed because the v0.7 compatibility wrapper could not import the `scripts` package under direct file execution.

No Cloudflare upload occurred in run #10. PR #87 fixed both direct builder and direct verifier entrypoints and added subprocess regression tests for the exact deployment command before run #11 was authorised.

## Acceptance statement

v0.7 is the accepted production release. Future production claims must re-resolve repository `main`, deployment identity and live verification rather than assuming this state remains current.

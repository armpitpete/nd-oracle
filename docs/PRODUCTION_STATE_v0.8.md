# ND Oracle production state v0.8

Accepted production state recorded on 2026-08-28.

## Release identity

- Canonical site: `https://ndoracle.org`
- Accepted release SHA: `e4a93bbbd579b8a033954300e540a11dafc65f5d`
- Content/navigation release: PR #90
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33178697469` (run #12)
- Deployment guard job: `98873984846`
- Direct Upload job: `98874029685`
- Generated artifact SHA-256: `75594181876f422d62fde519ec3db29574bfdd48e6b797df15b940d223597479`
- Cloudflare deployment identity: `https://9b09ce0c.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom domain set verified by the deployment workflow: `ndoracle.org`

The workflow checked out the exact release SHA, verified a clean exact identity, revalidated the governed graph, ran the 302-test pre-deployment regression suite, built the v0.8 static artifact through the direct deployment entrypoint, enforced the static/no-runtime boundary, recorded the deterministic artifact digest, verified pinned Wrangler 4.114.0 and the existing Direct Upload Cloudflare Pages project, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

## Corpus at release

The authoritative corpus contains 49 objects:

- 10 reviewed v0.1 Concept objects.
- 25 reviewed v0.2 Resource objects.
- 14 reviewed v0.2 Question objects.

Resource inclusion remains explicitly not endorsement. The ten resources added in v0.8 remain claimless unless a separate governed claim/evidence route exists. Question routes identify material relevant to inspect; they are not personalised recommendations and do not convert Resource listings into efficacy, safety, legal or diagnostic claims.

## Public contract

The accepted public site exposes 62 canonical indexable routes.

v0.8 expands the content/navigation surface with:

- 10 additional Resource detail routes;
- 9 additional practical Question detail routes;
- `/books-media/` as a governed Resource browse route;
- clearer primary labels: `Questions`, `Topics`, `Resources`;
- grouped Question navigation for everyday life/technology, work/study, information/support, games/downtime and anxiety/self-management;
- Topic pages linking to practical Questions and reviewed Resources;
- Resource pages linking back to Questions that lead to them;
- Question pages linking to governed Topics and Resources;
- corpus-derived production verification for all current Resource and Question detail routes.

`/oracle/` remains a compatibility `noindex` route. v0.8 adds no free-text question submission, AI/chat answer authority, accounts, query storage, analytics, recommendation scores or personalised ranking.

## Post-deployment verification

Fresh production verification was executed from a GitHub-hosted runner against `https://ndoracle.org` using the unchanged v0.8 verifier from the exact deployed source.

Temporary non-merge PR #91 was based on exact deployed source SHA `e4a93bbbd579b8a033954300e540a11dafc65f5d`. Its only change was `tests/test_live_production_v08_proof.py`, which invoked `scripts/verify_live_site.verify_production("https://ndoracle.org")`. The PR was closed without merge after evidence capture.

Verification evidence:

- Temporary proof PR: #91, closed without merge
- Proof head: `24e1b19ae3c0dfa5bfb6a9056bb7668483c0567e`
- Validation workflow run: `33178846180` (run #160)
- Validation job: `98874501625`
- Total tests including the live-proof wrapper: 303
- Canonical live routes verified: 62

Verified live at `https://ndoracle.org`:

- all 62 canonical routes;
- all 10 Concept reading routes;
- `/resources/`, `/tools/`, `/games/`, `/community/`, `/books-media/`;
- all 25 Resource detail routes;
- `/questions/` and all 14 Question detail routes;
- v0.8 14-question contract;
- v0.8 25-resource contract;
- v0.8 cross-content navigation contract;
- inherited v0.6 public-reading contract;
- inherited v0.6 15-resource compatibility contract;
- frozen v0.7 five-question compatibility contract;
- canonical/indexability requirements;
- 404 behaviour;
- `robots.txt`;
- exact sitemap contract;
- `/oracle/` compatibility `noindex` behaviour;
- `www` redirect with path/query preservation;
- inherited passive/static public-surface and production HTTP/security requirements.

The live-proof run completed successfully with all 303 tests passing.

## Acceptance statement

v0.8 is the accepted production release. The accepted deployment artifact is the artifact generated from exact release SHA `e4a93bbbd579b8a033954300e540a11dafc65f5d` with SHA-256 `75594181876f422d62fde519ec3db29574bfdd48e6b797df15b940d223597479`, deployed as `https://9b09ce0c.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org`.

Future production claims must re-resolve repository `main`, deployment identity and live verification rather than assuming this state remains current.

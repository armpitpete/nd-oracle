# ND Oracle production state v0.9

Accepted production state recorded on 2026-08-28 after repaired deployment and fresh network-backed verification.

## Release identity

- Canonical site: `https://ndoracle.org`
- Accepted release SHA: `286c1999a27509e74da2c70e5076fbdcda46e1a1`
- Content/navigation release: PR #93
- Homepage compatibility repair: PR #95
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful repaired deployment run: `33204071981` (run #14)
- Deployment guard job: `98960539377`
- Direct Upload job: `98960568499`
- Generated artifact SHA-256: `e13ed02c4f6794844fa6b2930937bdada772f0d15330290972acfc761b505076`
- Cloudflare deployment identity: `https://74c14b3d.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom domain set verified by the deployment workflow: `ndoracle.org`

The workflow checked out the exact release SHA, verified a clean exact identity, validated all 100 governed objects, ran the 314-test pre-deployment regression suite, built the v0.9 static artifact through the direct deployment entrypoint, enforced the static/no-runtime boundary, recorded the deterministic artifact digest, verified pinned Wrangler 4.114.0 and the existing Direct Upload Cloudflare Pages project, rechecked current `main`, and uploaded the exact artifact without changing DNS or custom-domain configuration.

## Corpus at release

The authoritative corpus contains exactly 100 governed objects:

- 20 reviewed v0.1 Concept objects;
- 50 reviewed v0.2 Resource objects;
- 30 reviewed v0.2 Question objects.

Resource inclusion remains explicitly not endorsement. The v0.9 Resource catalogue is claimless unless a separate governed Claim/Evidence route exists. Question routes identify material relevant to inspect; they are not personalised recommendations and do not convert Resource listings into efficacy, safety, legal or diagnostic claims.

The freshness gate checked all 100 governed objects with zero overdue records on 2026-08-28. Resource review age is capped at 180 days; other current governed content is capped at 365 days.

## Public contract

The accepted public site exposes exactly 125 canonical indexable routes.

v0.9 expands the public content/navigation surface with:

- 20 Concept detail routes;
- 50 Resource detail routes;
- 30 Question detail routes;
- need-led navigation through `/needs/` plus eight life-area hubs;
- browse-by-content-type at `/types/`;
- geographic-scope navigation at `/places/`;
- complete governed-content A–Z at `/a-z/`;
- Related Questions on Question pages;
- scope/type navigation on Resource pages;
- explicit editorial assignment of all 30 Questions to navigation groups;
- freshness enforcement in CI;
- preservation of the accepted v0.8 25-Resource/14-Question object subset;
- preservation of the frozen v0.7 five-question discovery contract.

`/oracle/` remains a compatibility `noindex` route. v0.9 adds no free-text question submission, AI/chat answer authority, accounts, query storage, analytics, recommendation scores or personalised ranking.

## Repair history

The first v0.9 deployment from SHA `5665f8a988fe3ba58da1fd111ce45067668d9721` succeeded technically as deployment run `33203052545` (run #13), but was not accepted as production after the network-backed verifier found a backward-navigation regression: two of the five frozen v0.7 practical Question routes were no longer linked from the homepage.

Temporary proof PR #94 captured that failure and was closed without merge. All 125 canonical routes and the v0.9 content/navigation contracts passed; the failure was limited to homepage compatibility for `workplace-support-great-britain` and `autism-anxiety-tools`.

PR #95 restored the frozen v0.7 homepage routes and added a regression test tying the builder compatibility set to the verifier's frozen v0.7 set. PR #95 was merged to produce the accepted release SHA `286c1999a27509e74da2c70e5076fbdcda46e1a1`, which was then separately authorised and deployed in run #14.

## Post-deployment verification

Fresh production verification was executed from a GitHub-hosted runner against `https://ndoracle.org` using the current v0.9 production verifier from the exact repaired deployed source.

Temporary non-merge PR #96 was based on exact deployed source SHA `286c1999a27509e74da2c70e5076fbdcda46e1a1`. Its only change was `tests/test_live_production_v09_repair_proof.py`, which invoked `scripts.verify_live_site.verify_production("https://ndoracle.org")`. The PR was closed without merge after evidence capture.

Verification evidence:

- Temporary proof PR: #96, closed without merge
- Proof head: `c2178c8a274fb470296389309b76be6813923553`
- Validation workflow run: `33204284355` (run #173)
- Validation job: `98961250853`
- Total tests including the live-proof wrapper: 315
- Canonical live routes verified: 125

Verified live at `https://ndoracle.org`:

- all 125 canonical routes;
- all 20 Concept reading/navigation routes;
- all 50 Resource detail routes;
- all 30 Question detail routes;
- v0.9 20-Concept reading/navigation contract;
- v0.9 30-Question contract;
- v0.9 50-Resource contract;
- v0.9 need/type/place/A–Z navigation contract;
- accepted v0.8 25-Resource/14-Question object-set compatibility;
- inherited v0.6 public-reading contract;
- inherited v0.6 15-resource compatibility contract;
- frozen v0.7 five-question discovery contract, including homepage links;
- 404 behaviour;
- `robots.txt`;
- exact sitemap contract;
- `/oracle/` compatibility `noindex` behaviour;
- `www` redirect with path/query preservation;
- inherited passive/static public-surface and production HTTP/security requirements.

The live-proof run completed successfully with all 315 tests passing.

## Acceptance statement

v0.9 is the accepted production release. The accepted deployment artifact is the artifact generated from exact release SHA `286c1999a27509e74da2c70e5076fbdcda46e1a1` with SHA-256 `e13ed02c4f6794844fa6b2930937bdada772f0d15330290972acfc761b505076`, deployed as `https://74c14b3d.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org`.

Future production claims must re-resolve repository `main`, deployment identity and live verification rather than assuming this state remains current.

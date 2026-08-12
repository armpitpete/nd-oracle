# ND Oracle production state v0.4

Status date: 2026-08-12

## Accepted production identity

- Deployed commit: `cbfb4ccc95c6340d8822a034a1d90ba7c8438689`
- Recovery ref: `release/v0.4-production`
- Production deployment workflow: run `31599633888` (`Deploy Cloudflare Pages (manual)`, run #6)
- Release artifact SHA-256: `b3da9c5891ae0f8bf143f652afd1150b636eceb6b8f02a1e1669355df3e9b9d1`
- Cloudflare deployment identity: `https://6e1b16d6.nd-oracle.pages.dev`
- Canonical public origin: `https://ndoracle.org`

The deployed commit is the merge of PR #76, which brought neurodiversity, autism, ADHD, executive function and sensory processing through the same minimum evidence/review lifecycle gate as Batch A. The public surface remains ten topic pages; v0.4 increases review depth rather than topic count.

## Deployment evidence

The protected production workflow verified before upload that:

- the requested release SHA exactly matched protected `main`;
- the checked-out commit exactly matched the requested release SHA and the checkout was clean;
- 10 authoritative objects validated with all governed evidence, uncertainty, perspective, reference and graph routes resolving;
- the deployment run passed 263 regression tests;
- the generated site artifact built successfully;
- the artifact remained static-only, with no Pages Functions, Worker, Wrangler configuration or symlinks introduced;
- the release artifact SHA-256 was `b3da9c5891ae0f8bf143f652afd1150b636eceb6b8f02a1e1669355df3e9b9d1`;
- Wrangler was exactly `4.114.0`;
- the Cloudflare Pages project was exactly `nd-oracle`, Direct Upload, production branch `main`;
- the provider subdomain was exactly `nd-oracle.pages.dev`;
- the normalized custom-domain set was exactly `{ndoracle.org}`;
- project/domain state and protected `main` were rechecked immediately before deployment.

Cloudflare considered 26 artifact files, uploaded 7 changed files with 19 already present, uploaded `_headers`, and reported deployment complete at `6e1b16d6.nd-oracle.pages.dev`. No DNS or custom-domain mutation was requested.

## Independent live-production verification

Live acceptance was performed from a separate GitHub-hosted runner with no production secrets and no write capability.

The first post-deployment run of the older unified verifier passed every route and production-behaviour check it knew about, but reported the five Batch A topic URLs as unexpected sitemap entries because its expected sitemap was still frozen to the earlier five-topic site. A separate Batch A verifier confirmed those five routes and their sitemap entries were live, identifying the failure as stale verifier scope rather than a production defect.

PR #77 then updated only the unified verifier's expected canonical route set. On exact PR head `9000bfb2da6a4805fc0061d209ca3975fe41452c`, live-production workflow run `31601103377` passed from GitHub's network. Before making live requests it validated all 10 authoritative objects and passed 263 tests. It then verified all 16 canonical public routes (the homepage, Understand index, all 10 topic pages, How it works, About, Accessibility and Privacy), plus:

- exact canonical/final URLs and expected page identity;
- accepted production security headers;
- passive pages with no forms, scripts, iframes or external resource loads;
- the exact ten-topic `sitemap.xml` URL set;
- `robots.txt`, including the accepted Cloudflare-managed prefix compatibility;
- a real noindex 404;
- all five legacy compatibility routes remaining `noindex`;
- `www` redirecting to the HTTPS apex while preserving path and query.

The unified verifier reported: `Verified 16 canonical routes plus production HTTP/public-surface contract at https://ndoracle.org.` PR #77 was subsequently merged as verifier maintenance only; that later commit is not the deployed v0.4 content identity.

## Corpus state at v0.4

The deployed authoritative corpus contains:

- 10 concepts;
- 36 claims;
- 47 sources;
- 38 open uncertainties;
- 21 perspectives;
- 26 relations;
- 34 ecosystem entry-point groups.

All 10 concepts are `reviewed` / `editor_reviewed` and have a recorded `last_reviewed` date. Open questions remain represented as uncertainties rather than being converted into false completion.

## Accepted publication boundary

Production v0.4 is the reviewed ten-topic public release represented by deployed commit `cbfb4ccc95c6340d8822a034a1d90ba7c8438689` and artifact SHA-256 `b3da9c5891ae0f8bf143f652afd1150b636eceb6b8f02a1e1669355df3e9b9d1`.

Later repository commits that add tests, verification evidence or documentation do not silently redefine the deployed production artifact. A future production release requires the normal exact-main guarded deployment workflow and a new production-state record.

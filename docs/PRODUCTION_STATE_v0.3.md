# ND Oracle production state v0.3

Status date: 2026-08-12

## Accepted production identity

- Deployed commit: `5aadb3c56d01dc2ced22d699c646d475f14342ec`
- Recovery ref: `release/v0.3-production`
- Production deployment workflow: run `31595099388` (`Deploy Cloudflare Pages (manual)`, run #5)
- Release artifact SHA-256: `5002c61669dafcfdf3327fa162c7d6ef8d7ba6ff22e59b30748667b55aefc3e1`
- Cloudflare deployment identity: `https://66ee366b.nd-oracle.pages.dev`
- Canonical public origin: `https://ndoracle.org`

The deployed commit is the squash merge of PR #73, which promoted the owner-accepted Batch A concepts and expanded the authoritative/public corpus from five to ten topics.

## Deployment evidence

The protected production workflow verified before upload that:

- the requested release SHA exactly matched protected `main`;
- the checked-out commit exactly matched the requested release SHA;
- the checkout was clean;
- 10 authoritative objects validated with all governed evidence, uncertainty, perspective, reference and graph routes resolving;
- the deployment run passed 252 regression tests;
- the real generated site artifact built successfully;
- the artifact remained static-only, with no Pages Functions, Worker, Wrangler configuration or symlinks introduced;
- Wrangler was exactly `4.114.0`;
- the Cloudflare Pages project was exactly `nd-oracle`, Direct Upload, production branch `main`;
- the provider subdomain was exactly `nd-oracle.pages.dev`;
- the normalized custom-domain set was exactly `{ndoracle.org}`;
- project/domain state and protected `main` were rechecked immediately before deployment.

Cloudflare reported 26 artifact files considered, 9 uploaded and 17 already present, then reported deployment complete at `66ee366b.nd-oracle.pages.dev`.

## Independent live-production verification

Because the assistant's public web sandbox could not directly resolve the apex domain, live acceptance was performed from a separate GitHub-hosted runner with no production secrets and no write capability.

Live verification workflow run `31595417407` passed against `https://ndoracle.org` after deployment. It reused the established canonical-route verifier and confirmed all five newly published Batch A routes:

- `/understand/dyslexia/`
- `/understand/developmental-coordination-disorder/`
- `/understand/tourette-syndrome/`
- `/understand/learning-disability/`
- `/understand/developmental-language-disorder/`

For each new route the verifier required HTTP 200, exact final/canonical URL, expected page identity, HTML content type, the accepted production security headers, and a passive surface with no forms, scripts, iframes or external resource loads. It also confirmed all five routes are present in the live sitemap.

That live-verification candidate passed 254 tests before making the production requests. The checker was subsequently merged as PR #74; that later checker-only commit is not the deployed v0.3 content identity.

## Corpus state at v0.3

The deployed authoritative corpus contains:

- 10 concepts;
- 27 claims;
- 32 sources;
- 28 open uncertainties;
- 11 perspectives;
- 23 relations;
- 34 ecosystem entry-point groups.

The five Batch A concepts are `reviewed` / `editor_reviewed` with `last_reviewed` recorded. The original five v0.2 concepts remain `seed` / `unreviewed_seed`; v0.3 does not conceal that review debt.

## Accepted publication boundary

Production v0.3 is accepted as the ten-topic public release represented by deployed commit `5aadb3c56d01dc2ced22d699c646d475f14342ec` and artifact SHA-256 `5002c61669dafcfdf3327fa162c7d6ef8d7ba6ff22e59b30748667b55aefc3e1`.

Later repository commits that add tests, verification evidence or documentation do not silently redefine the deployed production artifact. A future production release requires the normal exact-main guarded deployment workflow and a new production-state record.

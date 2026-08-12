# ND Oracle production state v0.5

Status date: 2026-08-12

## Accepted production identity

- Deployed commit: `30c1de55e62d1560b6e19c71ae0b5fcc7d03ca9f`
- Recovery ref: `release/v0.5-production`
- Production deployment workflow: run `31603558575` (`Deploy Cloudflare Pages (manual)`, run #7)
- Release artifact SHA-256: `949ad218ffdfe871d4bfc8f979b1a0e0c934ef615eb85ace5e1dc0b753d80694`
- Cloudflare deployment identity: `https://a7c4e33f.nd-oracle.pages.dev`
- Canonical public origin: `https://ndoracle.org`

The deployed commit is the merge of PR #79, the consolidated v0.5 public-reading pass. It changes the presentation/reading layer over the existing reviewed ten-topic corpus; it does not redefine the authoritative claims, sources, uncertainties, perspectives or relations.

## What v0.5 publishes

The public reading layer now provides:

- one ordinary-language homepage question for every one of the 10 current topics;
- a deliberately simple first-read explanation on every topic page;
- the more precise authoritative summary behind progressive disclosure;
- visible `Last reviewed` information on every topic page;
- a public explanation of all supported confidence labels: high, moderate, low, contested and not applicable;
- an indexable `/feedback/` route for accessibility, wording, evidence and broken-page reports;
- a warning not to put private health/contact information into the public GitHub issue tracker;
- an explicit statement that a private feedback route is not yet available;
- no search, forms, accounts, JavaScript, analytics or advertising trackers.

The site build also fails if the homepage-question and simple-explanation sets do not exactly cover the authoritative concept corpus, so future topic expansion cannot silently ship without a human-oriented entry route.

## Deployment evidence

Production workflow run `31603558575` succeeded against exact protected `main` commit `30c1de55e62d1560b6e19c71ae0b5fcc7d03ca9f`.

Before upload the workflow established that:

- the requested release SHA exactly matched protected `main`;
- exact checkout and clean release identity checks passed;
- all 10 authoritative objects validated with governed evidence, uncertainty, perspective, reference and graph routes resolving;
- the release passed 268 regression tests;
- the v0.5 static site built successfully;
- the artifact remained within the static-only boundary;
- the artifact SHA-256 was `949ad218ffdfe871d4bfc8f979b1a0e0c934ef615eb85ace5e1dc0b753d80694`;
- Wrangler was exactly `4.114.0`;
- Cloudflare Pages project state remained Direct Upload on project `nd-oracle`, production branch `main`;
- provider subdomain remained exactly `nd-oracle.pages.dev`;
- normalized custom-domain set remained exactly `{ndoracle.org}`;
- protected `main` and Cloudflare project/domain state were rechecked immediately before deployment.

Cloudflare considered 27 artifact files, uploaded 25 files with 2 already present, uploaded `_headers`, and reported deployment complete at `a7c4e33f.nd-oracle.pages.dev`. No DNS or custom-domain mutation was requested.

## Independent live-production verification

Post-deployment acceptance was performed from a separate GitHub-hosted runner with no production secrets and no write capability.

PR #80 updated the read-only verifier for the v0.5 public route and reading contract. The first live candidate correctly established that all canonical pages and production HTTP checks passed, but exposed a verifier-only HTML-escaping mismatch for the apostrophe in the Neurodiversity first-read sentence. The checker and its fixture were repaired without changing production.

On final PR #80 head `9088b70a454a00a7c5f51ad24dbdd453fefa7ecf`, live-production workflow run `31604785310` passed. Before making live requests it validated all 10 authoritative objects and passed 270 tests.

The live checker then verified all 17 canonical public routes:

- `/`;
- `/understand/`;
- all 10 current topic routes;
- `/how-it-works/`;
- `/about/`;
- `/accessibility/`;
- `/feedback/`;
- `/privacy/`.

It additionally verified on the real apex domain:

- every current topic has its intended ordinary-language homepage question and link;
- all 10 topic pages expose the intended simple first-read explanation;
- all 10 topic pages visibly expose `Last reviewed` metadata;
- all 10 topic pages retain a `More precise description` disclosure;
- topic confidence labels link to the confidence explanation;
- the confidence page exposes all five supported confidence meanings;
- the feedback page links to the public issue tracker, warns against posting private health information and states the current lack of a private feedback channel;
- exact canonical/final URLs and expected page identity;
- accepted production security headers;
- passive pages with no forms, scripts, iframes or externally loaded resources;
- exact sitemap membership including `/feedback/` and excluding legacy compatibility routes;
- `robots.txt`, including accepted Cloudflare-managed prefix compatibility;
- a real noindex 404;
- all five legacy compatibility routes remaining `noindex`;
- `www` redirecting to the HTTPS apex while preserving path and query.

Final live result: `Verified 17 canonical routes plus v0.5 reading and production HTTP/public-surface contracts at https://ndoracle.org.`

PR #80 was subsequently merged as verifier maintenance only. That later repository commit does not redefine the deployed v0.5 artifact.

## Publication boundary

Production v0.5 is the public reading release represented by deployed commit `30c1de55e62d1560b6e19c71ae0b5fcc7d03ca9f` and artifact SHA-256 `949ad218ffdfe871d4bfc8f979b1a0e0c934ef615eb85ace5e1dc0b753d80694`.

Later repository commits that add verification evidence or documentation do not silently redefine the deployed production artifact. A future production release requires the normal exact-main guarded production workflow and a new production-state record.

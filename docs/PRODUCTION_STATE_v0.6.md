# ND Oracle production state v0.6

Accepted production state recorded on 2026-08-28.

## Release identity

- Canonical site: `https://ndoracle.org`
- Accepted release SHA: `a82fe49190ebc398da3c04c560c4dd0e823bd2e8`
- Source change: PR #83 — Publish the first governed ND ecosystem resource layer
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33169505862` (run #9)
- Generated artifact SHA-256: `c17be1b30afe2d8eb6c8d8dfc708aeb69627c462e946f2350d1afe95399572f1`
- Cloudflare deployment identity: `https://031d6d95.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom domain set verified by the deployment workflow: `ndoracle.org`

The workflow checked out the exact release SHA, revalidated the knowledge graph, ran the regression suite, built the static artifact, enforced the no-runtime/static boundary, recorded the artifact digest, rechecked `main`, verified the existing Direct Upload Cloudflare Pages project and then uploaded the artifact.

## Corpus at release

- 10 reviewed v0.1 Concept objects.
- 15 reviewed v0.2 Resource objects.
- Resource inclusion is explicitly not endorsement.
- Resource URL locators require HTTPS.
- The public site exposes `/resources/`, `/tools/`, `/games/`, `/community/` and 15 canonical resource-detail routes.
- `/oracle/` remains a compatibility `noindex` route; no generated-answer authority surface is active.

## Post-deployment verification

The v0.6 live-production verifier was rerun after deployment in GitHub Actions workflow run `33153989610`, job `98843439151`. It completed successfully.

Verified live at `https://ndoracle.org`:

- 36 canonical public routes.
- All 10 concept reading routes.
- `/resources/`, `/tools/`, `/games/`, `/community/`.
- All 15 resource detail routes.
- v0.6 public-reading contract.
- v0.6 15-resource contract.
- Canonical links and indexability on active public routes.
- 404 behaviour.
- `robots.txt`.
- exact sitemap contract.
- `/oracle/` compatibility `noindex` behaviour.
- `www` redirect with path/query preservation.
- passive/static public-surface and security-header requirements enforced by the verifier.

Verifier terminal result:

`Verified 36 canonical routes plus v0.6 reading, resource and production HTTP/public-surface contracts at https://ndoracle.org.`

## Earlier failed dispatch

Deployment run `33169161300` (run #8) did not deploy anything. The `release_sha` input contained leading spaces and the exact-SHA guard rejected it before the Direct Upload job. This failed dispatch is not part of the accepted production identity.

## Acceptance statement

v0.6 is the accepted production release. Future production claims must re-resolve repository main, deployment identity and live verification rather than assuming this state remains current.

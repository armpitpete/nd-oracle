# The Neurodiverse Oracle — Cloudflare Pages Deployment Preflight v0.1

Status: preflight repair candidate; no deployment authorised

Date: 2026-08-10

## Scope

This record tests whether Site Shell v0.1 is structurally ready to enter the protected Cloudflare Pages deployment lane. It does not prove or authorise a live deployment, custom-domain attachment, DNS mutation or public acceptance.

## Repository identity inspected

Preflight began from protected `main`:

`82a26d22019412c41e828ff80c70feaad2872257`

Its Git tree is:

`7b6688c863b5fed512ed3b1977a89afac83c3c6c`

The authorised PR #21 head and GitHub's temporary PR merge commit both resolved to that same tree. The squash-merged `main` also resolves to that tree. Therefore the content tested by PR validation and the Site Shell content established on `main` were identical at preflight start.

This document and the deployment-tooling repair will change the repository commit identity if merged. The actual deployment SHA must therefore be freshly resolved from `main` after this repair is accepted; do not deploy remembered `82a26d22...`.

## Validation evidence

The exact Site Shell tree passed the GitHub `validate` job with:

- Python 3.13;
- source compilation;
- validation of all five knowledge objects;
- evidence, uncertainty, perspective and relationship-route validation;
- 28 regression tests passing.

The build tests execute the real `build_site.build()` function into a temporary `dist/` directory. They verify:

- root page;
- `/understand/`;
- `/tools/`;
- `/games/`;
- `/resources/`;
- `/community/`;
- `/oracle/`;
- `/about/`;
- `/accessibility/`;
- `/privacy/`;
- all five concept routes;
- stylesheet and `_headers` output;
- internal route existence;
- evidence and uncertainty links;
- skip-link/main-navigation accessibility basics;
- absence of JavaScript, forms and inline styles;
- non-mutation of authoritative knowledge objects;
- refusal to overwrite an unmarked output directory.

The Cloudflare tests build the real deployment output and verify the deployment `_headers` file byte-for-byte against the repository source plus the restrictive security policy.

## Static artifact characteristics

The current build is intentionally small and static:

- 15 generated HTML pages;
- one same-origin stylesheet;
- one Cloudflare `_headers` control file;
- one local generated-output marker;
- no JavaScript;
- no Pages Functions;
- no Worker;
- no forms;
- no accounts;
- no analytics or advertising tracker;
- no personal-data collection.

This is far below Cloudflare Pages Direct Upload's current Wrangler limit of 20,000 files and 25 MiB per file.

## Cloudflare contract verification

Checked against current official Cloudflare documentation on 2026-08-10:

- Pages Direct Upload accepts a prebuilt directory through `wrangler pages deploy`.
- `pages deploy` supports `--project-name`, `--branch`, `--commit-hash` and `--commit-dirty`.
- `_headers` in the build output is parsed for static Pages responses.
- `_headers` rules do not govern Pages Functions responses; Site Shell v0.1 has no Functions.
- an apex custom domain requires the domain to be a Cloudflare zone on the same account as the Pages project.
- Direct Upload projects cannot later be converted in-place to Git integration; that would require a new project.

## Preflight finding and repair

The initial release contract used floating `npx wrangler`, which allowed the production deployment tool to change without repository review.

Preflight therefore failed until this was repaired.

The candidate repair pins the reviewed deployment CLI to:

`wrangler@4.114.0`

and makes the Cloudflare regression test require the pinned command.

A future Wrangler update must be an intentional release-tooling change with renewed syntax/compatibility review.

## Deployment command template

After this repair is merged, resolve the new exact protected `main` SHA and build from a clean checkout of that exact commit. The production command template is:

```sh
npx --yes wrangler@4.114.0 pages deploy dist \
  --project-name=nd-oracle \
  --branch=main \
  --commit-hash=<EXACT_CURRENT_MAIN_SHA> \
  --commit-dirty=false
```

Project creation, authentication and deployment are protected production mutations and are not authorised by this record.

## Domain activation default

Unless live Cloudflare state shows a conflict, use:

- primary public hostname: `ndoracle.org`;
- `www.ndoracle.org`: redirect to the apex rather than operate as a second independent site identity.

The custom-domain and redirect configuration must be inspected against the real Cloudflare zone before mutation.

## Live-state unknowns intentionally not guessed

Preflight cannot establish these from repository evidence alone:

- whether a Cloudflare Pages project named `nd-oracle` already exists;
- the current Cloudflare account and zone IDs;
- current Cloudflare authentication/token state;
- current `ndoracle.org` zone settings and DNS records;
- current DNSSEC state;
- current custom-domain attachment state;
- current edge certificate state;
- actual public HTTPS behavior;
- actual live response headers;
- actual live route/navigation behavior.

These are deployment/activation evidence, not repository evidence. They must be checked against the real Cloudflare/public state at the protected deployment stage.

## Protected activation sequence

After this preflight repair is accepted and merged:

1. resolve and record the exact current protected `main` SHA;
2. confirm the accepted PR validation applies to the exact final tree;
3. build `dist/` from a clean checkout of that exact `main`;
4. inspect the generated file manifest and `_headers`;
5. create the Cloudflare Pages Direct Upload project only if it does not already exist;
6. deploy `dist/` with the pinned Wrangler version and exact commit metadata;
7. verify the resulting `pages.dev` deployment identity, HTTPS response, headers and navigation;
8. attach `ndoracle.org` only after the Pages deployment itself is accepted;
9. configure/verify the `www` redirect and DNS state;
10. verify the real apex hostname over HTTPS, including security headers and navigation;
11. only then record public-site acceptance.

DNSSEC, analytics, accounts, forms, community submissions and Oracle/AI activation remain separate decisions and are not implied by Site Shell deployment.

## Current gate

The deployment preflight is **not yet closed** because the Wrangler pinning repair is not on protected `main`.

The next valid action is review/merge of the bounded preflight-repair PR after exact-head CI passes. No Cloudflare mutation should occur before that gate closes.

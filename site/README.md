# ND Oracle website candidate

This directory contains presentation assets for the first reading-first ND Oracle website candidate.

The website is generated from the authoritative knowledge objects in `objects/concepts/`; it does not maintain a second copy of claim text, sources, uncertainties, or perspectives.

## Build

```sh
python scripts/build_site.py
```

The generated site is written to `dist/` and is intentionally not committed.

## Cloudflare Pages release contract

The intended hosting target is Cloudflare Pages using Direct Upload of the already-built `dist/` directory. The repository remains authoritative; Cloudflare receives only generated static assets.

Before any deployment:

1. verify the intended release commit is the exact current `main` commit;
2. require a clean working tree;
3. run the repository validator and complete test suite;
4. build `dist/` from that exact commit;
5. inspect the generated site and security headers;
6. stop for explicit owner authorisation before creating a Pages project or publishing any deployment.

After authorisation, the release command should attach the exact Git identity explicitly:

```sh
npx wrangler pages deploy dist \
  --project-name=nd-oracle \
  --branch=main \
  --commit-hash=<EXACT_MAIN_SHA> \
  --commit-dirty=false
```

Do not substitute a remembered SHA for `<EXACT_MAIN_SHA>`; resolve and verify it immediately before deployment.

Custom-domain attachment and DNS changes are later protected actions and are not implied by a Pages deployment.

## Boundary

This is a non-public candidate only. Repository governance treats publication and deployment as protected changes. Building or reviewing this candidate does not authorise Cloudflare Pages project creation, deployment, DNS changes, a public custom domain, analytics, accounts, forms, personal-data collection, or representation as clinical guidance.

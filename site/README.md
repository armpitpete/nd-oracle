# The Neurodiverse Oracle — Site Shell v0.1

This directory contains the minimal public-site foundation for The Neurodiverse Oracle.

The shell is deliberately plain: semantic HTML, system fonts, restrained colours, visible keyboard focus and no required JavaScript. Its purpose is to make future tools, games, resources, community contribution routes and Oracle integration easy to add without rebuilding the site structure.

The generated Understand pages continue to come from the authoritative knowledge objects in `objects/concepts/`. The website does not maintain a second copy of claim text, sources, uncertainties or perspectives.

## Structural routes

The build reserves these durable top-level routes:

- `/understand/`
- `/tools/`
- `/games/`
- `/resources/`
- `/community/`
- `/oracle/`
- `/about/`
- `/accessibility/`
- `/privacy/`

Tools, games, community features and the Oracle are inactive placeholders in v0.1. Reserving their routes now does not authorise their implementation or weaken their later privacy, security, evidence or governance gates.

## Build

```sh
python scripts/build_site.py
```

The generated site is written to `dist/` and is intentionally not committed.

## Security defaults

The current shell is static and deliberately narrow:

- no JavaScript;
- no forms;
- no accounts;
- no analytics or advertising trackers;
- no personal-data collection;
- no Pages Functions or other server-side runtime;
- restrictive Content Security Policy;
- anti-framing, MIME-sniffing, referrer, permissions and cross-origin headers;
- HSTS emitted with the static deployment headers.

The default policy should remain restrictive. When a future game or tool genuinely needs JavaScript or network access, relax policy only for the smallest necessary route and origin rather than weakening the global site policy.

## Cloudflare Pages release contract

The intended hosting target remains Cloudflare Pages using Direct Upload of the already-built `dist/` directory. The repository is authoritative; Cloudflare receives generated static assets only.

Before any deployment:

1. verify the intended release commit is the exact current `main` commit;
2. require a clean working tree;
3. run the repository validator and complete test suite;
4. build `dist/` from that exact commit;
5. inspect the generated site and security headers;
6. verify the pinned Wrangler version and deployment flags against current Cloudflare documentation;
7. stop for explicit owner authorisation before creating a Pages project or publishing any deployment.

The deployment CLI is deliberately version-pinned. Updating the Wrangler version is a release-tooling change and must be reviewed rather than silently inherited from `npx` latest.

After authorisation, the release command should attach the exact Git identity explicitly:

```sh
npx --yes wrangler@4.114.0 pages deploy dist \
  --project-name=nd-oracle \
  --branch=main \
  --commit-hash=<EXACT_MAIN_SHA> \
  --commit-dirty=false
```

Do not substitute a remembered SHA for `<EXACT_MAIN_SHA>`; resolve and verify it immediately before deployment.

Custom-domain attachment and DNS changes are later protected actions and are not implied by a Pages deployment.

Direct Upload is an intentional release-control choice: Cloudflare does not allow an existing Direct Upload Pages project to be converted to Git integration later. Moving to Git integration would require a new Pages project and a separately reviewed migration.

## Boundary

Building or reviewing Site Shell v0.1 does not authorise Cloudflare Pages project creation, deployment, DNS changes, custom-domain attachment, analytics, accounts, forms, community data collection, an Oracle chatbot, AI-generated answers, or representation as clinical guidance.

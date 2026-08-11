# The Neurodiverse Oracle — public site v0.2

This directory contains the presentation layer for the public ND Oracle site.

The v0.2 completion pass changes the product stance from “site shell with future-feature placeholders” to a small but intentional reading product built around the knowledge that actually exists now.

The generated Understand pages continue to come from the authoritative knowledge objects in `objects/concepts/`. The website does not maintain a second copy of claim text, sources, uncertainties or perspectives.

## Current public journey

A visitor can now:

1. start from an ordinary-language question on the homepage;
2. browse the five current topics under `/understand/`;
3. read a short summary and scope before encountering technical detail;
4. open the evidence and uncertainty behind individual statements only when wanted;
5. inspect different perspectives, related topics, sources and provenance;
6. recover from a bad URL through a useful `404.html` page;
7. discover indexable routes through `sitemap.xml` and `robots.txt`.

Primary navigation contains only active destinations:

- `/understand/`
- `/how-it-works/`
- `/about/`

Accessibility and privacy remain in the footer.

The old `/tools/`, `/games/`, `/resources/`, `/community/` and `/oracle/` routes remain as non-indexed compatibility pages so existing links do not become dead ends. They are deliberately absent from primary navigation and the sitemap until there is useful content to put there.

## Design stance

The public site remains deliberately calm and reading-first:

- semantic HTML;
- system fonts;
- restrained colours;
- visible keyboard focus;
- reading-width content;
- ordinary-language entry points;
- native `<details>` controls for progressive disclosure;
- no required JavaScript;
- no empty feature catalogue presented as a finished product.

## Build

```sh
python scripts/build_site.py
```

The generated site is written to `dist/` and is intentionally not committed.

## Security and privacy defaults

The current site remains static and deliberately narrow:

- no JavaScript;
- no forms;
- no accounts;
- no analytics or advertising trackers;
- no personal-data collection;
- no Pages Functions or other server-side runtime;
- restrictive Content Security Policy;
- anti-framing, MIME-sniffing, referrer, permissions and cross-origin headers;
- HSTS emitted with the static deployment headers.

The default policy should remain restrictive. When a future feature genuinely needs JavaScript or network access, relax policy only for the smallest necessary route and origin rather than weakening the global site policy.

## Search decision

A separate search runtime is not a v0.2 completion blocker while the public corpus contains only five topic pages. The homepage provides ordinary-language entry questions and `/understand/` exposes the full corpus in one scan.

Search should be introduced when it saves real navigation work rather than adding a JavaScript/runtime dependency before the corpus needs it.

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

This v0.2 presentation pass does not mutate authoritative knowledge objects, create accounts, collect community data, add analytics, introduce an Oracle chatbot, or represent the site as clinical guidance.

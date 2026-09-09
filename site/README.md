# The Neurodiverse Oracle — public presentation

This directory contains the shared presentation layer for ND Oracle. Governed knowledge remains in the repository objects, evidence records and discovery contracts; the site does not become a second authority.

## Current journey

A visitor can start from:

- **Find** — describe a problem in ordinary language;
- **Questions** — browse practical needs by area of life;
- **Resources** — inspect tools, services, organisations, games, books and practical help;
- **Topics** — understand a concept without already knowing the specialist vocabulary;
- eight Home areas of life;
- Places and the complete A–Z as deliberate secondary routes.

Home is intentionally an orientation surface, not a catalogue. Legacy per-topic/question shortcut inventories are not duplicated there.

## Presentation contract

- shared CSS lives in `site/styles.css`;
- shared generated shell/components live in `scripts/build_site.py`;
- Find uses the bounded same-origin `scripts/discovery_browser.js` enhancement;
- Evidence remains statically rendered;
- canonical content remains useful without JavaScript;
- the stylesheet URL is content-versioned from the stylesheet bytes.

## V2 composition

The current doctrine is defined by:

- `docs/ND_UX_V2_4_FUNCTIONAL_BASELINE.md`;
- `docs/ND_UX_V2_5_DESIGN_SYSTEM.md`.

The governing target is **quiet, obvious and controllable**.

Discovery/index pages use desktop width when overview helps. Long-form reading keeps a controlled measure. Page headings are directional landmarks rather than hero cards. Cards and enclosing panels are exceptional rather than the default page grammar.

Recognition precedes taxonomy. Where useful, unfamiliar words may be broken into bounded learning aids such as **mono – trop – ism**, while the governed definition and evidence route remain authoritative.

## Accessibility and privacy

The presentation preserves:

- semantic HTML and landmarks;
- skip navigation and visible keyboard focus;
- responsive reflow;
- forced-colour support;
- readable system fonts;
- native disclosure controls;
- no autoplay or surprise motion;
- no accounts;
- no analytics or personalised ranking;
- no stored Find queries;
- no AI-generated answer authority.

## Build

```sh
python scripts/build_site.py
```

Generated output is written to `dist/` and is not committed.

## Release boundary

Merges and production deployments remain protected. A presentation candidate must pass exact-head validation and hostile/no-drift review. Final V2 freeze additionally requires real ND task evidence under `docs/ND_UX_V2_USER_TEST_PROTOCOL.md`.

The production release contract remains Direct Upload from an exact current `main` SHA. Before deployment, verify the exact commit, clean tree, validation suite, built artifact and existing Cloudflare project/domain state, then stop for **explicit owner authorisation**.

After that separate protected authorisation, the guarded release path uses the pinned CLI:

```sh
npx --yes wrangler@4.114.0 pages deploy dist \
  --project-name=nd-oracle \
  --branch=main \
  --commit-hash=<EXACT_MAIN_SHA> \
  --commit-dirty=false
```

Do not substitute a remembered SHA for `<EXACT_MAIN_SHA>`. Custom-domain attachment and DNS changes are later protected actions and are not implied by a Pages deployment.

An exact live deployment SHA must come from protected deployment evidence; do not infer it from visible V2 page markers.

# The Neurodiverse Oracle — Site Shell v0.1

Status: implementation candidate

## Decision

The previous project rule **“No UI yet”** is superseded only for a minimal structural public site shell.

This does **not** authorise an Oracle chatbot, AI-generated answers, graph interface, elaborate application UI, accounts, public comments or other community-network features.

The project now proceeds in two parallel lanes:

1. **ND Commons / Site Shell** — useful public structure, tools, games, resources and contribution routes.
2. **Oracle Knowledge System** — repository-first knowledge objects, validation, evidence, uncertainty, provenance and later search/graph infrastructure.

A later integration lane may connect the two. The website consumes validated Oracle knowledge; it does not replace the Oracle as the knowledge authority.

## Site-shell purpose

Build the important structure once so future features can be added without navigation or layout redesign.

The shell should remain:

- calm;
- small-text but readable;
- soft-coloured;
- semantic;
- keyboard accessible;
- responsive;
- functional without JavaScript;
- easy to extend;
- deliberately light on CSS.

## Durable top-level routes

- `/understand/` — human-readable knowledge pages backed by repository objects.
- `/tools/` — future practical tools.
- `/games/` — future games and interactive experiments.
- `/resources/` — future catalogue of apps, books, organisations, services and communities.
- `/community/` — future corrections, suggestions and lived-experience contribution routes.
- `/oracle/` — reserved for later Oracle integration.
- `/about/`
- `/accessibility/`
- `/privacy/`

The five current root concept objects render under `/understand/<object-id>/`.

## Extension rules

### Tools and games

Interactive features may add JavaScript later, but only where necessary. A tool or game must not force JavaScript requirements onto reading pages or the rest of the site.

### Resources

A resource listing is not an endorsement. Catalogue data and evidence claims must remain distinguishable.

### Community

Community contribution does not automatically become factual knowledge. Contributions may become candidate material for later review, research or knowledge-object updates.

### Oracle

AI must not become the source of truth. Any later Oracle interface must preserve routes back to repository knowledge, evidence, uncertainty and revision history.

## v0.1 acceptance criteria

Site Shell v0.1 is structurally acceptable when:

- every durable route builds;
- navigation works across every generated page;
- internal links are regression-tested;
- the five current concepts remain rendered from authoritative objects;
- evidence and uncertainty routes remain visible on concept claims;
- the build does not mutate knowledge objects;
- the shell works without JavaScript;
- there are no forms or personal-data collection;
- keyboard focus is visible;
- a skip link and semantic navigation exist;
- responsive layout works without an application framework;
- styling uses a small shared token set;
- deployment security headers are regression-tested;
- publication remains a separate protected action.

## Non-goals for v0.1

- search;
- AI answers;
- graph exploration;
- user accounts;
- profiles;
- public comments;
- direct messages;
- analytics scripts;
- advertising;
- personalisation;
- community moderation infrastructure;
- polished visual branding.

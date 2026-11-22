# ND Oracle Find — Joomla module v1.0.0

This small Joomla 6 site module renders the **existing browser-local Find interface**. It does not create a new search engine, call remote search services, or change governed search rules.

## Dependencies and boundary

- Joomla 6.2 installed, with the `content/loadmodule` plugin enabled.
- Reviewed static assets remain at `/media/ndoracle/find.js` and `/media/ndoracle/find-index.json`. These are **not** bundled here because the original governed evaluator and catalogue remain the authority.
- The current bootstrap expects policy version `1.1` and an exact **363-entry** catalogue; changing the catalogue requires a reviewed update of its compatibility guard.
- Only **one Find interface per page** is supported by the frozen evaluator's stable HTML element IDs.
- All query text remains in the browser; only the static index and evaluator are requested. Do not place the server-submitted Joomla Smart Search form alongside this interface.

## Installation and embedding

Zip the **contents** of this directory so `mod_ndoracle_find.xml` is at the archive root. Install the archive via Joomla **System → Install → Extensions** or the Joomla 6 native CLI `extension:install --path=...` (normal public-asset file modes, e.g. 0644 for JS/JSON and 0755 for directories). The Joomla extension installer creates a **new unpublished module instance**; publish it, assign it to all menus (menuid 0), and embed its actual module ID in the dedicated Find article using `{loadmoduleid N}`. Do not add another copy of the search controls to that article.

Staging observation (22 November 2026): extension ID 253, module ID 113, article ID 742. These are **installation-specific** and must not be hardcoded in another Joomla instance.

The global template `media/templates/site/cassiopeia/js/user.js` previously held the same bootstrap. On staging it was replaced with a backed-up no-op after the module's JavaScript began loading. Retain the old template file in a secure backup until rollback is no longer needed; do not leave two active bootstraps.

## Staging test evidence

- Exact evaluator unchanged: SHA-256 `8376a7fe0dbfb624260a8da322b1e26bd82e085c957fe94645aa22a9d194e666`.
- Staging `/find` renders one input, button and results container and one module bootstrap.
- Index (363 entries), evaluator JS and module bootstrap each respond HTTP 200.
- Node/DOM simulation covers governed results, clinical restriction, blank query, Enter-key activation and no query transmission.
- The 450 production sitemap routes were independently checked before this module migration: 262 direct 200, 188 one-hop redirects to 200.

**Still required before release:** human browser testing on authenticated HTTPS staging (keyboard, focus, narrow layout, no-JS fallback), remaining page/content/evidence/asset parity, off-server restore and explicit cutover approval under issues #177 and #178.

## Rollback

On Oracle staging, the article's original text and template bootstrap were backed up under `/home/ndoracle/private-migration-backups/find-module-v1-20261122/`. Restore article 742, restore Cassiopeia `user.js`, unpublish module 113, and then verify `/find` and its assets. Do **not** uninstall or delete governed source/evaluator files just to roll back the module.

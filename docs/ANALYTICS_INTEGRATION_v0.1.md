# The Neurodiverse Oracle — Analytics Integration v0.1

Status: proposal only; not deployed by this document or branch

## Purpose

This lane adds privacy-first readership measurement to the public Site Shell without turning the site into an account system, advertising surface, behavioural-profile system, or JavaScript-dependent application.

It supersedes the earlier **no analytics scripts** rule only for this bounded Merrin Analytics integration. The requirement that the public site remain fully useful without JavaScript is preserved.

## Collector

The only permitted analytics origin is:

`https://collect.merrinworld.uk`

The generated site loads:

```html
<script src="https://collect.merrinworld.uk/beacon.js" data-site="nd_oracle" defer></script>
```

The Content Security Policy permits scripts and collector requests only to that origin. Inline script, `unsafe-inline`, `unsafe-eval`, forms and additional script origins remain prohibited.

## Data boundary

The analytics system may record:

- site identifier;
- page path with query string and fragment removed by the collector;
- page title;
- referring hostname after collector reduction;
- broad browser/device class;
- approximate town, region and country supplied by Cloudflare;
- an aggregate site-local visitor estimate.

For visitor estimation, the browser may hold a random token scoped to this site. The collector must not persist the raw token or a full token hash. It reduces the token immediately to the aggregate visitor sketch defined by `armpitpete/merrin-analytics`.

The analytics system must not intentionally create a cross-site visitor identity.

## Excluded

This integration does not authorise storage of:

- IP addresses or IP-derived identifiers;
- the raw browser visitor token;
- a full visitor-token hash;
- precise coordinates;
- form or query contents;
- health information;
- accounts, profiles or personal identities;
- advertising or remarketing identifiers;
- cross-site visitor identities.

## Functional boundary

If JavaScript is disabled, blocked or the collector is unavailable:

- every public route remains readable;
- navigation remains usable;
- knowledge content remains unchanged;
- no user-facing function is lost except analytics collection itself.

## Release boundary

This branch and any pull request created from it are repository proposals only.

Production activation requires a separately accepted Merrin Analytics collector release that allowlists `ndoracle.org`, followed by the normal ND Oracle exact-commit validation and guarded deployment process. Repository merge, D1 migration, analytics deployment and ND Oracle production deployment remain separate protected actions.

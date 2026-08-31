# ND Oracle builder release identity v1.2

Status: bounded engineering contract

## Purpose

`scripts/release_identity.py` is the canonical source for the human-facing public-site builder label printed by the active builder command.

The current value is `v1.2`. This describes the repository/public-site builder contract now that the v1.2 need-coverage slice is on protected `main`. It is deliberately separate from production acceptance evidence.

## Production evidence remains separate

`docs/PRODUCTION_STATE_v1.1.md` remains the immutable record of the currently accepted production deployment until an exact-SHA v1.2 deployment and fresh live verification are separately authorised, performed and accepted.

Changing `PUBLIC_SITE_RELEASE` does not deploy anything, does not establish production acceptance and must never be used as a substitute for exact-SHA production evidence.

## Repository version files

The existing repository `VERSION` and `CHANGELOG.md` retain their established meaning. This contract does not reinterpret the historical `0.1.0` line as the public-site release number and does not introduce repository-wide semantic versioning.

## Builder boundary

The identity module may affect only human-facing build-command output. It must not alter:

- governed Concept, Resource, Question or Evidence objects;
- object schemas or validation semantics;
- discovery eligibility, ranking, clinical boundaries or jurisdiction handling;
- generated HTML, JavaScript, headers, sitemap or other public artifact content;
- privacy, telemetry or query handling;
- provenance semantics;
- deployment workflow or production state.

The active builder remains the current self-contained module for site-generation behaviour. Release-label maintenance must not require replacing or regenerating that builder monolith wholesale.

## Acceptance

A candidate passes only when:

1. direct builder execution prints the current `v1.2` builder identity;
2. the stale `public site v1.0 candidate` label is absent;
3. the active builder remains larger than 100 KB and retains the v1.2 content/navigation changes already on `main`;
4. all 125 governed objects validate and freshness remains green;
5. frozen public compatibility and the complete regression suite pass;
6. generated public output is unchanged by the identity mechanism;
7. the exact diff demonstrates no governed-content, discovery, privacy or deployment change.

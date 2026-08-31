# ND Oracle builder release identity v1.1

Status: bounded engineering contract

## Purpose

`scripts/release_identity.py` is the canonical source for the human-facing public-site release label printed by the active builder command.

The current value is `v1.1`.

This identity describes the active public-site builder contract. It is deliberately separate from production acceptance evidence.

## Production evidence remains separate

`docs/PRODUCTION_STATE_v1.1.md` remains the immutable record of the accepted production deployment, including its exact source SHA, workflow evidence and generated artifact digest.

Changing `PUBLIC_SITE_RELEASE` does not deploy anything, does not establish that a release has been accepted in production and must never be used as a substitute for exact-SHA production evidence.

## Repository version files

The existing repository `VERSION` and `CHANGELOG.md` retain their established meaning. This change does not reinterpret the historical `0.1.0` line as the public-site release number and does not introduce a new repository-wide semantic-versioning contract.

## Builder boundary

The identity module may affect only human-facing build-command output. It must not alter:

- governed Concept, Resource, Question or Evidence objects;
- object schemas or validation semantics;
- discovery eligibility, ranking, clinical boundaries or jurisdiction handling;
- generated HTML, JavaScript, headers, sitemap or other public artifact content;
- privacy, telemetry or query handling;
- provenance semantics;
- deployment workflow or production state.

The active builder remains the current self-contained module for site-generation behavior. Release-label maintenance must not require replacing that generated monolith wholesale.

## Acceptance

A candidate passes this contract only when:

1. direct builder execution prints the current `v1.1` public-site identity;
2. the stale `public site v1.0 candidate` label is absent;
3. the active builder retains its full-size current architecture rather than being truncated or regenerated accidentally;
4. frozen public compatibility and the complete regression suite pass;
5. the exact diff demonstrates that generated public content and governed knowledge behavior are unchanged.

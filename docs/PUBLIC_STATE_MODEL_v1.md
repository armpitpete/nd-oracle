# ND Oracle public-state model v1

Date: 2026-09-09

## Purpose

ND Oracle has three distinct states. They must never be collapsed into one ambiguous phrase such as “current production”.

## 1. Knowledge baseline

Authority: `contracts/current-production.json`.

This identifies the last accepted governed knowledge deployment: governed objects, canonical routes, evidence coverage, discovery scope and exact accepted source identity. Presentation-only work must not rewrite this evidence.

Current accepted knowledge baseline:

- 366 governed objects;
- 450 canonical routes;
- 49/49 governed Claims covered;
- 0 evidence gaps;
- source SHA `8e60f264adfda2822312a05e835bc352ef263225`.

## 2. Presentation baseline

Authority: repository history plus `contracts/current-public-state.json`.

This records the accepted presentation baseline from which the next public-interface candidate is derived. ND-UX-V2.4 is merged through PRs #165, #166 and #167, with baseline source SHA `0065ab8000bbb0020aa221f084525116f436b373`.

A presentation candidate may move ahead of the accepted knowledge source without changing knowledge authority.

## 3. Live deployment state

Authority: a protected deployment record plus fresh network verification.

Visible live markers may establish that a presentation family is live. They do not by themselves prove the exact deployed commit, artifact hash or Cloudflare deployment identity. Until those are reconciled, the live presentation must be described as observed but deployment-identity-unreconciled.

## Invariants

1. Knowledge authority cannot be compressed into a presentation release.
2. Presentation changes cannot silently become governed-content changes.
3. A visible live interface cannot be assigned an exact deployed SHA without deployment evidence.
4. Historical production records remain immutable.
5. A final V2 Public Baseline requires exact-head CI, human ND task evidence, protected merge, protected deployment, live verification and final state reconciliation.

## Current consequence

`CONTENT_GAP_MAP_v1.4.md` is historical because it describes the earlier 325-object/409-route state. `CONTENT_GAP_MAP_v2.0.md` is the current editorial audit against the 366-object/450-route knowledge baseline.

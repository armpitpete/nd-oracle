# International three-package architecture review v1

Date: 2026-09-05
Status: candidate conclusion after Republic of Ireland + Australia + Canada package implementation

## Observed patterns

Across the three packages the repeated needs are:
- country identity;
- subnational implementation where material;
- explicit source scope;
- additive discovery aliases/scope;
- local/national non-inheritance;
- high-change freshness ownership.

## Sidecar verdict

**Retain additive jurisdiction sidecars. Do not change the core object schema.**

The three packages do not expose a field that cannot be represented safely through:
- ordinary governed Question/Resource fields;
- audience/scope wording;
- jurisdiction sidecars;
- source matrices;
- exact scope provenance.

A core schema migration would currently add migration and certainty risk without solving a demonstrated validation failure.

## Translation

No new translation subsystem is justified by these three packages. Ireland, Australia and the selected Canada sources are available in English. The existing rule remains: local-language authoritative evidence is preferred where material, machine translation is research assistance rather than provenance, and translation uncertainty must remain visible.

## Freshness

Country packages should mark national architecture sources separately from volatile local implementation sources. Adult ADHD implementation in Ireland and state/provincial service arrangements are examples of shorter-cadence material.

## Next international rule

Do not begin mass-country expansion. Future countries remain evidence-driven and one-package-at-a-time.

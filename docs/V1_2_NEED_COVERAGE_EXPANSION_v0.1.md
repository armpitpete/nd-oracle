# ND Oracle v1.2 — Need Coverage Expansion v0.1

Status: implementation contract

Baseline: protected `main` at `b4f37ca00fb06c46a5b7cde3278d985259f21d65`.

## Goal

Close one evidence-backed jurisdiction gap in the existing Education & study need area: higher-education disability-support navigation currently exists for England but not for Scotland, Wales or Northern Ireland.

## In scope

1. Scotland Disabled Students' Allowance / disability-related higher-education support route.
2. Wales Disabled Students' Allowance / disability-related higher-education support route.
3. Northern Ireland Disabled Students' Allowance / disability-related higher-education support route.
4. One governed Resource and one practical Question for each nation.
5. Minimum deterministic discovery phrases and scope-provenance declarations for those six new routes.
6. Tests that prove each nation's query selects the compatible practical route and cannot leak a different nation's scoped route.

## Out of scope

- new Concepts or schemas;
- adult autism or ADHD assessment expansion;
- healthcare-adjustment expansion;
- employment or benefits expansion;
- daily-life content expansion;
- ranking-weight changes;
- clinical-boundary changes;
- orientation or personalised ranking;
- external search, query persistence, analytics, profiling or AI answer generation;
- deployment or production mutation.

## Content rules

The new Resources are access/navigation entries, not endorsements and not individual entitlement decisions. Avoid freezing volatile annual maximum amounts into the objects. State that rules, evidence requirements and application processes can change and direct users to the current official source.

Questions must use the existing boundary: **Relevant to inspect, not recommended**. They should identify the current nation-specific route while preserving uncertainty about individual eligibility, approved support and institutional support available alongside DSA.

## Source authorities checked 2026-08-31

- Scotland: Student Awards Agency Scotland Disabled Students' Allowance guidance.
- Wales: Student Finance Wales Disabled Students' Allowance guide for 2026–27.
- Northern Ireland: nidirect Financial help for disabled students, routing to Student Finance NI.

Full source locators and the audit rationale are recorded in `docs/V1_2_NEED_COVERAGE_AUDIT_v0.1.md`.

## Acceptance

- exactly 125 governed objects: 20 Concepts, 61 Resources, 41 Questions and 3 Evidence;
- all six new objects validate under existing v0.2 schemas;
- the existing England route remains unchanged;
- Scotland, Wales and Northern Ireland practical study-support probes select their matching new Question/Resource rather than travel, benefits or workplace material;
- incompatible nation-specific routes are excluded under requested-jurisdiction containment;
- all previous frozen discovery/clinical/privacy/provenance tests continue to pass;
- public compatibility changes only where required to expose the three new Questions and Resources through normal generated navigation;
- exact diff contains no deployment change;
- hostile review passes before the protected merge gate.

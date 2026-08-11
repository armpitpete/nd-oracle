# ND Oracle Schema Contract v0.2

Status: implementation candidate. This contract is additive to schema v0.1 and does not migrate or modify authoritative knowledge objects.

## Purpose

Schema v0.2 implements the accepted six-object knowledge model while preserving the repository's provenance-first boundaries:

- Concept
- Evidence
- Question
- Resource
- Perspective
- Experience

Claims remain embedded, stable records. They are not top-level objects. Source identity belongs to Evidence objects; claim-specific evidential meaning belongs to Evidence Contribution records.

## Compatibility

During the compatibility phase:

- existing `schema_version: "0.1"` Concept objects continue to validate against `object-v0.1.json`;
- `schema_version: "0.2"` objects validate through `object-v0.2.json`;
- unknown schema versions fail closed;
- test fixtures are never counted as authoritative objects;
- no v0.1 object is rewritten merely because v0.2 exists.

The authoritative repository remains under `objects/`. v0.2 fixtures live only under `tests/fixtures/v0.2/`.

## Files

```text
schema/
├── object-v0.1.json
├── schema-v0.1.md
├── object-v0.2.json
├── schema-v0.2.md
├── common-v0.2.json
└── types/
    ├── concept-v0.2.json
    ├── evidence-v0.2.json
    ├── question-v0.2.json
    ├── resource-v0.2.json
    ├── perspective-v0.2.json
    └── experience-v0.2.json
```

`object-v0.2.json` is the top-level dispatcher. The validator loads every v0.2 schema into an in-process registry, so `$ref` resolution does not depend on network access.

## Common envelope

Every v0.2 object has `schema_version`, stable `id`, bounded `type`, lifecycle `status`, and provenance. Question status uses its own bounded inquiry lifecycle: `open`, `partially_resolved`, `resolved`, or `not_currently_answerable`.

## Claims

Only Concept and Resource may own `claims` in v0.2. A Claim record requires stable local identity, exact proposition text, claim-local confidence, one or more Evidence object IDs, one or more local Uncertainty records, and zero or more standalone Question IDs.

Canonical cross-object claim references use `<object-id>#<claim-id>`. The validator rejects malformed references, missing owners, missing claims, non-claim-owning targets, and ambiguous duplicate local IDs.

## Uncertainty and Question

A local Uncertainty is an embedded limitation or unresolved boundary tied to a specific Claim, Evidence Contribution, or relation. It requires a stable local ID, statement, why it matters, and a reopening or reduction condition.

A Question is standalone only when the inquiry is independently reusable, navigable, or researchable. Local uncertainties do not need standalone Questions.

## Evidence

An Evidence object represents source identity plus one or more Evidence Contributions. Source identity includes title, source kind, citation, typed locator, date, accessed date, authorship, provenance, and optional funding/conflicts.

Supported locator types are HTTPS URL, DOI, ISBN, archive identifier, repository/dataset identifier, and explicit offline citation.

A Contribution requires stable local ID, exact `claim_ref`, bounded role, non-blank finding, population/context, methodology, and zero or more local limitations. Roles are `compatible`, `supportive`, `discriminating`, `contradictory`, `falsifying`, and `inconclusive`.

The same Evidence object may contribute differently to different claims. A role is never treated as proof by itself.

## Resources

A Resource describes something people may use or access. Resource existence does not imply efficacy. Resources may own Claims where availability, function, efficacy, safety, cost, access, eligibility, compatibility, or another testable proposition needs an evidence and uncertainty route. A Resource may also have no Claims.

Commercial ownership and conflicts remain distinct from evidential support.

## Perspectives

A Perspective is an attributed viewpoint, framing, or position. It cannot own generic Claims in v0.2. `held_by` includes both a name and bounded representation scope. Supporting or disagreement material uses typed references. Citing Evidence does not convert a Perspective into fact.

## Experiences

An Experience represents an aggregated or published experiential pattern. It is not a diagnosis, causal conclusion, prevalence estimate, or efficacy claim. Contradictory and minority Experiences can coexist. The schema does not require personal identity data.

## Typed references

Important cross-object references either use a field whose target type is fixed, such as `evidence_ids`, or an explicit typed reference containing `type` and `id`. The validator rejects missing targets and target-type mismatches.

## Relations

v0.2 relation records contain bounded relation type, typed target, reason, confidence, Evidence IDs, local uncertainties, and Question IDs.

Initial vocabulary is `broader_than`, `narrower_than`, `associated_with`, `experienced_as`, `supported_by`, `challenged_by`, `described_by`, `used_for`, `debated_by`, and `questions`.

`broader_than` and `narrower_than` are Concept-to-Concept structural relations and require reciprocal inverse records. No other inverse is inferred automatically. Open-ended causal relation types are not part of v0.2.

## Repository validation

`scripts/validate.py` validates every schema as JSON Schema 2020-12, dispatches by `schema_version`, preserves established v0.1 semantic checks, validates v0.2 path/type consistency, enforces global/local ID uniqueness, resolves typed and exact Claim references, enforces Claim ↔ Evidence Contribution routing, checks Question/Evidence/Experience/relation references, enforces structural reciprocity, and fails closed on unsupported schema versions.

The CLI validates authoritative objects only. Tests can explicitly add `tests/fixtures/v0.2/` to the validation graph while the authoritative object count remains unchanged.

## Migration boundary

This implementation does not migrate authoritative v0.1 Concepts.

The validator exposes a deterministic v0.1 preservation inventory for migration-proof tests. It enumerates claim text and confidence, source routes, uncertainty routes, Perspectives, scope distinctions, relations, ecosystem entry points, and provenance so a later migration proof cannot silently omit known semantic work.

Any actual mapping of an authoritative v0.1 Concept into v0.2 remains a separate protected lane requiring review and acceptance before mutation.

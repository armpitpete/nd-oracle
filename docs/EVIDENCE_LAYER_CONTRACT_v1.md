# ND Oracle Evidence Layer Contract v1

Status: implementation contract for the Evidence Layer v1 programme.

## 1. Purpose

The Evidence layer exists so that a reader can inspect **why an exact ND Oracle claim is stated the way it is**, what source bears on that claim, what the source actually contributes, what limitations remain, and what would cause the claim to be revisited.

It is not an endorsement engine, citation counter, source-prestige score, recommendation system or substitute for clinical/legal/professional judgement.

The Evidence layer must answer:

1. What exactly is the claim?
2. Which governed object owns it?
3. Which source or sources bear on that exact wording and scope?
4. What role does each source play for that claim?
5. What population/context and method produced the relevant finding?
6. What limitations or contradictory evidence remain?
7. What confidence applies to the exact claim?
8. When was the source/interpretation last reviewed?
9. What would cause the claim to be reopened, weakened or changed?

## 2. Two accepted evidence models

ND Oracle currently has two authoritative evidence structures.

### 2.1 Legacy v0.1 embedded evidence

Reviewed v0.1 Concept objects contain:

- stable Claims;
- embedded source records;
- reciprocal `claim.source_ids` ↔ `source.supports` routes;
- explicit uncertainty routes;
- perspectives and provenance.

Those routes remain authoritative. Evidence Layer v1 **does not duplicate or silently migrate them** simply to increase the count of top-level Evidence objects.

Public Evidence projection may derive a readable source page from the existing source record, but the authoritative data remains the v0.1 Concept until a separately governed migration occurs.

### 2.2 Normalized v0.2 Evidence

v0.2 Evidence objects represent a source identity plus one or more claim-specific Evidence Contributions.

A normalized Contribution identifies:

- an exact `claim_ref`;
- a bounded role;
- the finding relevant to that claim;
- population/context;
- methodology;
- contribution-level limitations.

The role belongs to the Contribution, **not globally to the source**.

## 3. Serious-claim threshold

Resource identity, access route, declared purpose, ordinary catalogue description and clearly attributed first-party product facts may be recorded without converting the Resource into an efficacy/safety/legal/diagnostic claim.

A separate governed Claim/Evidence/Uncertainty route is required when ND Oracle asserts a materially testable proposition whose truth matters beyond merely identifying the source or resource. Typical triggers include:

- diagnosis or diagnostic boundaries;
- prevalence/frequency;
- efficacy or benefit;
- safety/harm;
- mechanism or causation;
- legal entitlement or legal interpretation;
- comparative accessibility quality;
- eligibility conclusions;
- historical attribution/date claims;
- materially consequential product/service facts that are not merely attributed first-party descriptions.

When uncertain, prefer narrower descriptive wording or `claims: []` rather than manufacturing a weak Claim.

## 4. Claim classes and evidential standards

Machine-readable rules live in `contracts/evidence-layer-v1.json`.

### Source identity / availability

A current first-party source can be enough for a tightly bounded statement about its own identity, published feature, availability or access route.

It cannot independently establish efficacy, safety, accessibility quality or personal fit.

### Legal / official guidance

Current authoritative material can establish what legislation, a regulator, government route or official guidance says.

That does not determine an individual case, entitlement or legal dispute.

### Diagnostic / definition

Use current authoritative clinical/diagnostic guidance and, where a claim extends beyond one authority's wording, appropriate independent synthesis. No single checklist, cognitive measure or group difference becomes an individual diagnosis.

### Prevalence / frequency

Population, time, sampling frame and measurement must be explicit. Community participation or reported experience frequency is not prevalence.

### Association

Observational evidence may establish association when appropriately designed and scoped. Association is not causation.

### Efficacy / benefit

Broad efficacy claims require comparative outcome evidence appropriate to the intervention/outcome, with person-defined outcomes, burden and adverse effects considered where relevant. Testimonials, popularity and vendor claims are insufficient.

### Safety / harm

Safety requires safety-specific evidence and relevant warnings/adverse-event information. Absence of a reported harm is not proof of safety.

### Mechanism / causation

Mechanistic claims require converging evidence. Causal claims require designs capable of supporting causal inference and explicit treatment of plausible alternatives.

### Historical

Prefer primary/archival sources and careful scholarship. Exact date precision must not exceed the evidence.

### Product / service feature

First-party documentation may support current feature existence when commercial interest is explicit. Developer-declared accessibility metadata is not independent accessibility certification.

### Lived experience

Experience evidence can establish that an experience was reported and can support bounded patterns within its sampled context. It does not automatically establish prevalence, mechanism, diagnosis or universality.

## 5. Source quality

Source quality is claim-relative.

- `authoritative_guidance`: strong for what current rules/guidance say; not automatically strong for outcomes.
- `peer_reviewed`: assess design, measurement, population, analysis, replication and relevance. Publication status is not a score.
- `dataset`: assess provenance, coverage, definitions, missingness, sampling and construct validity.
- `community`: strong for a community's own position/service/experience; not automatically population-representative.
- `lived_experience`: strong for the experience as reported; not for prevalence/causation by itself.
- `historical`: assess provenance, contemporaneity, edition/version and date certainty.
- `book`: evidential value depends on genre, sourcing and exact claim.
- `commercial`: useful for first-party product/service facts with conflicts explicit; not independent outcome evidence.
- `practical`: useful for bounded practice description; outcome claims need stronger support.
- `other`: requires explicit editorial justification.

Official status, peer review, institutional prestige and citation count must never automatically set claim confidence.

## 6. Evidence roles

Allowed normalized v0.2 roles:

- `compatible`
- `supportive`
- `discriminating`
- `contradictory`
- `falsifying`
- `inconclusive`

A bare role is insufficient. The Contribution must explain the bounded finding that justifies the role.

A source may be supportive for one claim and inconclusive or contradictory for another.

## 7. Confidence calibration

Confidence applies only to the exact claim text and scope.

- **High** — strong support for the bounded proposition, with important contrary evidence considered and no known disagreement large enough to require material rewording.
- **Moderate** — supported, but important limits, indirectness, transfer problems or unresolved uncertainty constrain the proposition.
- **Low** — some support exists but it is limited, indirect, fragile or under-replicated.
- **Contested** — credible evidence or interpretation materially disagrees.
- **Not applicable** — epistemic confidence is not the right description for that record; it must not be used to avoid appraisal.

A material confidence change requires an evidence-backed rationale preserved in provenance/commit history.

Source count is **not** a truth vote.

## 8. Uncertainty and contradiction

Every serious Claim retains an uncertainty/limitation route under its accepted schema.

Uncertainty should identify the actual epistemic problem, such as:

- sample/population mismatch;
- method or measurement weakness;
- jurisdiction mismatch;
- time/version sensitivity;
- indirectness;
- unresolved alternative explanation;
- conflicting evidence;
- poor generalisability;
- missing adverse-effect information.

Generic boilerplate should be rejected during review.

Contradictory or falsifying Evidence remains visible. It is not deleted because other evidence supports the claim.

Material contradiction triggers review of wording, scope and confidence.

A Perspective records an identifiable framing/interpretation. A factual proposition is not converted into truth merely because it appears in a Perspective.

## 9. Jurisdiction and applicability

Evidence must not silently travel farther than its source.

Review must consider, when relevant:

- country/nation/jurisdiction;
- health/education/employment system;
- age;
- diagnostic/clinical population;
- communication/support profile;
- sample selection;
- time period;
- platform/version;
- service eligibility.

England must not silently become UK. Great Britain must not silently include Northern Ireland. Adult evidence must not silently become child evidence. Clinical samples must not silently become universal neurodivergent-population claims.

## 10. Freshness and lifecycle

Evidence review freshness is about **whether ND Oracle's interpretation and access/source route are current**, not whether an old academic paper has ceased to exist.

Evidence Layer v1 uses source-kind review intervals:

- authoritative guidance / commercial / community / practical: 180 days;
- dataset / other: 365 days;
- peer-reviewed / lived experience: 730 days;
- book / historical: 1095 days.

Event-driven re-review overrides the interval when:

- legislation/rules change;
- a service or product materially changes;
- a source is corrected, retracted or withdrawn;
- a new edition/version supersedes the cited one;
- a materially contradictory source emerges;
- a claim's scope or wording changes.

Retracted/superseded evidence should remain inspectable as deprecated history where possible; claims are re-reviewed rather than silently rewired.

Immutable web snapshots/hashes are **not mandatory by default**. Consider them only for high-consequence mutable web evidence where exact wording matters and licensing/copyright/storage rules permit preservation.

## 11. Date precision and issue #106

The current v0.2 Evidence schema already supports `year`, `month` and `day` precision.

Issue #106 therefore no longer represents a simple inability to store partial dates. Its remaining question is narrower:

> How should ND Oracle represent uncertainty **within** a candidate date/edition identity when even the available year/month/day value is not sufficiently certain to state without qualification?

Evidence Layer v1 does not mutate the schema merely to close that question. A schema change requires a demonstrated real corpus case, migration plan and hostile certainty-inflation review.

## 12. Provenance

Evidence curation must record enough provenance to distinguish:

- source collection;
- evidence appraisal;
- claim interpretation;
- contribution-role assignment;
- material confidence changes;
- deprecation/supersession decisions.

Git history preserves prior states. When a role or interpretation materially changes, the changed object/provenance and commit message must explain why.

Rejected sources need not become authoritative Evidence objects, but materially important rejection decisions should be recorded in the research/coverage work when they affect later review.

## 13. Evidence intake workflow

For a proposed serious claim:

1. Write the exact bounded claim first.
2. Classify the claim editorially; do not machine-infer semantic class as authority.
3. Identify primary/authoritative sources.
4. Check source identity/version/date.
5. Appraise source design and applicability.
6. Extract only the finding relevant to the exact claim.
7. Assign a bounded Evidence role.
8. Record population/context and methodology.
9. Record limitations, funding and conflicts where relevant.
10. Search for material contradiction or alternative explanation.
11. Set claim confidence from the whole bounded evidence route.
12. Preserve explicit uncertainty.
13. Hostile-review high-consequence claims.
14. Validate reciprocity and provenance.
15. Publish only after exact-head CI.

Copyright-sensitive exact quotation/location notes may be retained internally when needed, but public pages should paraphrase unless short quotation is necessary and lawful.

## 14. Machine-readable coverage registry

`scripts/evidence_coverage.py` generates a deterministic registry across both accepted evidence models.

The registry records every governed Claim, its evidence model, source routes, source kinds, contribution roles (where normalized), confidence, uncertainty-route count, review age and machine triage flags.

Triage flags are **not semantic classifications**. They only help editors find claims that may deserve closer review.

Metrics such as:

- claims with evidence;
- claims with multiple source routes;
- source-kind distribution;
- normalized versus legacy evidence;
- possible high-consequence wording;

are audit signals, not truth scores.

## 15. Public Evidence UX

The public Evidence projection must remain reading-first.

It should expose:

- citation/title;
- source kind;
- authorship where structured;
- date/precision;
- access/review state;
- locator(s);
- exact claims the source bears on;
- contribution role;
- bounded finding;
- population/context;
- methodology;
- limitations;
- funding/conflicts where present;
- provenance.

Legacy v0.1 source pages must clearly state that they are **legacy embedded source routes** and do not invent v0.2 Contribution roles/findings that the authoritative data does not contain.

Claim → Evidence and Evidence → Claim navigation should be symmetrical.

Evidence pages do **not** join ordinary practical `/find/` ranking. Dedicated Evidence search may filter citation, title/authorship, source kind, DOI/ISBN/locator and claim references entirely in the browser. Queries must not be transmitted or stored.

## 16. Acceptance

Evidence Layer v1 passes only when:

- every authoritative Claim is present in the coverage registry;
- no governed Claim has a broken evidence/uncertainty route;
- every normalized v0.2 Claim/Evidence route is reciprocal;
- no normalized Evidence object is orphaned;
- source-kind/role/locator/commercial-conflict negative fixtures pass;
- contradiction and multi-claim fixtures remain valid;
- evidence-specific freshness rules pass;
- public Evidence index and individual Evidence projections build;
- dedicated Evidence search is browser-local;
- ordinary discovery ranking, clinical boundaries, jurisdiction filtering, privacy/query handling, schema authority and release-state gates remain unchanged;
- full exact-head CI passes;
- final hostile review finds no certainty inflation, hidden contradiction, endorsement conversion or provenance loss.

Migration of legacy v0.1 Concepts into v0.2 is **not** an Evidence Layer v1 acceptance requirement. It is a separately governed semantic migration and must not be performed merely to make the top-level Evidence count larger.

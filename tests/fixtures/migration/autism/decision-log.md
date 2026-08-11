# Autism migration decision log

Status: **migration decisions D1–D6 accepted**. The package remains non-authoritative and not ready for authoritative replacement: the three Perspective framing proposals remain pending; the paired Autism ↔ Neurodiversity candidate is prepared but its structural confidence field remains an explicit enrichment/schema-policy requirement; and the Neurodiversity → ADHD structural dependency remains unresolved.

Research pass: 2026-08-11, against repository `main` `0f6042e8841149da0485fe1b279dcd1bc9e5ff1f` and unchanged authoritative Autism blob `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`.

Owner decision D1 was accepted on 2026-08-11 against protected repository `main` `ebb6439d265a2e53920818aec9bb001940f6511d`.

Owner decision D2 was accepted on 2026-08-11 against protected repository `main` `274b27e66a6c548575bf7774fdd204c78fe4624e`.

Owner decision D3 was accepted on 2026-08-11 against protected repository `main` `2979996e82f7461a4431476c8c297d67bdb1b236`.

Owner decision D4 was accepted on 2026-08-11 against protected repository `main` `0cb73f1642f6a857049e41767bf69c677dccf0ac`.

Owner decision D5 was accepted on 2026-08-11 against protected repository `main` `e2f535ad2abdb97750d54c7c30233a3c802a8e74`.

Owner decision D6 was accepted on 2026-08-11 against protected repository `main` `653938871190b454696df12abcc5bc0260ce19fd`.

## Evidence-backed enrichment findings

### WHO source

Primary route: https://www.who.int/news-room/fact-sheets/detail/autism-spectrum-disorders

Verified proposal data:

- title: `Autism`;
- publication date: `2025-09-17`;
- corporate authorship: `World Health Organization` (no individual byline is displayed);
- Claim 1 contribution role: `supportive` — WHO directly states that abilities and needs vary and can evolve over time, while not explicitly operationalising the claim's `across contexts` wording;
- Claim 2 contribution role: `compatible` — WHO identifies unusual reactions to sensations and describes autism as diverse, but does not establish the claim's detailed hyperreactivity/hyporeactivity/sensory-interest taxonomy by itself.

WHO methodology is represented as an authoritative fact sheet synthesising referenced evidence and public-health guidance, not as a claim-specific primary empirical study.

### Neurobiology source

Primary routes:

- https://pubmed.ncbi.nlm.nih.gov/32711809/
- https://doi.org/10.1016/bs.pmbts.2020.04.020
- https://www.sciencedirect.com/science/article/pii/S1877117320300648

Verified proposal data:

- title: `Neurobiology of sensory processing in autism spectrum disorder`;
- electronic publication date: `2020-05-13`;
- authors: `Phoebe Pui Pui Cheung; Benson Wui Man Lau`;
- source type/method: narrative review chapter integrating clinical, behavioural and neurobiological literature; the accessible source description does not report a systematic-review search protocol;
- Claim 2 contribution role: `supportive` for altered sensory processing, hyper-/hyposensitivity across sensory domains, and variable severity; it does not by itself establish every element of the legacy claim, especially `unusual sensory interests`.

### Source-integrity conflict discovered

The authoritative v0.1 source record cites:

`Kawakami, S. et al. Neurobiology of sensory processing in autism spectrum disorder (2020).`

but PMID `32711809` and DOI `10.1016/bs.pmbts.2020.04.020` identify the authors as **Phoebe Pui Pui Cheung and Benson Wui Man Lau**.

The v0.1 object remains unchanged.

## Accepted decisions

### D1 — Correct the neurobiology citation in the future v0.2 Evidence object — **ACCEPTED**

**Accepted rule:** use the verified Cheung & Lau attribution in the future non-authoritative v0.2 Autism Evidence candidate while retaining the original v0.1 `Kawakami, S. et al.` source text unchanged in the preservation trail.

Accepted citation value:

`Cheung, Phoebe Pui Pui; Lau, Benson Wui Man. Neurobiology of sensory processing in autism spectrum disorder (2020).`

Evidence routes:

- https://pubmed.ncbi.nlm.nih.gov/32711809/
- https://doi.org/10.1016/bs.pmbts.2020.04.020

**Boundary:** this decision does not authorise mutation of `objects/concepts/autism.json`, authoritative v0.2 replacement, migration of Neurodiversity, or acceptance of later decisions.

### D2 — Legacy `related_to` mapping — **ACCEPTED AS DEFERRED MAPPING**

**Accepted rule:** retain both Autism v0.1 `related_to` relations as `legacy_retained_unmapped` migration units. Do not map them to v0.2 `associated_with`, and do not invent relation confidence.

The exact retained legacy relations are:

- `related_to -> sensory-processing` with note `Sensory differences are common but heterogeneous.`;
- `related_to -> executive-function` with note `Executive demands can shape daily access and support; this is not a defining equivalence.`

**Reason:** `associated_with` is only the nearest v0.2 vocabulary, not an exact deterministic equivalent, and v0.2 relations additionally require a confidence value absent from v0.1. Assigning `low`, `moderate`, `not_applicable`, or another confidence merely to make the schema pass would manufacture semantics.

**Reopening condition:** revisit only if a later accepted relation-migration policy can represent the legacy relation without inventing confidence, or if an individual relation is explicitly reviewed as a new semantic act.

**Boundary:** D2 does not delete the relations, change the authoritative v0.1 Autism object, authorise `associated_with`, authorise a confidence value, construct an authoritative v0.2 candidate, or accept later decisions.

### D3 — List-valued `what_would_reduce_it` — **ACCEPTED AS SCHEMA-POLICY DEFERRAL**

**Accepted rule:** retain both Autism v0.1 uncertainty units as `legacy_retained_unmapped` with their exact `what_would_reduce_it` arrays. Do not flatten the arrays into prose and do not encode them into the current v0.2 single-string field.

The retained reduction-condition arrays are:

- `autism-uncertainty-measurement`: `longitudinal community-led studies`; `multidimensional support descriptions`; `validation across ages, cultures, communication modes, and intellectual abilities`;
- `autism-uncertainty-sensory`: `participatory trials of accommodations`; `ecologically valid measures`; `reporting of benefit, burden, and adverse effects`.

**Reason:** flattening makes item boundaries convention-dependent; a canonical string could be reversible but would still force structured one-or-many semantics into a prose field. Neither is required merely to satisfy the current schema.

**Reopening condition:** revisit through an explicit schema-policy decision that supports one-or-many reduction conditions directly, or another explicitly accepted reversible representation that preserves item boundaries.

**Boundary:** D3 authorises no schema change now, no flattening, no canonical-string encoding, no mutation of the authoritative v0.1 Autism object, no authoritative v0.2 replacement, and no acceptance of later decisions.

### D4 — `ecosystem_entry_points` — **ACCEPTED AS ECOSYSTEM-MODEL DEFERRAL**

**Accepted rule:** retain all four Autism v0.1 `ecosystem_entry_points` exactly as `legacy_retained_unmapped`. Do not auto-promote their embedded questions and do not force the structures into any existing v0.2 object type.

The retained categories are:

- `accommodations`;
- `communities`;
- `services`;
- `tools`.

Each category's original embedded questions remain part of its exact retained legacy payload.

**Reason:** no exact v0.2 semantic home has been demonstrated. Treating embedded prompts as standalone Question objects would add semantics not present in the legacy object, while forcing the whole structure into an existing type would misrepresent its navigation/ecosystem role.

**Reopening condition:** revisit when a first-class ecosystem or navigation model is explicitly designed. An embedded question may be considered independently only through a separate review of whether it is independently reusable as a standalone Question.

**Boundary:** D4 authorises no auto-promotion, no forced mapping, no new schema or object type, no mutation of the authoritative v0.1 Autism object, no authoritative v0.2 replacement, and no acceptance of later decisions.

### D5 — Autism ↔ Neurodiversity structural closure — **ACCEPTED AS STRUCTURAL-PAIRING POLICY**

**Accepted rule:** when structural migration is prepared, Autism and Neurodiversity must be handled as the minimum paired non-authoritative candidate required to preserve the reciprocal `narrower_than` / `broader_than` relationship. Do not weaken the v0.2 reciprocity validator.

The authoritative legacy reciprocal remains:

- Autism: `narrower_than -> neurodiversity`;
- Neurodiversity: `broader_than -> autism`.

**Reason:** semantic reciprocity already exists in v0.1, but the v0.2 validator requires both sides in v0.2 relation shape. Migrating Autism alone would therefore create an invalid structural candidate unless reciprocity validation were weakened, which is explicitly rejected.

**Current dependency state:** still `unresolved`. The paired non-authoritative candidate has now been prepared, but it cannot yet validate as complete v0.2 relation data because the legacy relations do not supply the required confidence field.

**Closure condition:** demonstrate an exact paired v0.2 relation under the unchanged reciprocity rule once all required relation semantics have a non-fabricating representation.

**Boundary:** D5 authorises preparation of that paired non-authoritative candidate only. It does not authorise mutation of either authoritative v0.1 object, authoritative replacement of either object, weakening of the reciprocity validator, deployment, or publication.

### D6 — Missing structural relation confidence — **ACCEPTED AS ENRICHMENT/SCHEMA-POLICY DEFERRAL**

**Accepted rule:** do not infer or default `confidence` for migrated structural `broader_than` / `narrower_than` relations when the legacy relation contains no confidence value. Preserve the paired Autism ↔ Neurodiversity candidate without `confidence` until either an evidence-backed confidence value is proposed and reviewed or a separate structural-confidence schema policy is accepted.

`not_applicable` is explicitly **not** authorised merely as a way to make the current v0.2 schema validate.

**Reason:** the current schema requires a confidence field, but the authoritative v0.1 structural relations do not contain one. Supplying a default would turn a schema-completion step into invented knowledge. Using `not_applicable` without a semantic policy would hide that invention behind a nominally valid enum value.

**Current state:** the policy choice is resolved, but the field itself remains unresolved. This is now an explicit enrichment/schema-policy requirement rather than an invitation to choose a convenient default.

**Reopening condition:** revisit when an evidence-backed confidence value is proposed for explicit review or when a distinct structural-confidence schema policy is proposed. Acceptance of either remains a separate decision.

**Boundary:** D6 authorises no confidence value, no schema change, no authoritative v0.1 mutation, no authoritative v0.2 replacement, and no weakening of reciprocity validation.

The machine-readable decision records are in `owner-decisions.json`; exact retained relation, uncertainty and ecosystem payloads remain recoverable in `preservation-ledger.json`, and unresolved structural dependencies remain recorded in the dependency ledger.

## Perspective proposals — not accepted

Evidence routes: WHO autism fact sheet plus https://www.who.int/about/

Proposed `held_by.scope`:

> WHO institutional global public-health guidance on autism; not a statement representing all clinicians, autistic people, families, researchers or WHO Member States individually.

Proposed `reasoning`:

> WHO frames autism as diverse, with variable and evolving abilities and needs, and links health and quality of life to accessible, inclusive, person-responsive services plus community and societal support.

Proposed Perspective `scope`:

> Global public-health description of autism, health and care needs, inclusion and support across the life course; excludes individual diagnosis and does not purport to capture the full range of autistic lived experience or community perspectives.

These remain `owner_decision` proposals because they are framing choices rather than raw source metadata.

## Preserved rejected shortcut

Inventing placeholder or plausible-looking values solely to make v0.2 schemas pass remains rejected. Reopen only if the accepted migration compatibility contract itself changes.

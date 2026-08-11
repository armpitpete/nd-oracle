# Autism migration decision log

Status: **owner decision pending**. D1 and D2 are accepted. D3–D5 remain pending. No authoritative replacement is authorised by this file.

Research pass: 2026-08-11, against repository `main` `0f6042e8841149da0485fe1b279dcd1bc9e5ff1f` and unchanged authoritative Autism blob `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`.

Owner decision D1 was accepted on 2026-08-11 against protected repository `main` `ebb6439d265a2e53920818aec9bb001940f6511d`.

Owner decision D2 was accepted on 2026-08-11 against protected repository `main` `274b27e66a6c548575bf7774fdd204c78fe4624e`.

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

**Boundary:** this decision does not authorise mutation of `objects/concepts/autism.json`, authoritative v0.2 replacement, migration of Neurodiversity, or acceptance of D2–D5.

### D2 — Legacy `related_to` mapping — **ACCEPTED AS DEFERRED MAPPING**

**Accepted rule:** retain both Autism v0.1 `related_to` relations as `legacy_retained_unmapped` migration units. Do not map them to v0.2 `associated_with`, and do not invent relation confidence.

The exact retained legacy relations are:

- `related_to -> sensory-processing` with note `Sensory differences are common but heterogeneous.`;
- `related_to -> executive-function` with note `Executive demands can shape daily access and support; this is not a defining equivalence.`

**Reason:** `associated_with` is only the nearest v0.2 vocabulary, not an exact deterministic equivalent, and v0.2 relations additionally require a confidence value absent from v0.1. Assigning `low`, `moderate`, `not_applicable`, or another confidence merely to make the schema pass would manufacture semantics.

**Reopening condition:** revisit only if a later accepted relation-migration policy can represent the legacy relation without inventing confidence, or if an individual relation is explicitly reviewed as a new semantic act.

**Boundary:** D2 does not delete the relations, change the authoritative v0.1 Autism object, authorise `associated_with`, authorise a confidence value, construct an authoritative v0.2 candidate, or accept D3–D5.

The machine-readable decision records are in `owner-decisions.json`; the exact legacy relation payloads remain recoverable in `preservation-ledger.json`.

## Perspective proposals — not accepted

Evidence routes: WHO autism fact sheet plus https://www.who.int/about/

Proposed `held_by.scope`:

> WHO institutional global public-health guidance on autism; not a statement representing all clinicians, autistic people, families, researchers or WHO Member States individually.

Proposed `reasoning`:

> WHO frames autism as diverse, with variable and evolving abilities and needs, and links health and quality of life to accessible, inclusive, person-responsive services plus community and societal support.

Proposed Perspective `scope`:

> Global public-health description of autism, health and care needs, inclusion and support across the life course; excludes individual diagnosis and does not purport to capture the full range of autistic lived experience or community perspectives.

These remain `owner_decision` proposals because they are framing choices rather than raw source metadata.

## Pending decision candidates

### D3 — List-valued `what_would_reduce_it` — **PENDING**

Options:

1. flatten the list into prose — **not recommended**, because reversibility and item boundaries become convention-dependent;
2. encode the original array as a canonical string — reversible but semantically awkward inside a prose field;
3. revise the v0.2 uncertainty representation in a later schema-policy lane to preserve one-or-many reduction conditions directly.

**Recommendation:** option 3. Keep the original arrays in the preservation ledger until that policy is accepted.

### D4 — `ecosystem_entry_points` — **PENDING**

Options:

1. auto-promote embedded questions to standalone Question objects — rejected by the accepted migration contract;
2. map the whole structure into an existing v0.2 object type — no exact semantic home has been demonstrated;
3. retain as `legacy_retained_unmapped` pending a first-class navigation/ecosystem-entry model, with individual questions eligible for later independent-reusability review.

**Recommendation:** option 3.

### D5 — Autism ↔ Neurodiversity structural closure — **PENDING**

The v0.1 Neurodiversity object already contains the reciprocal `broader_than -> autism` relation, so the semantic reciprocal is present in legacy data. The dependency remains unresolved because the v0.2 validator requires both sides in v0.2 relation shape.

**Candidate:** when structural migration is authorised, prepare Autism and Neurodiversity as the minimum paired structural candidate rather than weaken reciprocity validation.

**Recommendation:** use the paired-candidate approach; do not weaken the v0.2 reciprocity rule.

## Preserved rejected shortcut

Inventing placeholder or plausible-looking values solely to make v0.2 schemas pass remains rejected. Reopen only if the accepted migration compatibility contract itself changes.

# Autism migration decision log

Status: **owner decision pending**. No migration mapping or authoritative replacement is accepted by this file.

Research pass: 2026-08-11, against repository `main` `0f6042e8841149da0485fe1b279dcd1bc9e5ff1f` and unchanged authoritative Autism blob `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`.

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

The v0.1 object remains unchanged. The enrichment ledger contains a verified corrected-citation proposal for a future v0.2 Evidence candidate, but adopting it requires an explicit owner decision because it changes preserved source text.

## Perspective proposals — not accepted

Evidence routes: WHO autism fact sheet plus https://www.who.int/about/

Proposed `held_by.scope`:

> WHO institutional global public-health guidance on autism; not a statement representing all clinicians, autistic people, families, researchers or WHO Member States individually.

Proposed `reasoning`:

> WHO frames autism as diverse, with variable and evolving abilities and needs, and links health and quality of life to accessible, inclusive, person-responsive services plus community and societal support.

Proposed Perspective `scope`:

> Global public-health description of autism, health and care needs, inclusion and support across the life course; excludes individual diagnosis and does not purport to capture the full range of autistic lived experience or community perspectives.

These remain `owner_decision` proposals because they are framing choices rather than raw source metadata.

## Explicit decision candidates — none accepted

### D1 — Correct the neurobiology citation in the future v0.2 Evidence object

**Candidate:** use the verified Cheung & Lau citation in the v0.2 candidate while retaining the original v0.1 source unit in the preservation trail.

**Reason to accept:** PMID and DOI metadata directly contradict the legacy author attribution.

**Reason to reject/defer:** migration may be kept strictly text-preserving until source correction is handled as a separate editorial repair.

**Recommendation:** accept the corrected v0.2 citation only through an explicit source-correction decision; do not mutate v0.1 during this lane.

### D2 — Legacy `related_to` mapping

The nearest v0.2 vocabulary is `associated_with`, but this is not yet safely mechanical. A further gap was identified: every v0.2 relation also requires `confidence`, while the two v0.1 `related_to` records contain no confidence field.

Options:

1. accept `related_to -> associated_with` plus a separately governed migration rule for missing relation confidence;
2. retain the relations as legacy-unmapped until v0.2 has a non-fabricating representation for missing legacy confidence;
3. review each relation individually as a new semantic act.

**Recommendation:** option 2 for now. Do not invent `low`, `moderate`, or `not_applicable` merely to satisfy the schema.

### D3 — List-valued `what_would_reduce_it`

Options:

1. flatten the list into prose — **not recommended**, because reversibility and item boundaries become convention-dependent;
2. encode the original array as a canonical string — reversible but semantically awkward inside a prose field;
3. revise the v0.2 uncertainty representation in a later schema-policy lane to preserve one-or-many reduction conditions directly.

**Recommendation:** option 3. Keep the original arrays in the preservation ledger until that policy is accepted.

### D4 — `ecosystem_entry_points`

Options:

1. auto-promote embedded questions to standalone Question objects — rejected by the accepted migration contract;
2. map the whole structure into an existing v0.2 object type — no exact semantic home has been demonstrated;
3. retain as `legacy_retained_unmapped` pending a first-class navigation/ecosystem-entry model, with individual questions eligible for later independent-reusability review.

**Recommendation:** option 3.

### D5 — Autism ↔ Neurodiversity structural closure

The v0.1 Neurodiversity object already contains the reciprocal `broader_than -> autism` relation, so the semantic reciprocal is present in legacy data. The dependency remains unresolved because the v0.2 validator requires both sides in v0.2 relation shape.

**Candidate:** when structural migration is authorised, prepare Autism and Neurodiversity as the minimum paired structural candidate rather than weaken reciprocity validation.

**Recommendation:** use the paired-candidate approach; do not weaken the v0.2 reciprocity rule.

## Preserved rejected shortcut

Inventing placeholder or plausible-looking values solely to make v0.2 schemas pass remains rejected. Reopen only if the accepted migration compatibility contract itself changes.

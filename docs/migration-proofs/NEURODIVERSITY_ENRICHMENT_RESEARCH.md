# Neurodiversity v0.2 enrichment research

Status: **evidence-backed non-authoritative proposals prepared; owner decisions remain pending**.

Prepared on 2026-08-11 against protected repository `main`:

`26ee009309efd624c9da661bd168522a3089932c`

Authoritative Neurodiversity source anchor:

- `objects/concepts/neurodiversity.json`
- blob `5a38bc4250079412dd3f4da1d598dfcab984ca66`

Machine-readable research record:

`migration-candidates/autism-neurodiversity/neurodiversity-enrichment-research.json`

## Source findings

### Judy Singer — `neurodiversity-source-singer`

Verified:

- title: `NeuroDiversity: The Birth of an Idea`;
- authorship: `Judy Singer`.

Date is **not resolved**. The legacy citation and Singer's own bibliography point to a 2016 Kindle edition, while the repository's actual Wellcome locator describes a 2017 print edition. The current v0.2 Evidence schema requires a full `YYYY-MM-DD` date. Combining the 2016 citation with 2017 print metadata would silently create a synthetic source identity, so no date is proposed.

Evidence Contribution proposals:

- Claim 1 role: `compatible` — Singer documents the 1998 thesis, participant observation on InLv and late-1990s autistic/disability-rights context, but this source alone cannot establish the stronger conclusion that origin credit must be collective.
- Claim 2 role: `compatible` — Singer's work supports coexistence of disability-rights, medical and sociological framings, but the accessible evidence does not directly establish every element of the claim about support needs and clinical care.

Both contributions include explicit limitations and reopening conditions rather than treating source compatibility as proof of the full claim.

### Botha et al. — `neurodiversity-source-botha`

Verified:

- title: `The neurodiversity concept was developed collectively: An overdue correction on the origins of neurodiversity theory`;
- date: `2024-03-12`;
- authorship: `Monique Botha; Robert Chapman; Morénike Giwa Onaiwu; Steven K Kapp; Abs Stannard Ashley; Nick Walker`;
- publication type: peer-reviewed scholarly letter in *Autism*.

A source-integrity conflict was found. The authoritative v0.1 record contains DOI:

`10.1080/09687599.2024.2327837`

The cited University of Portsmouth publication record identifies the paper's DOI as:

`10.1177/13623613241237871`

The v0.1 object remains unchanged. A corrected future v0.2 citation is recorded as a verified proposal requiring explicit owner acceptance.

Claim 1 contribution role: `supportive`. The paper directly compares dated origin evidence and argues that the concept and theorising have multiple, collective origins. It remains bounded because it is a historical correction letter synthesising selected archival findings, not an exhaustive archive of every early participant.

## Perspective proposals — not accepted

### `neurodiversity-perspective-paradigm`

Proposed `held_by.scope`:

> Neurodiversity advocates and scholars using disability-rights, sociological and inclusion-oriented framings; not a claim that all neurodivergent people, clinicians, researchers or advocates hold one position.

Proposed `reasoning`:

> Singer's work situates neurological variation within disability-rights, social-constructionist and feminist analysis, combines autobiographical and autistic-community observation, and argues for balancing medical accounts with sociological or adaptive understandings rather than treating diagnosis as the whole meaning of difference.

Proposed `scope`:

> A social and political framing of neurological variation, disability, rights, environment, inclusion and movement-building; excludes individual diagnosis, person-specific support prescriptions and any claim that all neurological differences are beneficial.

### `neurodiversity-perspective-collective`

Proposed `held_by.scope`:

> Botha, Chapman, Giwa Onaiwu, Kapp, Stannard Ashley and Walker as an international group of autistic scholars writing on the historical origins of neurodiversity; not a statement representing all autistic people or all neurodiversity scholarship.

Proposed `reasoning`:

> The authors compare dated archival and published evidence from autistic online-community discussion, Singer's 1998 thesis, Blume's 1997 and 1998 writing, and a reported 1996 InLv post, and conclude that the concept and theorising of neurodiversity have multiple, collective origins.

Proposed `scope`:

> Historical attribution of the origins and early theorising of neurodiversity; excludes ownership of later meanings, a complete history of every contributor, and representation of all contemporary neurodiversity positions.

These are evidence-backed framing proposals only. Research does not accept them.

## Decision candidates produced

1. **Singer edition reconciliation** — do not choose or combine the 2016 Kindle and 2017 print identities until the intended source and a schema-valid full date are explicitly resolved.
2. **Botha citation correction** — recommended acceptance of the verified DOI/citation correction for the future non-authoritative v0.2 Evidence candidate only, preserving the v0.1 source exactly.
3. **Paradigm Perspective framing** — owner decision required.
4. **Collective-origin Perspective framing** — owner decision required.

## Preserved blockers

This research pass does not alter:

- the list-valued Neurodiversity `what_would_reduce_it` uncertainty arrays;
- D6's prohibition on inferred/defaulted structural confidence;
- the unresolved Neurodiversity `broader_than -> adhd` structural dependency;
- either authoritative v0.1 source object;
- the v0.2 schema or authoritative validator.

No authoritative replacement, publication, deployment, site, DNS, analytics or production change is authorised.

# Batch A cross-topic gap resolution

Status: **candidate research only — not authoritative, not public**

Prepared: 2026-08-12

This file resolves the five batch-level checks left open by `BATCH_A_RESEARCH_MATRIX.md` before candidate concept objects are drafted.

## G1 — UK learning disability ↔ international terminology

### Question

Can ND Oracle simply say UK “learning disability” = international “intellectual disability”?

### Evidence checked

- NHS England currently defines learning disability through reduced ability to understand/learn, reduced adaptive independence, developmental onset, and explicitly distinguishes it from specific learning difficulties such as dyslexia.
- NHS England identification material sometimes references records saying “learning disability, intellectual disability, or global developmental delay”.
- WHO ICD-11 uses the diagnostic-group wording **“disorders of intellectual development”** and describes these disorders through significant limitations in intellectual functioning and adaptive behaviour.

### Disposition

**Do not claim perfect label equivalence.**

Candidate public wording should be:

> In UK health and social care, the usual term is **learning disability**. International clinical and research sources may instead use terms such as **intellectual disability**; WHO ICD-11 uses **disorders of intellectual development**. These terms substantially overlap, but legal, service and diagnostic wording varies by system.

This preserves the UK distinction from dyslexia without pretending all jurisdictions use identical categories.

### Sources

- NHS England, Learning Disability Register guidance: https://www.england.nhs.uk/long-read/find-out-about-the-learning-disability-register/
- WHO, Mental disorders fact sheet (2025): https://www.who.int/news-room/fact-sheets/detail/mental-disorders
- WHO ICD-11 CDDR publication: https://www.who.int/publications/i/item/9789240077263

**Result:** resolved for candidate drafting.

---

## G2 — dyslexia, intelligence and IQ-discrepancy models

### Question

Could “dyslexia does not imply low intelligence” accidentally recreate an IQ eligibility rule?

### Evidence checked

- NHS says dyslexia does not affect intelligence.
- The International Dyslexia Association adopted a revised definition in October 2025, published with scientific rationale in 2026.
- The 2025 IDA definition centres word reading/spelling accuracy and/or speed, persistence despite effective instruction, orthographic variation and multifactorial influences.
- The IDA explanation explicitly says the revised definition **removed reference to other cognitive abilities** because the older wording had encouraged unsupported IQ-discrepancy/cognitive-profile identification. It states that word-level literacy difficulty occurs across a range of cognitive profiles.
- A 2021 systematic review found psychologists still use diverse identification methods and highlighted lack of universal assessment consensus.

### Disposition

Replace the earlier candidate wording with:

> Dyslexia is characterised primarily by persistent difficulty with word reading and/or spelling. It occurs across a range of cognitive profiles, so general intelligence should not be used as a simple eligibility test for whether someone can be dyslexic.

Keep the NHS anti-stigma point, but **do not** say or imply that average/high IQ is required.

Also update the scope so “writing” is not presented as equally core with word reading/spelling merely because an NHS summary uses broad public wording.

### Sources

- International Dyslexia Association, 2025 Definition Project: https://dyslexiaida.org/2025-dyslexia-definition-project/
- Catts HW, Haynes CW, Joshi RM. `Defining dyslexia: 2025 revision`. Annals of Dyslexia. 2026. PMID 42053753. DOI 10.1007/s11881-026-00363-4.
- Methods used by psychologists for identifying dyslexia: a systematic review. PMID 34931397.
- NHS dyslexia pages.

**Result:** resolved for candidate drafting; multilingual/orthographic assessment remains a topic uncertainty, not a blocker.

---

## G3 — Tourette/tic exact classification wording

### Question

Should ND Oracle freeze one diagnostic manual's exact criteria into the seed page?

### Evidence checked

- Current NHS guidance uses a UK-facing description: motor and vocal tics; onset before 18; duration one year or more; many children have tics without Tourette syndrome.
- 2022 European Society for the Study of Tourette Syndrome assessment guidelines explicitly review diagnostic changes and differential diagnoses and note the need to distinguish other tic/functional movement presentations.
- WHO's ICD-11 CDDR is the current global clinical diagnostic manual, but the accessible WHO publication landing page does not expose enough disorder-specific text here to justify copying exact ICD wording into ND Oracle.

### Disposition

**Do not present the NHS summary as the complete universal diagnostic criteria.**

Candidate wording should say:

> Tourette syndrome is a tic disorder involving both motor and vocal tics, with onset during development and persistence over time. Exact diagnostic wording differs between classification systems, so ND Oracle does not use this page as a self-diagnosis checklist.

A separate evidence note can state that current NHS public guidance uses onset before 18 and at least one year of tics.

This is more accurate than pretending one criterion set is universal.

### Sources

- NHS Tourette syndrome: https://www.nhs.uk/conditions/tourette-syndrome/
- Szejko N et al. ESSTS guidelines v2.0 Part I: assessment. PMID 34661764.
- WHO ICD-11 CDDR publication: https://www.who.int/publications/i/item/9789240077263

**Result:** resolved for candidate drafting.

---

## G4 — has newer consensus superseded CATALISE for DLD?

### Question

Can CATALISE 2017 be presented as the universal current definition of DLD?

### Evidence checked

- CATALISE Phase 2 reached multinational/multidisciplinary consensus that DLD applies to language disorder causing functional impairment/poor prognosis when not associated with a known biomedical aetiology; risk factors do not preclude DLD; DLD can co-occur with conditions such as ADHD; no verbal/nonverbal discrepancy is required.
- 2023 implementation research still describes active efforts to integrate CATALISE recommendations across English-speaking countries, indicating that CATALISE remains active rather than historically superseded.
- 2024 UK speech-sound terminology work explicitly **builds on** the CATALISE DLD model while refining overlap with speech sound disorder.
- A 2024 German interdisciplinary guideline uses “developmental language disorders” more broadly, including language disorders associated with relevant comorbidities, and explicitly notes that this differs from the narrower CATALISE use.

### Disposition

**CATALISE remains a strong English-speaking consensus anchor, but it is not universal terminology.**

Candidate page wording should therefore be explicit:

> In the CATALISE framework widely used in English-speaking research and services, DLD refers to persistent, functionally significant developmental language disorder without a known biomedical cause. Other systems use the term more broadly, so terminology is not completely uniform internationally.

This turns terminology disagreement into inspectable evidence rather than hiding it.

### Sources

- Bishop et al. CATALISE Phase 2. PMID 28369935.
- Gallagher et al. CATALISE dissemination/implementation. PMID 37300436.
- Stringer et al. speech sound disorder/DLD terminology. PMID 38059693.
- Neumann et al. 2024 German clinical practice guideline. PMID 38377329.

**Result:** resolved for candidate drafting; international terminology variation becomes a published uncertainty.

---

## G5 — relation to Neurodiversity

### Question

Should Batch A concepts use `narrower_than -> neurodiversity` because they are commonly discussed as neurodivergence?

### Repository evidence checked

Existing non-authoritative relation-semantics review:

`migration-candidates/autism-neurodiversity/relation-semantics-review.json`

It found that the legacy `broader_than` / `narrower_than` labels look taxonomic while their notes only claim discourse/ecosystem inclusion. Current source review distinguished **neurodiversity** (population-level diversity) from **neurodivergence** (particular patterns/differences), and recommended against silently converting discourse inclusion into a taxonomy edge.

The review specifically found the same mismatch for ADHD as a consistency test.

### Disposition

**Do not emit `narrower_than -> neurodiversity` for any Batch A candidate.**

For candidate concept objects:

- no direct taxonomy edge to `neurodiversity` by default;
- use specific evidence-backed relations to other concepts only when the relation itself is meaningful;
- if ND Oracle later wants to encode “commonly discussed within neurodiversity discourse”, model that as a separately reviewed semantic relation/perspective rather than overloading `narrower_than`.

This is not a new authoritative schema decision. It simply avoids repeating a known candidate-level semantic error.

**Result:** resolved for Batch A candidate drafting.

---

# Overall result

All five pre-object checks are resolved sufficiently to draft **non-authoritative candidate concept objects**.

What remains deliberately unresolved should travel with each candidate as uncertainty rather than block the whole batch:

- cross-linguistic/orthographic dyslexia assessment;
- adult DCD assessment and outcomes;
- classification-system detail and adult course in tic disorders;
- cross-cultural/adaptive assessment and terminology for learning disability/intellectual disability;
- multilingual assessment and international DLD terminology.

Next step: materialise five candidate objects in the migration-candidate area, validate them structurally, then present their actual proposed public statements for human content acceptance before anything enters `objects/concepts/`.

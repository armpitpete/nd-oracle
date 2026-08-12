# ND Oracle original-five Batch B evidence review

Status: **bounded batch review candidate**

Review date: 2026-08-12

Base protected `main`: `e665673556e5d32515896d0e2d29b15fb83f1f96`

Batch:

1. neurodiversity;
2. autism;
3. ADHD;
4. executive function;
5. sensory processing.

This batch brings the five original `seed` concepts up to the evidence/review standard used for Batch A. The five topics are reviewed together so cross-topic relations and terminology are tested as one system rather than as five independent narratives.

## Evidence rule

Each public claim in the batch must have:

- a bounded plain-language meaning;
- inspectable supporting evidence;
- an explicit confidence level;
- a boundary or counterexample;
- an open uncertainty where the evidence does not justify a universal statement;
- a clear condition under which ND Oracle should revise the claim.

Current public guidance is used for current clinical terminology and service context. Systematic reviews, meta-analyses and peer-reviewed conceptual/historical work are used to test whether simplifications are defensible. Lived/community or normative perspectives are represented as perspectives, not silently converted into empirical facts.

## Cross-batch findings

### B1 — Neurodiversity is not a diagnostic taxonomy

The old graph encoded `neurodiversity broader_than autism/ADHD` and reciprocal `narrower_than` edges. That is too taxonomic for the evidence. The reviewed batch replaces those edges with `related_to` ecosystem relations. This carries forward the already accepted ND Oracle rule that being discussed within neurodiversity does not make a diagnosis a formal child class of neurodiversity.

### B2 — Autism needs both clinical and community/language evidence

WHO and NICE support a heterogeneous lifelong neurodevelopmental description with widely varying abilities and support needs. Current systematic review evidence shows identity-first language is often preferred by autistic adults, but there is no universal preference and existing studies underrepresent parts of the autistic population. The reviewed object therefore uses autistic-person language by default while explicitly preserving individual preference.

### B3 — ADHD assessment is clinical, not a cognitive-test shortcut

NICE requires specialist assessment using developmental/psychiatric history, impairment across settings and consideration of alternative/co-occurring explanations; rating scales or cognitive tests are not sufficient alone. Recent executive-function reviews show real group-level differences but poor diagnostic specificity. The reviewed object therefore relates ADHD to executive function without making executive dysfunction synonymous with ADHD.

### B4 — Executive function is a measurement family, not one thing

The unity/diversity literature supports correlated but partly separable processes, while systematic re-analysis finds no single factor structure that fits every age/sample. Recent ecological-validity work also warns that a task looking like daily life is not evidence that its score predicts daily functioning. The reviewed object therefore separates construct, measurement and everyday-function questions.

### B5 — Sensory evidence is real but easy to overgeneralise

Recent autism and ADHD syntheses support group-level sensory differences with substantial heterogeneity. Sensory differences are therefore represented as transdiagnostic and non-specific. Recent systematic reviews of fidelity-defined Ayres Sensory Integration do not justify a universal verdict: some evidence supports individualised functional goals in autistic children, while generalisation to broad behaviour change, other sensory interventions, ages or groups remains uncertain. The reviewed object preserves that disagreement and removes `sensory integration` and `sensory modulation` as exact aliases of the broader `sensory processing` concept.

## Topic claim map

| Topic | Reviewed public positions | Main falsification / reopening condition |
|---|---|---|
| Neurodiversity | collective historical development; distinguish diversity from paradigm/movement; disability/support can coexist with neurodiversity framing | stronger primary historical record or evidence that current framing systematically excludes major represented groups |
| Autism | heterogeneous lifelong condition; sensory features are variable/non-specific; language preferences vary; support should be person- and context-led | changed clinical consensus; broader language-preference evidence; stronger outcome evidence contradicting person-defined support framing |
| ADHD | developmental/lifespan condition; specialist multi-source assessment; EF differences are heterogeneous/non-specific; environment can alter impairment | changed UK diagnostic guidance; validated high-specificity biomarkers; stronger lifespan/support evidence |
| Executive function | unity plus diversity; no universal factor model; ecological validity requires real-world prediction; EF differences are transdiagnostic | replicated invariant factor model; strong out-of-sample real-world prediction; validated condition-specific EF signatures |
| Sensory processing | multidimensional/contextual; cross-diagnostic; intervention effects are outcome/fidelity/population specific; group findings do not select individual support | independent replicated trials showing broad generalisable benefits/harms, or consensus construct/diagnostic changes |

## Source-quality map

### Neurodiversity
- Botha et al. 2024 — peer-reviewed historical correction of single-originator narratives.
- Singer 2016 — historical first-person source, represented with year-only publication precision.
- Pellicano & den Houting 2022 — peer-reviewed neurodiversity-paradigm review.
- Kapp 2026 — peer-reviewed discussion of overlap/tension between neurodiversity and medical models.

### Autism
- WHO 2025 and NICE adult-autism guidance — current authoritative clinical/public guidance.
- Chen et al. 2024 — systematic review/meta-analysis of sensory differences and mental-health associations in autism.
- Schuck et al. 2025 (corrected 2026) — systematic review of autistic adults' identity-/person-first language preferences.
- Pellicano & den Houting 2022 — neurodiversity-informed research perspective.

### ADHD
- NICE NG87, last reviewed 2025 — UK diagnosis and management guidance.
- Faraone et al. 2021 — international consensus built from large studies/meta-analyses.
- Kofler et al. 2024 and Sadozai et al. 2024 — review/meta-analysis testing EF specificity and transdiagnostic patterns.
- Jurek et al. 2025 — sensory-processing meta-analysis with high heterogeneity explicitly retained.

### Executive function
- Miyake et al. 2000 — foundational unity/diversity latent-variable study.
- Karr et al. 2018 — systematic review/re-analysis of latent factor models.
- Suchy et al. 2024 — systematic review of ecological-validity claims.
- Sadozai et al. 2024 and Kofler et al. 2024 — transdiagnostic and ADHD/autism EF reviews.

### Sensory processing
- Dunn 1997 — historical occupational-therapy conceptual model.
- Chen et al. 2024 and Jurek et al. 2025 — recent autism/ADHD syntheses.
- AAP 2012 — diagnostic-boundary caution; retained as older guidance, not treated as final word on intervention evidence.
- Acuña et al. 2025 and Kishida et al. 2026 — recent systematic reviews whose different emphases are preserved rather than averaged into false certainty.

## Adversarial checks before promotion

1. No claim may rely on a source that does not reciprocally list that claim/perspective.
2. No Batch B object may encode `broader_than` or `narrower_than` with `neurodiversity`.
3. `sensory integration` and `sensory modulation` must not be encoded as exact aliases of sensory processing.
4. Executive-function measures must not be described as diagnostic biomarkers for ADHD or autism.
5. Autism language preference must not be universalised.
6. Sensory-intervention evidence must preserve outcome/population/fidelity limits and the current disagreement in review emphasis.
7. All five pre-promotion candidate objects remain preserved after authoritative review.
8. Promotion may alter only lifecycle/provenance metadata; the reviewed authoritative semantics must match the preserved candidate semantics.

## Review disposition

No evidence found in this batch requires reopening the already accepted non-taxonomic neurodiversity rule. The substantive repairs are evidence-tightening rather than a change in ND Oracle's public mission: more precise boundaries, stronger source depth, explicit heterogeneity and preserved uncertainty.

The batch is ready for schema/evidence-link validation and semantic promotion as one unit.

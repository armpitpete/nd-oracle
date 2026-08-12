# ND Oracle Batch A candidate evidence matrix

Status: **candidate research only — not authoritative, not public, not accepted**

Research date: 2026-08-12

Base main: `aec70f753d91d4636cb16c78cf31f33adb78040e`

Batch:

1. dyslexia;
2. developmental co-ordination disorder (DCD / dyspraxia);
3. Tourette syndrome and tic disorders;
4. learning disability / intellectual disability;
5. developmental language disorder (DLD).

The purpose of this file is to prepare five topics in parallel. It does not promote anything into `objects/` and it does not change the public site.

## Evidence rule for this batch

Each proposed public claim must have:

- a bounded plain-language meaning;
- at least one inspectable source;
- an explicit confidence level;
- a known boundary or counterexample;
- an uncertainty record where evidence does not justify a universal statement;
- a falsification/change test describing what evidence would make ND Oracle revise the claim.

Public guidance is used to establish current UK-facing terminology and service context. Peer-reviewed reviews/guidelines are used to test whether the public-facing simplification is supportable. Neither source type automatically outranks contradictory evidence.

---

# 1. Dyslexia

## Candidate scope

A developmental learning difference/difficulty centred primarily on reading, spelling and written language, with effects that can continue into adulthood and interact with task demands, education, work and available support.

### Include

- reading accuracy/fluency and spelling/written-language difficulties;
- childhood and adult presentation;
- assessment and support context;
- overlap with other developmental learning/language conditions;
- person-environment fit and assistive/support strategies.

### Exclude

- treating low reading attainment alone as proof of dyslexia;
- equating dyslexia with low intelligence;
- treating every difficulty with numbers, memory, planning or attention as part of dyslexia;
- individual diagnosis or a universal intervention recommendation.

## Candidate claims

### DYS-C1 — core learning profile

**Proposed wording:** Dyslexia is a learning difficulty that mainly affects reading, writing and spelling; it does not imply low intelligence.

**Candidate confidence:** high for the bounded UK-facing statement.

**Support:** NHS children guidance explicitly describes dyslexia as a common learning difficulty mainly affecting reading, writing and spelling and states that it does not affect intelligence. The adult NHS page describes continuing reading/writing difficulties and possible effects in other task areas.

**Boundary:** definitions and assessment models vary across education, psychology and research. “Does not imply low intelligence” must not be misread as requiring average or high intelligence for dyslexia.

**Would change/reduce confidence if:** strong current consensus evidence showed that the proposed wording systematically excludes recognised dyslexic people or that the intelligence wording is misleading in contemporary assessment practice.

### DYS-C2 — lifespan and context

**Proposed wording:** Dyslexic difficulties can continue into adulthood, while their practical impact varies with tasks, environment and support.

**Candidate confidence:** high for persistence; moderate for the broader person-environment formulation.

**Support:** NHS maintains separate current adult guidance, including workplace/study support. The developmental dyslexia review by Peterson and Pennington treats dyslexia as a developmental condition with multiple interacting risk factors rather than a single-cause deficit.

**Boundary:** persistence does not mean an identical profile or level of difficulty across the lifespan.

**Would change/reduce confidence if:** longitudinal evidence showed that the proposed persistence formulation is substantially wrong for recognised dyslexia populations or that environment/support has negligible practical relevance.

## Candidate uncertainties

- How should ND Oracle describe dyslexia across languages and writing systems without treating English-language assessment models as universal?
- Which assessment models best distinguish dyslexia from low educational opportunity, language difference, DLD and other causes of reading difficulty?
- Which commonly reported non-reading features belong in the core construct, and which are co-occurring or secondary?

## Candidate perspective note

Clinical/educational definitions focus on measurable literacy difficulty. Many dyslexic people also use dyslexia as part of identity and describe strengths as well as barriers. ND Oracle should not convert either framing into a universal claim about every dyslexic person.

## Candidate relations

- `narrower_than -> neurodiversity` (candidate ecosystem relation, not taxonomic diagnosis claim);
- `related_to -> adhd` (co-occurrence/overlap questions, not equivalence);
- future `related_to -> developmental-language-disorder`;
- future `related_to -> dyscalculia`.

## Initial sources

- NHS. **Dyslexia in children.** https://www.nhs.uk/conditions/dyslexia-in-children/ (accessed 2026-08-12)
- NHS. **Dyslexia in adults.** https://www.nhs.uk/conditions/dyslexia-in-adults/ (accessed 2026-08-12)
- Peterson RL, Pennington BF. **Developmental dyslexia.** Annual Review of Clinical Psychology. 2015;11:283–307. PMID 25594880. DOI 10.1146/annurev-clinpsy-032814-112842.

---

# 2. Developmental co-ordination disorder (DCD / dyspraxia)

## Candidate scope

A developmental motor-coordination condition in which motor skill acquisition/execution is below what is expected for age/opportunity and materially affects everyday activity or participation.

### Include

- fine- and gross-motor coordination;
- daily activities, education/work and participation;
- childhood through adulthood;
- assessment boundaries and co-occurrence;
- environmental/support adaptations.

### Exclude

- generic clumsiness as a diagnosis;
- acquired movement-planning difficulty after stroke, head injury or other neurological damage;
- assuming all planning, memory, emotional or social difficulties are caused by DCD;
- individual diagnosis or one universal therapy.

## Candidate claims

### DCD-C1 — developmental motor difficulty with functional impact

**Proposed wording:** DCD is a developmental condition in which motor coordination is substantially below expectation and persistently affects everyday activities or participation; diagnosis requires considering other explanations.

**Candidate confidence:** high.

**Support:** NHS diagnostic guidance requires motor skills below age/opportunity expectations, persistent effect on day-to-day activities/achievement, developmental onset and exclusion of better explanations. The international EACD clinical practice recommendations address definition, diagnosis, assessment, intervention and psychosocial impact using literature review plus formal expert consensus.

**Boundary:** DCD can coexist with other developmental conditions; an exclusion rule must not be misused to deny DCD solely because another diagnosis is present.

**Would change/reduce confidence if:** current diagnostic frameworks materially changed the functional-impact/developmental-onset requirements or high-quality evidence showed those criteria do not capture the recognised construct.

### DCD-C2 — lifespan

**Proposed wording:** DCD often continues to affect people in adolescence and adulthood, although the activities that create difficulty and the support needed can change.

**Candidate confidence:** moderate-high.

**Support:** NHS child guidance says continued problems often extend into adulthood; NHS now has a dedicated adult DCD/dyspraxia page. The international recommendations specifically added adolescent/adult evidence and recommendations.

**Boundary:** childhood motor-test performance should not be assumed to map directly onto adult participation or support needs.

**Would change/reduce confidence if:** stronger longitudinal evidence showed that adult persistence is uncommon or that current adult descriptions conflate developmental DCD with acquired dyspraxia.

## Terminology boundary — mandatory

In UK public language, **dyspraxia** is commonly used for DCD, but NHS guidance notes that healthcare professionals generally prefer **developmental co-ordination disorder (DCD)** because “dyspraxia” can also refer to movement difficulties acquired after brain injury or stroke. ND Oracle should make that ambiguity explicit rather than silently treating the terms as exact synonyms.

## Candidate uncertainties

- How reliable and accessible is adult DCD assessment in practice?
- Which measures best predict real-world participation rather than only motor-test performance?
- Which non-motor difficulties commonly attributed to “dyspraxia” are core, co-occurring or consequences of environmental demands?

## Candidate perspective note

A deficit-only motor description can miss the practical role of environment, task design and learned strategies. A strengths-oriented account must also avoid implying that all people with DCD share the same strengths.

## Candidate relations

- `narrower_than -> neurodiversity` (candidate ecosystem relation);
- `related_to -> executive-function` (task demands can overlap; not a defining equivalence);
- `related_to -> sensory-processing` (coordination and sensory demands can interact; mechanism not assumed);
- `related_to -> adhd` and `related_to -> autism` as co-occurrence questions, not identity claims.

## Initial sources

- NHS. **Developmental co-ordination disorder (dyspraxia) in children — overview.** https://www.nhs.uk/conditions/developmental-coordination-disorder-dyspraxia/ (accessed 2026-08-12)
- NHS. **Developmental co-ordination disorder (dyspraxia) in children — diagnosis.** https://www.nhs.uk/conditions/developmental-coordination-disorder-dyspraxia/diagnosis/ (accessed 2026-08-12)
- NHS. **Dyspraxia in adults (developmental co-ordination disorder).** https://www.nhs.uk/conditions/developmental-coordination-disorder-dyspraxia-in-adults/ (accessed 2026-08-12)
- Blank R et al. **International clinical practice recommendations on the definition, diagnosis, assessment, intervention, and psychosocial aspects of developmental coordination disorder.** Developmental Medicine & Child Neurology. 2019;61(3):242–285. PMID 30671947. DOI 10.1111/dmcn.14132.

---

# 3. Tourette syndrome and tic disorders

## Candidate scope

A developmental tic-disorder topic centred on Tourette syndrome, while clearly distinguishing Tourette syndrome from transient/provisional or other persistent tic disorders.

### Include

- motor and vocal tics;
- waxing/waning and context-sensitive tic expression;
- diagnosis/differential assessment;
- co-occurring ADHD/OCD and functional impact;
- treatment/support only to the degree supported by evidence and person-defined need.

### Exclude

- presenting swearing as defining Tourette syndrome;
- treating every repetitive movement/sound as a tic;
- assuming tic severity alone measures quality of life or support need;
- presenting tic suppression as automatically desirable;
- individual diagnosis or medication advice.

## Candidate claims

### TIC-C1 — current UK-facing Tourette description

**Proposed wording:** Tourette syndrome involves both motor and vocal tics with developmental onset and persistence over time; not every childhood tic means Tourette syndrome.

**Candidate confidence:** high for the bounded NHS-facing description.

**Support:** current NHS guidance describes Tourette syndrome through motor and vocal tics, onset before age 18 and duration of one year or more, and explicitly notes that many children have tics without having Tourette syndrome. European assessment guidelines review diagnostic and differential-assessment evidence.

**Boundary:** diagnostic manuals can differ in wording and criteria. ND Oracle should not claim that one public-health summary exhausts DSM/ICD distinctions.

**Would change/reduce confidence if:** current UK diagnostic guidance materially changed the defining motor/vocal, developmental-onset or persistence criteria.

### TIC-C2 — coprolalia misconception

**Proposed wording:** Swearing (coprolalia) is not required for Tourette syndrome and occurs in only a minority of people with it.

**Candidate confidence:** high for “not required”; high-moderate for “minority” without publishing a precise prevalence estimate.

**Support:** NHS lists swearing as a rare vocal tic rather than a defining symptom.

**Boundary:** avoid turning “rare” into a precise percentage unless a high-quality prevalence source is separately accepted.

**Would change/reduce confidence if:** representative epidemiological evidence contradicted the minority formulation.

### TIC-C3 — co-occurrence and treatment need

**Proposed wording:** ADHD and OCD commonly co-occur with Tourette syndrome, and treatment decisions should consider the problems a person actually experiences rather than assuming every tic needs treatment.

**Candidate confidence:** moderate-high.

**Support:** NHS identifies ADHD and OCD as common co-occurring conditions and offers treatment when tics are causing problems. Updated European guidelines cover assessment plus psychological and pharmacological treatment.

**Boundary:** the final clause is a bounded support principle, not a claim that tics never cause substantial harm or impairment.

**Would change/reduce confidence if:** current clinical guidance shifted toward routine treatment irrespective of functional burden, or co-occurrence evidence materially changed.

## Candidate uncertainties

- Which outcomes matter most to people with Tourette syndrome beyond tic counts?
- How should ND Oracle explain functional tic-like behaviours and differential diagnosis without creating self-diagnosis rules?
- What is known about adult course and adult service access relative to the childhood evidence base?

## Candidate perspective note

Some clinical outcomes emphasise tic reduction; affected people may prioritise pain, concentration, stigma, autonomy, co-occurring conditions or participation instead. The site should preserve that distinction.

## Candidate relations

- `narrower_than -> neurodiversity` (candidate ecosystem relation);
- `commonly_co_occurs_with -> adhd`;
- future relation to OCD if/when OCD exists in the corpus;
- possible `related_to -> sensory-processing` only if evidence supports a useful relation; do not add merely for graph density.

## Initial sources

- NHS. **Tourette syndrome.** https://www.nhs.uk/conditions/tourette-syndrome/ (accessed 2026-08-12)
- Szejko N et al. **European clinical guidelines for Tourette syndrome and other tic disorders—version 2.0. Part I: assessment.** European Child & Adolescent Psychiatry. 2022;31(3):383–402. PMID 34661764. DOI 10.1007/s00787-021-01842-2.
- Andrén P et al. **European clinical guidelines for Tourette syndrome and other tic disorders—version 2.0. Part II: psychological interventions.** European Child & Adolescent Psychiatry. 2022;31(3):403–423. PMID 34313861. DOI 10.1007/s00787-021-01845-z.
- Müller-Vahl KR et al. **European clinical guidelines for Tourette syndrome and other tic disorders: summary statement.** European Child & Adolescent Psychiatry. 2022. PMID 34244849.

---

# 4. Learning disability / intellectual disability

## Candidate scope

A UK-first concept page explaining **learning disability** in NHS/social-care usage, with an explicit terminology bridge to **intellectual disability** internationally and a clear separation from **specific learning difficulties** such as dyslexia.

### Include

- developmental limitations in learning/intellectual and adaptive functioning;
- wide variation in communication, independence and support needs;
- reasonable adjustments and health/service access;
- terminology differences across systems;
- rights, autonomy and supported decision-making as relevant perspectives.

### Exclude

- using “learning disability” as a synonym for dyslexia or a school-specific learning difficulty;
- reducing a person to IQ or a severity label;
- assuming autism automatically implies learning disability;
- treating one support profile as representative of everyone;
- individual diagnosis or capacity assessment.

## Candidate claims

### LD-C1 — UK definition and terminology boundary

**Proposed wording:** In UK NHS usage, a learning disability means developmental difficulty with learning/understanding and adaptive independence; it is different from a specific learning difficulty such as dyslexia. International sources often use “intellectual disability” for the corresponding concept.

**Candidate confidence:** high for the NHS distinction; moderate-high for the international terminology bridge pending a dedicated cross-system terminology source.

**Support:** NHS England describes reduced ability to understand/learn new information and skills, reduced ability to cope independently/adapt, with onset before 18, and explicitly distinguishes learning disability from learning difficulties such as dyslexia. NHS England materials also use “learning disability” and “intellectual disability” in the same identification context.

**Boundary:** terminology is jurisdiction-dependent. The page must say which usage it is following instead of declaring one label universally correct.

**Would change/reduce confidence if:** NHS terminology materially changed, or international classification evidence showed the proposed bridge conflates materially different constructs.

### LD-C2 — support needs are not one fixed profile

**Proposed wording:** People with a learning disability have widely varying abilities and support needs; some live and work independently while others need substantial lifelong support.

**Candidate confidence:** high.

**Support:** current NHS overview explicitly says no two people are the same and describes a wide range from work/relationships/independent living to greater lifelong support.

**Boundary:** examples of independence must not become an expectation or measure of a person's worth.

**Would change/reduce confidence if:** representative evidence contradicted the broad heterogeneity formulation.

### LD-C3 — diagnosis should not erase access needs

**Proposed wording:** A learning-disability label is relevant to healthcare access and reasonable adjustments, but the label alone does not specify an individual person's communication, decision-making or support needs.

**Candidate confidence:** moderate-high.

**Support:** NHS England's Learning Disability Register guidance links identification to reasonable adjustments such as longer appointments, quiet waiting areas and accessible information, while individual needs still require assessment.

**Boundary:** do not infer mental capacity from diagnosis; capacity is decision-specific and outside this concept seed unless separately evidenced.

**Would change/reduce confidence if:** policy or evidence showed that individualised adjustment assessment is not the accepted service approach.

## Terminology boundary — mandatory

For a UK audience, **learning disability** and **learning difficulty** must not be used interchangeably. Dyslexia belongs under specific learning difficulties, not learning disability in NHS usage. The page should also explain that many international clinical/research sources use **intellectual disability** where UK health and social care commonly say **learning disability**.

## Candidate uncertainties

- What is the clearest non-stigmatising way to bridge UK “learning disability” and international “intellectual disability” without implying perfect equivalence in every legal/clinical context?
- How should adaptive-functioning and intellectual-assessment evidence be presented without making IQ the person?
- How can the site include people with profound and multiple learning disabilities and non-speaking people rather than building the concept around the most independently communicating users?
- Which terms for support level are useful and which reproduce harmful functioning hierarchies?

## Candidate perspective note

Clinical classification is relevant to services and support, but rights-based and self/advocate perspectives emphasise personhood, communication access, autonomy and removal of environmental barriers. These perspectives should coexist rather than be collapsed into a single “official” account.

## Candidate relations

- `narrower_than -> neurodiversity` only if the project explicitly chooses an ecosystem relation rather than a claim that every usage of “neurodivergent” includes intellectual disability;
- `related_to -> autism` because co-occurrence is clinically recognised but neither implies the other;
- future relation to communication/AAC and reasonable adjustments;
- explicit `distinct_from -> dyslexia` would be useful if/when the schema supports a relation type that does not overstate ontology.

## Initial sources

- NHS England. **Find out about the Learning Disability Register.** https://www.england.nhs.uk/long-read/find-out-about-the-learning-disability-register/ (updated 2025-08-12; accessed 2026-08-12)
- NHS England. **Find out more about the Learning Disability Register.** https://www.england.nhs.uk/long-read/find-out-more-about-the-learning-disability-register/ (accessed 2026-08-12)
- NHS. **Learning disabilities — overview.** https://www.nhs.uk/conditions/learning-disabilities/ (accessed 2026-08-12)
- NHS. **Learning disabilities — getting support.** https://www.nhs.uk/conditions/learning-disabilities/diagnosis/ (accessed 2026-08-12)

---

# 5. Developmental language disorder (DLD)

## Candidate scope

A persistent developmental difficulty understanding and/or using spoken language that causes meaningful functional impairment and, under the CATALISE terminology, is not attributed to a known biomedical condition.

### Include

- receptive and expressive language difficulties;
- impact on communication, learning and participation;
- persistence and support across development;
- co-occurring developmental risk factors/conditions where compatible with DLD terminology;
- multilingual assessment and terminology uncertainty.

### Exclude

- treating bilingualism/multilingualism as a cause of DLD;
- treating speech-sound difficulty as synonymous with language disorder;
- acquired language disorder after neurological injury;
- language disorder explicitly associated with a known biomedical condition being silently relabelled DLD;
- individual diagnosis or one universal speech-and-language intervention.

## Candidate claims

### DLD-C1 — persistent language difficulty with functional impact

**Proposed wording:** DLD is a persistent developmental difficulty understanding and/or using language that creates meaningful problems in communication, learning or everyday life and is not attributed to a known biomedical condition.

**Candidate confidence:** high-moderate.

**Support:** the multinational CATALISE terminology consensus proposed “Language Disorder” where language problems are persistent and functionally impairing, and “Developmental Language Disorder” where the disorder is not associated with a known biomedical aetiology. Current NHS speech-and-language services use DLD for persistent difficulties understanding/using language with everyday impact.

**Boundary:** DLD is not a perfectly sharp natural category. Terminology and exclusion boundaries remain subjects of professional discussion.

**Would change/reduce confidence if:** a newer broad multidisciplinary consensus replaced the CATALISE terminology or materially changed the biomedical-association boundary.

### DLD-C2 — bilingualism is not a cause

**Proposed wording:** Learning or using more than one language does not cause DLD; assessment must distinguish a language difference from a disorder affecting the person's language-learning system.

**Candidate confidence:** high for “does not cause”; moderate-high for the assessment formulation.

**Support:** current NHS DLD services explicitly state that bilingualism/multilingualism is not a cause. CATALISE was designed partly to improve identification and terminology across heterogeneous presentations.

**Boundary:** multilingual assessment can be difficult; a child having weaker English than monolingual peers is not by itself evidence of DLD.

**Would change/reduce confidence if:** high-quality evidence showed bilingual exposure itself causally produces DLD or that the proposed assessment distinction is invalid.

### DLD-C3 — overlap without collapsing conditions

**Proposed wording:** DLD can occur alongside developmental risk factors and some other neurodevelopmental conditions, but language difficulties associated with certain known biomedical conditions are classified separately under the CATALISE framework.

**Candidate confidence:** moderate.

**Support:** CATALISE distinguishes differentiating biomedical conditions from risk factors and allows co-occurring neurodevelopmental difficulties in its terminology framework. Current NHS services describe DLD alongside conditions such as ADHD, dyslexia, dyscalculia and speech-sound difficulties.

**Boundary:** this is precisely where careless wording can misclassify autism-associated language disorder as DLD. The final page must use examples only after the terminology cross-check is complete.

**Would change/reduce confidence if:** updated consensus evidence rejects the CATALISE distinction or demonstrates that the proposed co-occurrence wording is misleading.

## Candidate uncertainties

- How consistently is CATALISE terminology implemented across UK NHS services and adult services?
- How should DLD be assessed across multilingual populations and culturally different language environments?
- Where should ND Oracle draw the public-facing boundary between DLD, speech-sound disorder, literacy disorder/dyslexia and language disorder associated with autism or hearing loss?
- What adult outcome/support evidence is strong enough for a lifespan claim?

## Candidate perspective note

A diagnostic label can improve recognition and access to support, but DLD is heterogeneous and labels can also obscure individual communication profiles. The page should state both functions rather than presenting the category as perfectly discrete.

## Candidate relations

- `narrower_than -> neurodiversity` only as an ecosystem relation if accepted;
- future `related_to -> dyslexia`;
- `related_to -> adhd` as a co-occurrence relation, not equivalence;
- `related_to -> autism` only with wording that preserves the CATALISE diagnostic boundary rather than implying DLD is the name for autistic language differences.

## Initial sources

- Bishop DVM, Snowling MJ, Thompson PA, Greenhalgh T; CATALISE-2 consortium. **Phase 2 of CATALISE: a multinational and multidisciplinary Delphi consensus study of problems with language development: Terminology.** Journal of Child Psychology and Psychiatry. 2017;58(10):1068–1080. PMID 28369935. DOI 10.1111/jcpp.12721.
- Bishop DVM. **Why is it so hard to reach agreement on terminology? The case of developmental language disorder (DLD).** International Journal of Language & Communication Disorders. 2017;52(6):671–680. DOI 10.1111/1460-6984.12335.
- Bedfordshire and Luton Children's Health / NHS. **Developmental Language Disorder (DLD).** https://bedslutonchildrenshealth.nhs.uk/services/bedfordshire-and-luton-childrens-speech-and-language-therapy-service/developmental-language-disorder-dld/ (accessed 2026-08-12)
- NELFT NHS Foundation Trust. **Developmental Language Disorder (DLD).** https://www.nelft.nhs.uk/developmental-language-disorder-dld/ (accessed 2026-08-12)
- Alder Hey Children's NHS Foundation Trust. **Developmental Language Disorder.** https://www.alderhey.nhs.uk/conditions/patient-information-leaflets/developmental-language-disorder/ (accessed 2026-08-12)

---

# Batch-level adversarial checks

These are mandatory before creating candidate concept JSON.

## A1 — dyslexia and intelligence

Try to falsify the wording “does not imply low intelligence” by checking whether contemporary diagnostic practice requires an IQ discrepancy, whether people with intellectual disability can also have specific reading disorders, and whether the NHS wording could be misunderstood as an exclusion rule.

**Current position:** retain the anti-stigma statement but do not turn it into an IQ eligibility criterion.

## A2 — DCD versus dyspraxia

Try to falsify the assumption that the labels are synonyms across all contexts.

**Current position:** assumption fails. NHS explicitly documents broader/acquired uses of “dyspraxia”; use DCD as the precise developmental label and explain common UK usage.

## A3 — Tourette and swearing

Try to falsify the popular assumption that coprolalia defines Tourette syndrome.

**Current position:** assumption fails. Current NHS guidance identifies swearing as rare and does not make it a diagnostic requirement.

## A4 — learning disability versus learning difficulty

Try to falsify any draft that treats UK “learning disability” as a broad umbrella containing dyslexia.

**Current position:** such a draft would be wrong in NHS usage. The distinction must be explicit on the page and in graph relations.

## A5 — DLD as a perfectly discrete condition

Try to falsify any draft that treats DLD as a sharp biological category or assumes every developmental language difficulty with another diagnosis is DLD.

**Current position:** reject that simplification. Preserve the CATALISE terminology boundary and the acknowledged heterogeneity/overlap.

---

# Batch-level gaps before candidate JSON

1. Obtain a dedicated current international terminology/classification source for the UK `learning disability` ↔ `intellectual disability` bridge rather than relying only on NHS contextual usage.
2. Check current dyslexia assessment consensus on IQ-discrepancy models and multilingual/orthographic variation before finalising exclusions.
3. Check current Tourette/tic disorder classification wording against both ICD and current UK practice before freezing exact diagnostic language.
4. Check whether a newer DLD consensus has superseded or materially modified CATALISE since 2017.
5. Decide whether `narrower_than -> neurodiversity` is semantically acceptable for all five or whether ND Oracle needs an explicit `commonly_included_in_neurodiversity_discourse` relation rather than forcing a taxonomic hierarchy.

Until those five checks are resolved, **no Batch A object should be promoted into `objects/concepts/`.**

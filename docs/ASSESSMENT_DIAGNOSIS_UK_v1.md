# Assessment & Diagnosis — UK reference contract v1

Date: 2026-09-03
Base: `b4894eb557ce04a4822ae664bb1e3de99de421a4`

## Purpose

Define a bounded, jurisdiction-aware UK reference implementation for neurodevelopmental assessment and diagnosis without weakening ND Oracle's frozen clinical, jurisdiction, privacy, provenance, discovery or release-state boundaries.

This contract starts with autism and ADHD because the repository already contains governed Concepts and England adult assessment Questions for both. It deliberately distinguishes national guidance from local service practice and does not imply that screening, self-identification, educational assessment, needs assessment and formal clinical diagnosis are interchangeable.

## Jurisdiction model

The UK is represented as four separate national service contexts:

- England
- Scotland
- Wales
- Northern Ireland

National guidance may coexist with sub-national service variation:

- England: local NHS/ICB/provider pathways can vary; NHS Right to Choose is England-specific.
- Scotland: NHS inform explicitly states that there is no standard ADHD assessment approach across Scotland and pathways depend on the health board.
- Wales: health-board neurodevelopmental and adult ADHD routes vary; the Welsh Government Neurodivergence Improvement Programme is working on more consistent pathways and adult ADHD options.
- Northern Ireland: autism pathways are Trust-based; 2026 Department of Health evidence records uneven and incompletely commissioned adult ADHD provision across HSC Trusts.

A local service record may narrow a national context but must never be promoted into a national rule merely because it is the best available first-party example.

## Route dimensions

Every Assessment & Diagnosis route must make the following dimensions explicit in its governed text or route identity where they materially affect access:

1. jurisdiction;
2. age group (adult or child/young person);
3. condition or assessment target;
4. public/NHS/HSC versus private route;
5. referral mechanism where evidenced;
6. assessment stage;
7. national versus local service authority;
8. review date and reopening conditions.

No new schema is required for v1. The current Question and Resource objects can carry these dimensions through exact governed wording, related objects, limitations and provenance. Jurisdiction containment remains owned by the frozen discovery scope mechanism.

## Clinical boundary

ND Oracle may explain:

- how to seek an assessment;
- who may refer;
- what an assessment commonly involves;
- current public/private access distinctions;
- waiting-list and pre-assessment support routes;
- what may happen after an assessment;
- how a person can ask a service to explain or review an outcome;
- where local pathways differ.

ND Oracle must not:

- diagnose a person from symptoms, scores, chat text or screening tools;
- treat a checklist as diagnostic proof;
- recommend whether a person should obtain a diagnosis;
- recommend a named private provider as clinically suitable;
- recommend medication, dose changes, titration or shared-care decisions;
- imply that an educational or workplace adjustment always requires a formal diagnosis;
- silently import England-only Right to Choose into Scotland, Wales or Northern Ireland.

## Assessment-type distinctions

The public material must preserve these distinctions:

- **screening:** an initial aid or triage input; not a diagnosis;
- **clinical diagnostic assessment:** a specialist process capable of reaching a clinical diagnostic conclusion;
- **educational assessment:** assessment for learning needs or specific learning differences; not automatically a medical diagnosis;
- **occupational/functional assessment:** assessment of function or support need; not automatically diagnostic;
- **needs assessment:** identifies support needs and may be useful whether or not a diagnosis is present.

## Adult autism baseline

Each nation needs a governed Question covering how to start, referral/self-referral where evidenced, what assessment may involve, waiting/local variation, private-assessment caveats, disagreement/no-diagnosis routes and post-assessment support.

England additionally exposes Right to Choose as an England-only NHS choice route.

## Adult ADHD baseline

Each nation needs a governed Question covering how to start, specialist assessment, local variation, waiting, private-assessment caveats and post-assessment support.

Diagnosis is kept separate from medication initiation, titration, prescribing and shared care.

## Children and young people baseline

Each nation needs separate autism and ADHD Questions covering the roles of family, school/nursery, GP/health visitor and local neurodevelopmental services where evidenced. Support while waiting must be represented without implying that support is conditional on diagnosis.

## Cross-cutting routes

The UK reference candidate must also cover:

- private assessment quality/acceptance checks;
- waiting for assessment and support without diagnosis;
- referral refusal, disagreement and second-opinion/review routes where evidenced;
- post-assessment and no-diagnosis outcomes;
- reasonable communication/sensory adjustments during assessment;
- co-occurring autism/ADHD and the possibility of broader neurodevelopmental assessment.

These routes may be UK-wide only when their wording explicitly preserves nation/local variation. A UK-wide route must not convert a nation-specific entitlement into a UK entitlement.

## Source hierarchy

Preferred order:

1. national government or national health service;
2. NICE or equivalent national clinical guidance where applicable;
3. national programme/service guidance;
4. health board/HSC Trust/local NHS provider for explicitly local practice;
5. professional regulator/body;
6. peer-reviewed evidence where a serious proposition cannot be supported by first-party operational material.

Provider/service identity and access listings remain claimless Resources unless ND Oracle is making a separately governed testable proposition.

## Private assessment rule

Private assessment is not one UK-wide acceptance regime.

The public route must tell readers to check, before paying, whether the relevant NHS health board/HSC Trust/local service/GP will accept or act on the report and what follow-up is included. This is especially important for ADHD because diagnosis, prescribing, titration and shared care are distinct decisions.

ND Oracle does not maintain an 'approved private provider' list in v1.

## Waiting and support rule

Waiting for assessment must not be represented as 'wait without support'. Where authoritative material supports it, routes should point to needs-led help available before diagnosis in health, education, work and communication/access contexts. Existing adjustment Questions may be linked rather than duplicated.

## Outcome rule

An assessment can result in diagnosis, no diagnosis, a request for more information, watch-and-wait/review, or another explanation/route. ND Oracle must represent no-diagnosis and disagreement without treating either the assessor or the user as automatically wrong.

## Other neurodevelopmental assessments

The architecture must remain capable of extending to dyslexia, developmental coordination disorder/dyspraxia, dyscalculia, Tourette/tic disorders, speech/language/communication assessment and learning-disability/intellectual-developmental assessment. Those routes must preserve the clinical/educational distinction rather than forcing all neurodevelopmental differences into one medical pathway.

## International compatibility

The UK model is the reference implementation for later international work. It must generalise to:

`country -> state/province/region -> local service area -> age group -> assessment type -> public/private/funding route -> source -> reviewed date`

International expansion must not begin by manufacturing empty country shells. A country is added only when useful first-party or otherwise authoritative pathway evidence can be maintained.

## Acceptance gates

Before the UK autism/ADHD reference implementation can be called complete:

- four adult autism nation routes exist;
- four adult ADHD nation routes exist;
- four child/young-person autism nation routes exist;
- four child/young-person ADHD nation routes exist;
- private assessment, waiting/support, disagreement/outcome, assessment-adjustment and co-occurrence routes exist;
- all nation-specific routes have exact jurisdiction scope provenance;
- England Right to Choose cannot surface as a Scotland/Wales/Northern Ireland entitlement;
- clinical diagnosis and medication hostile boundaries remain unchanged;
- national guidance and local service examples are explicitly distinguished;
- full schema/governance/freshness/evidence/discovery regression passes;
- hostile diff review passes;
- protected exact-head merge authority is separately granted;
- post-merge and production reconciliation occur before FINAL PASS.

## Non-goals for this candidate

- no personalised diagnostic inference;
- no provider ranking;
- no medication or prescribing advice;
- no new schema solely to model geography;
- no graph database;
- no analytics, profiling or query storage;
- no production deployment without separate exact-SHA authority;
- no claim that every UK local service has been catalogued.

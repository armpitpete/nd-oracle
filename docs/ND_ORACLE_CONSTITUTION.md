# ND Oracle Constitution / Product Requirements v0.1

**Status:** Proposed for acceptance  
**Date:** 2026-08-10

## Mission

> **Build an ND-centred knowledge system that helps people understand neurodivergence, navigate uncertainty, and find useful resources without having to repeatedly decode the world.**

The ND Oracle exists to reduce repeated research effort, information fragmentation, uncertainty rediscovery, and cognitive overhead when seeking understanding, support, or useful resources.

Success is measured by **epistemic work saved**, not by page count, content volume, or the number of AI-generated answers.

## Governing epistemic rules

### 1. Preserve identified uncertainty

> **Never make the next person rediscover an uncertainty already identified.**

The system must preserve unresolved questions, competing explanations, evidence gaps, limitations, and serious disagreements. An unknown is a knowledge object, not a failure to hide.

### 2. Every serious question improves the system

> **Every serious question should leave the knowledge system better than it found it.**

A serious investigation should contribute reusable epistemic work: sources assessed, claims clarified, uncertainties identified, hypotheses weakened or strengthened, or research gaps made more precise.

### 3. Preserve the route to conclusions

> **No conclusion without its route back to the evidence and uncertainty that produced it.**

Significant conclusions and claims must remain traceable to supporting evidence, counterevidence, uncertainty, scope, confidence, and conditions under which they should be reconsidered.

### 4. Measure saved reasoning, not generated text

> **Measure success by epistemic work saved, not text produced.**

The system should reduce duplicated investigation and preserve work that later users can inherit. A concise answer with inspectable provenance is preferable to a large body of unsupported prose.

## ND-centred design requirement

Neurodivergent people are primary users of the system, not merely its subject matter.

The system must reduce the cognitive load required to find, understand, compare, and use information. It should not require users to first understand professional terminology, information architecture, diagnostic categories, or the internal ontology before receiving useful help.

ND-centred design does **not** mean lowering evidential standards, presenting neurodivergence only positively, or suppressing impairment, harm, uncertainty, or disagreement.

It means optimising for clarity, predictability, autonomy, multiple routes into knowledge, and reduced unnecessary decoding.

## User experience principles

### Reading first

The public interface should feel like a calm reading and thinking environment rather than a dashboard.

Prefer:

- roughly consistent body text sizing;
- hierarchy through **bold**, *italic*, spacing, indentation, and restrained dividers;
- short summaries before deeper material;
- progressive disclosure of detail;
- predictable navigation;
- low visual competition.

Avoid unnecessary giant headings, tiny metadata, dense card grids, gamified engagement, and attention-seeking interface elements.

### Multiple routes into knowledge

Users must be able to begin with:

- a diagnosis or identity term;
- an experience;
- a difficulty or need;
- a practical question;
- a tool, game, app, service, or other resource;
- an uncertainty or disagreement.

The system should connect ordinary language such as “I can’t start tasks” to relevant concepts without requiring the user to know terms such as “task initiation” or “executive function” first.

### Preserve user control

Where practical, users should be able to choose between:

- a short answer;
- deeper explanation;
- evidence and provenance;
- lived-experience perspectives;
- practical resources;
- open questions and uncertainty.

The system should not force one preferred depth or explanatory framing on every user.

### Explain connections

The knowledge graph must ultimately answer not only **what is connected**, but **why it is connected**.

Relationships should progressively support rationale, evidential basis, confidence, scope, and uncertainty rather than becoming unexplained graph edges.

## Knowledge integrity principles

The Oracle must keep distinct kinds of knowledge distinct.

### Evidence

Research findings, authoritative records, measurements, and other inspectable evidence relevant to a claim.

### Lived experience

What neurodivergent people and others report experiencing. Lived experience is legitimate knowledge about experience and practical reality; it is not automatically evidence for a separate causal, diagnostic, or biological claim.

### Perspective

A sourced interpretation or position held by a person, community, profession, institution, or other identifiable group. No perspective should be silently presented as universal for the group that contains it.

### Resource

Something that exists and may be useful: for example a tool, game, app, book, service, organisation, community, accommodation, guide, product, or media work.

A resource may deserve inclusion without clinical evidence. Claims that a resource produces particular outcomes require evidence appropriate to those claims.

### Claim

A proposition whose wording and scope determine what evidence is relevant to it. Confidence attaches to the exact claim, not to a topic or source as a whole.

These categories must not silently collapse into one another.

For example:

> Many autistic people report using noise-reduction tools.

is not equivalent to:

> Noise-reduction tools are clinically proven to improve outcomes for autistic people.

## Scope

The ND Oracle covers the **full neurodiversity ecosystem**.

This includes, but is not limited to:

- autism, ADHD, dyslexia, dyspraxia/DCD, dyscalculia, Tourette syndrome, and other relevant neurodevelopmental or neurodivergent concepts;
- traits, experiences, needs, and practical difficulties;
- research, theories, competing explanations, and unknowns;
- lived experience and community knowledge;
- terminology, history, politics, policy, rights, and institutional classifications;
- accommodations and practical strategies;
- tools and assistive technology;
- apps and software;
- games, including games valued for enjoyment or social connection rather than treatment;
- books, media, guides, and courses;
- services and organisations;
- communities and peer resources;
- education and workplace resources;
- products relevant to neurodivergent life.

The Oracle must not become a clinical encyclopedia with resources added as an afterthought.

## Resource principles

Resources should be evaluated according to the claims actually made about them.

The system should distinguish:

- documented properties;
- accessibility features;
- price and availability;
- reported user experience;
- practical utility;
- evidentially supported outcomes;
- limitations, burden, privacy concerns, conflicts of interest, and harms.

Popularity, commercial visibility, search ranking, or institutional recommendation must not automatically become evidence of effectiveness.

Games and media should not be treated only as therapeutic instruments. Enjoyment, structure, creativity, social connection, sensory characteristics, accessibility, and personal fit are legitimate reasons for inclusion.

## Uncertainty and disagreement

The Oracle should expose disagreement clearly rather than compressing it into vague statements such as “this is controversial.”

Where serious interpretations differ, the system should preserve:

- what the positions actually claim;
- what evidence each relies on;
- where they agree;
- where they conflict;
- what evidence would discriminate between them;
- what remains unresolved.

Uncertainty should never be collapsed merely to make an answer easier to read.

## AI role

AI may accelerate discovery, extraction, comparison, gap detection, drafting, and navigation.

AI is **not** the authority of record.

Where claims enter the accepted knowledge layer, they must satisfy the system’s provenance and review rules. AI-generated prose without a preserved evidence route must not become accepted knowledge merely because it sounds plausible.

The Oracle interface may use AI to navigate the accepted knowledge system, but the knowledge system must remain independently inspectable.

## Search and Oracle behaviour

The search system should understand intent rather than merely match keywords.

It should support questions such as:

- What is this?
- Why might this happen?
- What is known?
- What is disputed?
- What do people report?
- What might help?
- What tools, games, services, or resources exist?
- What remains unknown?

Search activity may reveal unmet needs and research gaps, but user queries must not automatically become factual evidence.

## Anti-goals

The ND Oracle must not become:

### A diagnosis engine

It should not diagnose individuals or present probabilistic pattern matching as a clinical diagnosis.

### A treatment marketplace

Commercial presence and resource listings must not become endorsements.

### A positivity filter

Impairment, distress, discrimination, adverse effects, and difficult evidence remain part of the map.

### An authority replacement

The Oracle should help users inspect evidence and options. It does not replace appropriate professional, legal, clinical, educational, or safeguarding judgement.

### A content factory

Producing more prose is not success if the same reasoning has to be repeated later.

### A conventional website by default

The system should not reproduce standard web patterns simply because they are familiar when those patterns add cognitive load without helping understanding.

## Feature acceptance test

Before a significant feature is accepted, ask:

1. Does this reduce cognitive or epistemic work for ND users?
2. Does it preserve important uncertainty rather than hiding it?
3. Can users understand why information is connected?
4. Does it keep evidence, lived experience, perspective, and resource claims appropriately distinct?
5. Does it help users navigate without requiring unnecessary specialist decoding?
6. Does it preserve or increase reusable epistemic work?

A feature that fails these tests requires a clear justification or should not be built.

## Relationship to implementation

This constitution sits above implementation choices.

Database technology, graph libraries, AI models, search engines, hosting providers, interface frameworks, and visual design systems are replaceable components.

They must serve this constitution rather than redefining it.

The accepted knowledge base should remain exportable, versioned, and inspectable so that the public knowledge asset is not trapped inside one website or vendor.

## Change control

Material changes to this constitution should be explicit, versioned, reviewable, and preserve the reason for the change.

A later version must not silently erase an earlier governing requirement. Superseded versions should remain available as historical provenance.

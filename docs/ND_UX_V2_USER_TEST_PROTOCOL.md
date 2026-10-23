# ND-UX-V2 human task-test protocol

Date: 2026-09-29
Status: required before final V2 Public Baseline freeze

## Rule

Automated route tests, screenshots and AI review are not a substitute for real neurodivergent task evidence. Do not mark this gate PASS from automated checks, screenshots or AI simulation.

The current Home repair is deliberately bounded: test the six first choices, Search, secondary exploration and first-hop recovery. Do not turn this test into a general redesign of ND Oracle.

## Before testing

Record the exact candidate SHA and confirm the participant is testing that exact build.

For the current-vs-candidate comparison, record the current baseline at a high level:

- number of immediately prominent Home choices;
- number of competing first-level classification systems;
- obvious hesitation/backtracking already observed;
- any known route-comprehension failures.

The purpose is to determine whether the candidate **reduces decision burden without losing useful findability**.

## First-impression check

Without explaining ND Oracle terminology, ask:

> **Without clicking anything, what kinds of things do you think you can find on this website?**

The participant should be able to identify concrete things such as neurodivergence/conditions, books/media, games/apps, practical help or support.

## Primary-label comprehension

Before explaining any route, point to each of the six primary headings in turn and ask:

> **What would you expect to find here?**

Do not correct the participant until the six headings have been checked.

Record unexpected interpretations, especially for:

- ADHD, autism & other neurodivergence;
- Help with everyday life;
- Books, films & media;
- Games & apps;
- Find support;
- Ask a question.

## Candidate journeys

Ask the participant to attempt these without facilitator guidance:

1. **Find information about ADHD.**
2. **Find a book about an autistic young person.**
3. **Find something that could help with starting tasks.**
4. **Find an app.**
5. **Find help with sensory overload.**
6. **Find a local neurodivergent peer group.**
7. **Find help with school or study.**
8. **Find help with work.**
9. **You do not know the correct word for the problem. Find somewhere sensible to start.**
10. **Use Search to look for something you already know you want.**
11. **Open More ways to explore and find the A–Z.**
12. **Deliberately choose the wrong first route, then recover without assistance.**

The wrong-route task is mandatory: a simplified first decision is only safe if a mistaken choice is easy to undo.

## Existing fixed journeys

The broader V2 gate still retains these established journeys for continuity:

1. “I think I might have ADHD. Where do I begin?”
2. “Phone calls are difficult.”
3. “I need help at work.”
4. “My child struggles with eating.”
5. “What is monotropism?”
6. “I want an autistic peer group.”
7. “I don't know the correct word for my problem.”
8. “I need help but I don't know which section.”
9. “I want to understand the evidence behind this.”
10. “I live outside England.”

Where one candidate journey clearly covers the same behaviour, one observed run may support both records, but do not invent a PASS for an untested behaviour.

## Record for each journey

Record only what is needed:

- first choice;
- route reached;
- hesitation or pause that appears meaningful;
- navigation steps;
- backtracks;
- wrong first route;
- whether recovery succeeded;
- terminology confusion;
- scanning/overload notes;
- whether colour/location helped reorientation;
- whether Search was obvious;
- whether the participant could explain where they were and how to get back;
- **Found it / Confusing / Couldn't find it**;
- PASS / PARTIAL / FAIL with a short moderator reason.

Do not ask only whether the participant “likes” the page.

## Interpretation

One person's hesitation is evidence to inspect, not an automatic redesign instruction.

Repeated confusion by multiple participants around the same label or route is evidence of a likely design problem.

Aesthetic preference alone does not block release unless it causes a demonstrated usability or accessibility failure.

Repairs are limited to demonstrated problems in the Home/header/secondary-navigation/first-hop scope.

## Wrong-choice recovery acceptance

A participant who chooses the wrong first route must be able to recover by one of these ordinary mechanisms:

- return to the six Home choices;
- use Search;
- use browser Back;
- follow an obvious related route.

A dead end or need for facilitator rescue blocks acceptance.

## Accessibility spot-check

At least one human/assistive-technology pass must verify:

- keyboard-only navigation;
- logical focus order;
- the six route names make sense when heard without relying on colour/layout;
- Search is reachable;
- Menu is operable as a native disclosure;
- More ways to explore announces and behaves as collapsed/expanded;
- 200% browser/text zoom remains usable;
- colour is not the only route distinction.

Use VoiceOver on iOS/macOS or an equivalent screen reader where available.

## Young-person safeguard

If actual minors are tested:

- define the intended age range before recruitment;
- use appropriate parent/guardian consent and participant assent where required;
- do not request diagnosis proof, medical records or unnecessary health disclosure;
- minimise identifiable information;
- obtain explicit permission before audio/video/screen recording;
- define how notes/recordings are stored and deleted;
- prepare an age-appropriate safeguarding/escalation procedure before the session;
- use neutral tasks that do not require disclosure of the young person's own sensitive circumstances.

The interface can be tested without collecting a child's medical history.

## Evidence handling

Keep participant evidence anonymous and minimal. Do not store diagnostic proof or unnecessary personal details.

For each finding, record:

- finding;
- severity;
- whether it is reproducible;
- disposition: ACCEPT / REPAIR / REJECT;
- reason;
- exact repair if required.

After repairs, re-run the affected task on the fresh exact-head candidate.

## Stop conditions

The final V2 freeze is blocked by:

- repeated severe misrouting around the same primary label;
- inability to recover from a wrong first choice;
- hidden essential content;
- inaccessible controls;
- repeated wrong-jurisdiction exposure;
- task failure without a reasonable alternate route;
- a blocking assistive-technology defect.

Do not expand the repair into unrelated destination architecture, taxonomy or typography work.

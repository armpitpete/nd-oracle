# Question-led discovery v0.7

## Goal

Move ND Oracle from separate topic/resource catalogues toward ordinary-question discovery without introducing an AI authority layer.

The v0.7 foundation uses the existing governed `question` object. A practical Question links an ordinary user need to already reviewed Concepts and Resources, gives a bounded current synthesis, keeps evidence gaps explicit, and records conditions that should reopen the answer.

## First five practical questions

1. Task starting and organisation.
2. Games with little or no time pressure.
3. Workplace support in Great Britain.
4. Choosing the right kind of autism information/support organisation.
5. Autism-oriented anxiety/self-management tools in the current catalogue.

## Product rule

A Question route means **relevant to inspect**, not **recommended**, **proven effective**, or **suitable for a diagnosis**.

Question synthesis may compare already governed descriptive facts and limitations. It must not manufacture efficacy, safety, clinical, legal or personalised-fit claims that do not have their own governed evidence route.

## Public interface sequence

The first slice establishes valid Question objects and cross-object routes. The next slice publishes a static question index and canonical question pages, then makes practical questions the first discovery layer from the homepage.

No free-text chatbot is required for v0.7. The useful architecture is:

`ordinary question -> governed Question object -> relevant Concepts/Resources -> inspectable evidence/uncertainty`

## Acceptance criteria for this foundation

- All practical Question objects validate against schema v0.2.
- Every related object resolves to an authoritative object in the repository.
- Current understanding is bounded by the reviewed corpus.
- Evidence gaps and reopening conditions remain explicit.
- No Resource listing is silently converted into an efficacy or endorsement claim.
- Repository validation and regression tests pass with the expanded mixed-type corpus.

# ND Oracle v1.2 need coverage audit v0.2

Baseline: protected post-#124 `main` at `efce179eb111a0706839bc7ee1e19ed2a448fe3b` (tree `fe7fb4a565676b4383b0d11eddb2231bd7d398fb`).

Status: evidence audit only. It does not authorise content, ranking changes, merge or deployment.

## Fresh execution evidence

The audit was executed through temporary draft PR #126 and then removed from the research branch. PR #126 was closed unmerged.

- workflow run: `33441406491`
- job: `99650253510`
- executed corpus: 125 governed objects
- regression suite in the audit run: 333 tests, all passing
- frozen public compatibility: PASS
- current Question contract: 41, PASS
- temporary probe assertion: the three devolved disabled-student-support routes remain correct

## Corpus

- Concepts: 20
- Resources: 61
- Questions: 41
- Evidence: 3
- Total: 125

The v1.2 v0.1 student-support slice therefore changed the prior audit baseline from 119 to 125 objects without changing schemas or the accepted v1.1 discovery architecture.

## What v0.1 fixed

Fresh deterministic probes now select the intended governed Question first for all three new higher-education routes:

| Query | Current top route | Result |
| --- | --- | --- |
| `disabled student support Scotland` | `/questions/disabled-student-support-scotland/` | FIXED |
| `disabled student support Wales` | `/questions/disabled-student-support-wales/` | FIXED |
| `disabled student support Northern Ireland` | `/questions/disabled-student-support-northern-ireland/` | FIXED |

Related `exam adjustments Scotland neurodivergent` and `exam adjustments Wales neurodivergent` now also orient to the matching national student-support Question rather than work-adjustment material.

## Remaining evidence-backed gaps

### 1. Healthcare communication and access adjustments — highest-priority coherent slice

All three devolved healthcare probes still select an unrelated domain:

| Query | Current top route |
| --- | --- |
| `healthcare communication adjustments Scotland` | `/questions/disabled-student-support-scotland/` |
| `healthcare communication adjustments Wales` | `/questions/disabled-travel-support-wales/` |
| `healthcare communication adjustments Northern Ireland` | `/questions/disabled-student-support-northern-ireland/` |

This is a strong content/jurisdiction gap, not evidence for loosening lexical eligibility. England already has the parallel governed Question/Resource route.

### 2. Northern Ireland work support

- `reasonable adjustments at work Northern Ireland` -> Northern Ireland DSA Resource.
- `Access to Work Northern Ireland` -> Northern Ireland disabled-student-support Question.

This needs a separately sourced NI employment/support slice; Great Britain routes must not be stretched across Northern Ireland.

### 3. Adult assessment outside England

All six Scotland/Wales/Northern Ireland autism/ADHD assessment probes still return benefits, student-finance or generic information material rather than a practical national assessment route. One fresh Wales autism probe now returns the new Student Finance Wales DSA Resource first, showing that additive scoped content can create new collisions when the underlying need remains uncovered.

This remains important but is higher-risk than healthcare-access navigation because diagnostic pathways vary locally and carry a stronger clinical-boundary burden.

### 4. Hard no-match everyday needs

The following still end in `no_match`:

- `housework is overwhelming ADHD`
- `shopping is overwhelming autism`
- `smells make me overwhelmed`
- `friendship misunderstandings autism`
- `debt paperwork disability help`

These are genuine coverage leads. They are not permission to add generic synonyms without governed practical content.

### 5. Other wrong-domain routes

- `disabled travel support England` -> England Disabled Students' Allowance Resource.
- `school transition support autism England` -> adult autism assessment Question.
- `occupational health neurodivergent adjustments` -> England healthcare-adjustments Question.
- `clothes feel painful sensory` -> masking/burnout Question.
- `help remembering appointments neurodivergent` -> neurodivergent-parent admin Question.

These should be ranked separately rather than bundled into one broad routing patch.

## Ranking for the next bounded slice

1. **Healthcare communication/access adjustments: Scotland, Wales, Northern Ireland.** Three clear wrong-domain jurisdiction probes; direct parity with an existing England route; current national sources exist; relatively low clinical-risk navigation scope.
2. **Northern Ireland work support.** High practical value and clear jurisdiction defect, but requires careful separation from Great Britain employment law/support routes.
3. **Adult autism/ADHD assessment outside England.** High usefulness but greater clinical/pathway complexity and local variation.
4. **Everyday no-match cluster.** High lived usefulness, but source authority and bounded object design need more research.
5. **Single-domain navigation gaps** such as England concessionary travel and school transition support.

## Architecture interpretation

The v1.2 additions validate the content-first strategy: the intended student-support queries are now correct without changing ranking weights, jurisdiction containment, clinical boundaries or orientation. At the same time, additive content exposed new collisions in still-uncovered domains. The correct response is therefore to add evidence-backed governed routes one bounded need at a time, with explicit scope provenance and regression controls, rather than make the ranker more permissive.

Frozen boundaries remain:

- compositional personal clinical-decision boundary;
- complete requested-jurisdiction containment;
- meaningful lexical eligibility;
- exact governed route-scope provenance;
- deterministic Python/browser parity;
- orientation disabled;
- no external search, accounts, analytics, query persistence, profiling, personalised ranking or AI answer authority.

# ND Oracle whole-site content inventory v0.3

Status date: 2026-08-12

Promotion candidate base: `46366ea5d14f2832e7df3a48c320719c6475376e`

This inventory describes the proposed authoritative corpus on `agent/promote-batch-a-v0.3`. It supersedes the five-topic v0.2 inventory only if the promotion PR is merged.

## Corpus totals

| Measure | v0.2 | v0.3 candidate |
|---|---:|---:|
| Authoritative concepts | 5 | 10 |
| Claims | 10 | 27 |
| Sources | 10 | 32 |
| Open uncertainties | 10 | 28 |
| Perspectives | 6 | 11 |
| Relations | 13 | 23 |
| Ecosystem entry-point groups | 19 | 34 |
| Reviewed concepts | 0 | 5 |
| Concepts with `last_reviewed` | 0 | 5 |

## Added reviewed concepts

| Concept | Claims | Sources | Uncertainties | Perspectives | Relations | Review state |
|---|---:|---:|---:|---:|---:|---|
| Dyslexia | 3 | 5 | 3 | 1 | 2 | editor_reviewed |
| Developmental co-ordination disorder | 3 | 4 | 3 | 1 | 3 | editor_reviewed |
| Tourette syndrome | 3 | 4 | 5 | 1 | 1 | editor_reviewed |
| Learning disability | 4 | 4 | 3 | 1 | 2 | editor_reviewed |
| Developmental language disorder | 4 | 5 | 4 | 1 | 2 | editor_reviewed |
| **Batch total** | **17** | **22** | **18** | **5** | **10** |  |

The original five concepts remain authoritative `seed` / `unreviewed_seed` objects. Their review debt is not concealed by the new batch.

## Public surface if promoted

The generated `/understand/` surface expands from five to ten concept pages. The five added routes are:

- `/understand/dyslexia/`
- `/understand/developmental-coordination-disorder/`
- `/understand/tourette-syndrome/`
- `/understand/learning-disability/`
- `/understand/developmental-language-disorder/`

The homepage topic count is derived mechanically from the authoritative corpus rather than hardcoded. The sitemap is likewise generated from the corpus, so all ten canonical concept routes are included automatically.

## Preserved boundaries

- The accepted candidate blobs remain under `migration-candidates/topic-expansion-batch-a/candidates/`.
- Promotion does not add a taxonomic `broader_than` / `narrower_than` edge from any Batch A concept to `neurodiversity`.
- `dyspraxia` is explained but is not encoded as an exact DCD alias.
- `intellectual disability` and `disorder of intellectual development` are explained but are not encoded as exact aliases of UK `learning disability`.
- Dyslexia is not described as a `learning disability` in the UK-facing summary.
- All accepted uncertainty records remain open and visible.

## Remaining corpus debt after this promotion

The site would have materially better breadth, but completion work remains:

1. review the original five seed concepts to the same standard;
2. continue the ranked topic backlog rather than returning to one-source-at-a-time work;
3. add cross-cutting experiences only where their evidence status and terminology are explicit;
4. reconsider public search/evidence browsing when the corpus becomes large enough that simple browsing stops being sufficient.

# D12 — Singer 2017 revised-print date enrichment

Prepared on 2026-08-11 against protected `main` `f56355b7edaec7fad020bebeab0d80ec04ebc37e`.

## Owner decision

Accepted:

> Accept `nd-singer-2017-date-enrichment`: use `2017-09-05` as the full publication date for the future non-authoritative `neurodiversity-source-singer-2017-revised-print` Evidence identity candidate, based on ISBN-bound catalogue corroboration. Preserve the authoritative v0.1 source unchanged.

Repository decision ID: `d12-singer-2017-date-enrichment`.

## Evidence path

The accepted date comes from the bounded research record:

- `migration-candidates/autism-neurodiversity/singer-edition-enrichment-research.json`
- decision candidate `nd-singer-2017-date-enrichment`
- proposed value `2017-09-05`
- research status `corroborated_catalogue_candidate`

The accepted evidence routes bind the date to the revised 2017 print identity, including ISBN `9780648154709`:

- Wellcome Collection: `https://wellcomecollection.org/works/ywrdd8ff`
- Google Books: `https://books.google.com/books/about/NeuroDiversity.html?id=Ox_7uQEACAAJ`
- Open Library: `https://openlibrary.org/books/OL30658778M/NeuroDiversity`

## Candidate effect

Only `neurodiversity-source-singer-2017-revised-print` gains an accepted future-candidate full date:

- `publication_date`: `2017-09-05`
- `full_schema_date_status`: `accepted_by_d12_for_future_non_authoritative_candidate`
- `date_decision_ref`: `d12-singer-2017-date-enrichment`

The candidate remains non-authoritative.

## Preserved boundaries

D12 does **not**:

- accept `2016-07-03` for the Kindle candidate;
- accept any Singer Evidence Contribution binding;
- copy Claim support across editions;
- mutate `objects/concepts/neurodiversity.json`;
- create authoritative Evidence;
- alter schema or validator policy;
- resolve uncertainty shape, D6 structural confidence, or the Neurodiversity → ADHD dependency;
- authorise authoritative v0.2 replacement, publication, or deployment.

The authoritative Neurodiversity v0.1 blob remains `5a38bc4250079412dd3f4da1d598dfcab984ca66`.

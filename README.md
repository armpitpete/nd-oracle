# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current repository state

The authoritative corpus currently contains:

- 10 reviewed v0.1 Concept objects covering Neurodiversity, Autism, ADHD, Executive function, Sensory processing, Dyslexia, Developmental co-ordination disorder, Tourette syndrome, Learning disability and Developmental language disorder;
- 15 reviewed v0.2 Resource objects spanning tools/apps, games, workplace support, organisations and books.

Resource inclusion is **not endorsement**. A Resource may be listed without an efficacy claim when its identity, access route, intended use, limitations, cost/access notes and conflicts are useful. Any efficacy, safety or other serious testable proposition requires its own governed Claim and Evidence route.

Every v0.2 Resource requires at least one typed access locator. HTTPS URLs are enforced for web locators so a public catalogue entry cannot become an unreachable name with no governed route to the thing being described.

## Production state

Production remains the accepted v0.5 reading release until a later exact-main deployment is separately authorised and verified. v0.5 publishes the reviewed ten-topic reading layer at `https://ndoracle.org`; see `docs/PRODUCTION_STATE_v0.5.md` for the frozen deployment identity and evidence.

The ecosystem v0.6 work is a candidate until its protected schema/publication and deployment gates are passed. It activates reviewed Resources rather than exposing empty Tools/Games/Community placeholders.

## Repository map

```text
objects/concepts/                  Reviewed concept objects
objects/resources/                 Reviewed resource objects
schema/object-v0.1.json            v0.1 concept contract
schema/object-v0.2.json            v0.2 six-object dispatcher
schema/types/                      v0.2 object-type contracts
site/                              Static public site source
scripts/validate.py                Schema, governance-route, and graph checks
scripts/build_site.py              Reading-first static site generator
docs/ECOSYSTEM_PUBLICATION_v0.6.md Ecosystem publication contract
GOVERNANCE.md                      Decision rights and protected changes
CONTRIBUTING.md                    Contribution and provenance rules
```

## Validate

```shell
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests
```

## Public interface boundary

The site remains intentionally semantic, reading-first, privacy-first, and functional without JavaScript. The ecosystem layer adds static discovery routes and resource pages without accounts, profiling, recommendation scoring, personalised ranking, analytics or an AI answer surface.

A later Oracle query/discovery layer may route ordinary questions across the knowledge graph, but generated answers must never become the source of truth or bypass governed evidence and uncertainty.

## Licensing status

No reuse licence has yet been selected. Copyright remains with contributors until an owner explicitly adopts a licence. This is recorded as an open governance decision rather than guessed.

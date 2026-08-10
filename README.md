# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. A future website will be a reading-first window onto it.

## Governing rules

1. Never make the next person rediscover an uncertainty already identified.
2. Every serious question leaves the knowledge system better than it found it.
3. No conclusion without its route back to evidence and uncertainty.
4. Measure success by epistemic work saved, not text produced.

## Current state

Version `0.1.0` contains schema v0.1 and five root concept objects:

- Neurodiversity
- Autism
- ADHD
- Executive function
- Sensory processing

The seed objects are orientation material, not diagnosis or medical advice. They deliberately retain disagreements, scope limits, and open questions.

## Repository map

```text
objects/concepts/       Root knowledge objects
schema/object-v0.1.json Machine-readable contract
schema/schema-v0.1.md   Human-readable model and decisions
scripts/validate.py     Schema, governance-route, and graph checks
GOVERNANCE.md           Decision rights and protected changes
CONTRIBUTING.md         Contribution and provenance rules
```

## Validate

```shell
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests
```

## Design direction (deferred)

The eventual UI should be soft and reading-first. Text sizes should be roughly uniform; hierarchy should come mainly from weight, italics, spacing, and indentation. No web application is included in v0.1.

## Licensing status

No reuse licence has yet been selected. Copyright remains with contributors until an owner explicitly adopts a licence. This is recorded as an open governance decision rather than guessed.

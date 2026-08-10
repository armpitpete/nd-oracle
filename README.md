# ND Oracle

ND Oracle is a provenance-first knowledge commons for the full neurodiversity ecosystem. It connects concepts and claims to evidence, lived experience, uncertainty, and practical resources—including tools, games, apps, books and media, services, organisations, communities, and accommodations.

This repository is the system of record. The public site at `https://ndoracle.org` is a reading-first window onto validated repository content; it does not replace the repository as the knowledge authority.

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

Site Shell v0.1 is accepted in production at `https://ndoracle.org`. The accepted release was deployed from exact commit `5fa502bf717adb0e4c900eda7594bcbc4f74a6f0`; repository and production identities must still be re-resolved independently before any later deployment claim. See `docs/PRODUCTION_STATE_v0.1.md` for the recorded release, artifact, route, security-header, DNS, and redirect evidence.

## Repository map

```text
objects/concepts/                  Root knowledge objects
schema/object-v0.1.json            Machine-readable contract
schema/schema-v0.1.md              Human-readable model and decisions
site/                              Static public site source
scripts/validate.py                Schema, governance-route, and graph checks
docs/SITE_SHELL_v0.1.md            Public shell contract
docs/PRODUCTION_STATE_v0.1.md      Accepted production identity and evidence
GOVERNANCE.md                      Decision rights and protected changes
CONTRIBUTING.md                    Contribution and provenance rules
```

## Validate

```shell
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests
```

## Public shell and future interface work

Site Shell v0.1 is intentionally small, semantic, reading-first, and functional without JavaScript. Search, graph exploration, AI answers, accounts, comments, analytics, and other application features remain separate later lanes and are not implied by the existence of the public shell.

## Licensing status

No reuse licence has yet been selected. Copyright remains with contributors until an owner explicitly adopts a licence. This is recorded as an open governance decision rather than guessed.
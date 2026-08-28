# Resource locator addendum to schema v0.2

Status: candidate protected schema change.

The v0.2 Resource object now requires a non-empty `locators` array using the existing typed locator definition in `common-v0.2.json`.

## Reason

A Resource represents something a person may use or access. The original Resource contract could describe a resource without preserving any governed route to reach or identify it. That is insufficient for a public tools, games, books, services or organisation catalogue.

## Contract

- `locators` is required.
- At least one locator is required.
- Locator entries use the existing common v0.2 locator vocabulary.
- A locator of type `url` must use HTTPS.
- Multiple locators must be unique.
- A locator establishes identity/access only. It does not establish efficacy, safety, endorsement or evidential quality.

This is a bounded extension of the existing Resource object. It does not change the Claim, Evidence, Question, Perspective or Experience models and does not migrate the ten existing v0.1 Concept objects.

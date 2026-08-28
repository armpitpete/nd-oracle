# Governance

## Purpose

Governance protects provenance, recorded uncertainty, contributor dignity, privacy and the usefulness of the commons over time.

## Non-negotiable invariants

- A conclusion or serious claim must name supporting evidence and at least one uncertainty, limitation or explicit `none_identified` route where the schema permits it.
- Removing uncertainty requires a rationale and evidence; it must not erase the historical route by which it was resolved.
- Lived experience is first-class evidence about experience, access, acceptability and practical effects. It must not be silently generalised into a universal clinical claim.
- Clinical, community, historical, commercial and practical sources must be labelled by source kind. Authority in one domain does not imply authority in another.
- Conflicts and minority perspectives remain visible when they materially affect interpretation or action.
- Objects use stable IDs. Renaming a display label must not break links.
- Resource inclusion is not endorsement. A resource listing does not become an efficacy, safety, legal or diagnostic recommendation merely by appearing in the commons.
- Generated or algorithmically routed output is never the source of truth. Discovery may point into governed material; it may not bypass provenance and uncertainty.

## Roles

- **Contributors** propose changes and supply provenance.
- **Maintainers** review structure, evidence routes, safety, scope and compatibility.
- **Project owner** approves protected changes until a broader governing body is constituted.

## Protected changes

The following require an explicit owner decision and a reviewed pull request:

- schema-version changes or migrations;
- licensing changes;
- removal of a source, uncertainty, perspective or material limitation;
- changes to these governing rules;
- merge to protected `main` when an exact-head gate is being used;
- publication or production deployment;
- representation as clinical guidance;
- collection of personal or sensitive data;
- changes to moderation, editorial authority or community representation.

## Review gates

Every material change must pass, as applicable:

1. automated schema and graph validation;
2. provenance review for new or changed claims;
3. uncertainty-preservation review;
4. scope, privacy and safety review;
5. backwards-compatibility/public-journey review;
6. owner review for protected changes.

## Current remote enforcement

GitHub reports `main` as protected and requires status check `validate` for everyone. The repository currently exposes no repository rulesets, so this document does not claim ruleset enforcement. The production environment is separately configured to accept protected branches only, and the manual deployment workflow verifies that configuration before accepting an exact current-main SHA.

The GitHub integration cannot read every branch-protection detail from the dedicated protection endpoint, so this record deliberately states only enforcement observable from branch metadata and the deployment environment. If those controls change, governance documentation must be updated rather than assuming the historical state persists.

## Release evidence

A production claim requires a route back to:

- the accepted release commit;
- successful pre-deployment validation;
- the deterministic artifact digest;
- the deployment workflow/run identity;
- the accepted production project/domain identity;
- fresh network-backed verification of the canonical domain.

Successful upload alone is not production acceptance.

## Epistemic-work accounting

Success is not object count or word count. Evaluation should track reusable work: governed questions answered or bounded, evidence routes reused, recorded uncertainties reused, duplicate investigations avoided, provenance paths completed and real user journeys made shorter. v1.0 adds a frozen ordinary-language discovery benchmark so route existence is not mistaken for useful discovery.

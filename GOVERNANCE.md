# Governance

## Purpose

Governance protects provenance, recorded uncertainty, contributor dignity, and the usefulness of the commons over time.

## Non-negotiable invariants

- A conclusion or claim must name at least one supporting source and at least one uncertainty, limitation, or explicit `none_identified` record.
- Removing uncertainty requires a rationale and evidence; it must not erase the historical route by which it was resolved.
- Lived experience is first-class evidence about experience, access, acceptability, and practical effects. It must not be silently generalized into a universal clinical claim.
- Clinical, community, historical, commercial, and practical sources must be labelled by source kind. Authority in one domain does not imply authority in another.
- Conflicts and minority perspectives remain visible when they materially affect interpretation or action.
- Objects must use stable IDs. Renaming a display label must not break links.

## Roles

- **Contributors** propose changes and supply provenance.
- **Maintainers** review structure, evidence routes, safety, and scope.
- **Project owner** alone approves protected changes until a broader governing body is constituted.

## Protected changes

The following require an explicit owner decision and a reviewed pull request:

- schema-version changes or migrations;
- licensing changes;
- removal of a source, uncertainty, perspective, or material limitation;
- changes to these governing rules;
- publication, deployment, or representation as clinical guidance;
- collection of personal or sensitive data;
- changes to moderation, editorial authority, or community representation.

## Review gates

Every change must pass:

1. automated schema and graph validation;
2. provenance review for new or changed claims;
3. uncertainty-preservation review;
4. scope and safety review;
5. owner review for protected changes.

Use protected branches and required pull-request reviews when a remote is configured. Direct pushes to the default branch should then be disabled.

## Epistemic-work accounting

Success is not object count or word count. Future evaluation should track reusable work such as sourced claims retrieved, recorded uncertainties reused, duplicate investigations avoided, provenance paths completed, and questions that improve existing objects. The metric design remains intentionally open in v0.1.

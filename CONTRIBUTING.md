# Contributing

Contributions should make future inquiry cheaper, safer, or clearer.

## Before proposing a change

1. Search stable IDs, aliases, claims, Questions and recorded uncertainties before adding anything.
2. Extend an existing object when it already owns the question.
3. Separate observations, interpretations, recommendations and unresolved questions.
4. Prefer accessible sources and persistent identifiers. Record access date, source kind and the exact proposition the source supports.
5. Do not include private health information, confidential material or copyrighted text beyond short quotations permitted by law.

## Claim standard

Each claim needs a stable claim ID, a calibrated confidence label, an evidence route and at least one explicit uncertainty/limitation route. Confidence describes support for the exact wording and scope; it is not a percentage and does not rank a person's experience.

Use identity-first or person-first language according to the people and communities described. Preserve materially contested terminology in perspectives/uncertainty rather than declaring a universal preference.

Resource inclusion is not endorsement. A listing may identify and describe a resource without making an efficacy, safety, legal or diagnostic claim. Serious testable propositions require governed claim/evidence/uncertainty routes.

## Safety

Do not present the commons as diagnosis, treatment, crisis support or a substitute for qualified professional judgement. Practical-resource entries must expose audience/scope, possible drawbacks, accessibility, costs/access constraints, commercial relationships and the basis for any claims.

## Change process

- Create a focused branch from current `main` and open a pull request.
- Keep the repository's stable object IDs and backwards-compatible public routes unless an explicit reviewed contract changes them.
- Run:

```shell
python scripts/validate.py
python scripts/check_content_freshness.py --fail-overdue
python -m unittest discover -s tests
```

- Explain changed objects, evidence, uncertainties, exclusions and any public-route effects.
- Never resolve an uncertainty by deleting its history. Preserve the route by which it was reduced or resolved.
- Sign off each contribution commit with `Signed-off-by: Your Name <email@example.com>`.

## Contributor rights and licensing certification

ND Oracle uses a split licensing model. See `LICENSE`, `CONTENT_LICENSE.md` and `DCO.md`.

### Software/code contributions

Software/code contributions are submitted under the Apache License 2.0 (`Apache-2.0`). By adding a `Signed-off-by:` line, the contributor certifies the Developer Certificate of Origin 1.1 in `DCO.md`, including that they have the right to submit the contribution under the indicated open-source licence.

Software/code includes implementation material such as source code, schemas, tests, workflows, scripts, templates, styles and other implementation assets unless a specific notice says otherwise.

### Original knowledge/content contributions

Original ND Oracle knowledge content, prose/documentation and applicable database rights are submitted under the Creative Commons Attribution 4.0 International licence (`CC BY 4.0`) described in `CONTENT_LICENSE.md`.

For any contribution containing original content, the contributor's `Signed-off-by:` also certifies that, to the best of their knowledge:

1. they created the contribution or otherwise have the necessary rights or permission to submit it;
2. they agree that the rights they are entitled to license in their original contribution may be distributed under CC BY 4.0;
3. any third-party quotation, excerpt, image, dataset, trade mark or other externally controlled material is clearly identified with its source and applicable licence, permission or legal basis;
4. they have not silently represented third-party material as ND Oracle-owned or CC BY-licensed content; and
5. they understand that the contribution and sign-off form part of the public project record.

If you cannot make the applicable certification, do not submit the material until the rights position has been resolved.

### Third-party material

Public availability is not permission to relicense. Do not copy substantial third-party text, images or datasets merely because they can be accessed online. Keep quotations bounded, record provenance, and identify the applicable rights basis. A file-specific or item-specific licence notice overrides the repository default for the material it identifies.

### No CLA

ND Oracle does not require a Contributor Licence Agreement at this stage. Contributors retain copyright in their original contributions while granting the rights provided by the applicable project licence.

## Remote enforcement and protected boundaries

`main` is a protected branch. The GitHub branch metadata reports required status check `validate` for everyone. Current repository rulesets are empty; classic branch protection is the active branch-level mechanism visible to this integration. The production environment independently accepts protected branches only.

Merges and production deployments remain protected project-owner boundaries. Production deployment uses the manual `Deploy Cloudflare Pages (manual)` workflow, requires an exact 40-character SHA that is still current `main`, rebuilds and revalidates the artifact, and rechecks the accepted Cloudflare project before Direct Upload.

Schema changes, licensing changes, removal of material evidence/uncertainty, collection of personal or sensitive data, moderation/editorial-authority changes and representation as clinical guidance require an explicit reviewed protected decision under `GOVERNANCE.md`.

## Licensing baseline

The adopted licensing baseline is:

- Apache-2.0 for software/code;
- CC BY 4.0 for original ND Oracle knowledge content, prose/documentation and applicable database rights;
- no relicensing of third-party material unless separately identified as reusable;
- DCO 1.1 sign-off for software plus the content-rights certification above;
- no CLA at this stage.

Future changes to this licensing baseline remain protected decisions under `GOVERNANCE.md`.


## Evidence contributions

Evidence is accepted for an exact governed Claim, not as citation volume. State the source identity, the exact proposition it bears on, its source kind, relevant population/context, methodology and material limitations. Normalized v0.2 Evidence Contributions must use a bounded contribution role and remain reciprocal with the target Claim.

Official status, publication prestige, source count and community popularity are not automatic quality scores. First-party commercial material may establish current first-party product/service facts when conflicts are explicit, but it does not independently establish efficacy, safety, accessibility quality or personal fit. Lived experience can establish the experience as reported without becoming prevalence, mechanism or diagnosis.

Do not add dataset, book, commercial or other source classes merely to satisfy a diversity quota. Add them when a real Claim needs them. Contradictory, falsifying and inconclusive evidence must remain visible rather than being removed to simplify a conclusion. Material Evidence-role, confidence or interpretation changes require a provenance-bearing explanation.

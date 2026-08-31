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
- Sign off commits with `Signed-off-by:` when contributing material for which you hold the necessary rights.

## Remote enforcement and protected boundaries

`main` is a protected branch. The GitHub branch metadata reports required status check `validate` for everyone. Current repository rulesets are empty; classic branch protection is the active branch-level mechanism visible to this integration. The production environment independently accepts protected branches only.

Merges and production deployments remain protected project-owner boundaries. Production deployment uses the manual `Deploy Cloudflare Pages (manual)` workflow, requires an exact 40-character SHA that is still current `main`, rebuilds and revalidates the artifact, and rechecks the accepted Cloudflare project before Direct Upload.

Schema changes, licensing changes, removal of material evidence/uncertainty, collection of personal or sensitive data, moderation/editorial-authority changes and representation as clinical guidance require an explicit reviewed protected decision under `GOVERNANCE.md`.

## Licensing

No reuse licence has yet been adopted. Do not assume that public availability grants reuse rights. Issue #105 tracks the protected code/content licensing decision.

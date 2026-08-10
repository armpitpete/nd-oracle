# Contributing

Contributions should make future inquiry cheaper, safer, or clearer.

## Before proposing a change

1. Search stable IDs, aliases, claims, and uncertainties before adding anything.
2. Extend an existing object when it already owns the question.
3. Separate observations, interpretations, recommendations, and unresolved questions.
4. Prefer accessible sources and persistent identifiers. Record access date and source kind.
5. Do not include private health information, confidential material, or copyrighted text beyond short quotations permitted by law.

## Claim standard

Each claim needs a stable claim ID, a calibrated confidence label, source IDs, and uncertainty IDs. Confidence describes support for this wording and scope; it is not a percentage and does not rank a person's experience.

Use identity-first or person-first language according to the people and communities described. Preserve contested terminology in `perspectives` rather than declaring a universal preference.

## Safety

Do not present the commons as diagnosis, treatment, crisis support, or a substitute for a qualified professional. Practical-resource entries must record who they may help, possible drawbacks, accessibility, commercial relationships, and the basis for claims.

## Change process

- Create a focused branch and pull request.
- Run `python scripts/validate.py`.
- Explain changed objects, new evidence, uncertainties added or resolved, and exclusions.
- Never resolve an uncertainty by deleting it. Add a resolution record in a future schema version or preserve the rationale in history.
- Sign off commits with `Signed-off-by:` to certify that you have the right to contribute the material.

Until remote governance is configured, local commits are provisional and publication is a protected owner gate.

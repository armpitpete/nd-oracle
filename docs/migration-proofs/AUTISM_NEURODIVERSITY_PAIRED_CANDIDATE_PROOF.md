# Autism + Neurodiversity paired migration candidate proof

Status: **non-authoritative paired candidate prepared; D6 confidence policy and D7 Autism WHO Perspective framing accepted; Neurodiversity enrichment research prepared; remaining owner decisions and dependencies unresolved**.

Prepared on 2026-08-11 against protected repository `main`:

`1b7e4261c70bd6a86346d34a1f08abf90c3deece`

D6 structural-confidence policy accepted on 2026-08-11 against protected repository `main`:

`653938871190b454696df12abcc5bc0260ce19fd`

D7 Autism WHO Perspective framing accepted on 2026-08-11 against protected repository `main`:

`cae42eaf485f91f2920dcc1a15176bc335286719`

Neurodiversity enrichment research prepared on 2026-08-11 against protected repository `main`:

`26ee009309efd624c9da661bd168522a3089932c`

Source anchors:

- `objects/concepts/autism.json` — blob `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`;
- `objects/concepts/neurodiversity.json` — blob `5a38bc4250079412dd3f4da1d598dfcab984ca66`.

## Authorised scope

D5 authorises preparation of a **paired non-authoritative Autism + Neurodiversity migration candidate** so their reciprocal legacy structural relationship is not broken merely to migrate one side first.

D6 governs the missing structural confidence field: do not infer or default it, and do not use `not_applicable` merely to satisfy validation. The field stays absent until evidence-backed enrichment or a separately accepted structural-confidence schema policy supplies a non-fabricating representation.

D7 accepts the three WHO-backed framing fields for the future non-authoritative Autism Perspective candidate only.

The Neurodiversity enrichment pass is research/proposal construction only. It does not accept the new source-reconciliation or Perspective decisions it identifies.

These decisions and research steps do not authorise:

- mutation of either authoritative v0.1 object;
- authoritative v0.2 replacement;
- weakening the v0.2 reciprocity validator;
- invention or defaulting of relation confidence;
- use of `not_applicable` as a schema-completion shortcut;
- automatic expansion of the candidate to ADHD;
- acceptance of Neurodiversity Perspective framing or source-reconciliation choices;
- publication or deployment.

## Candidate prepared

The committed structural slice is:

`migration-candidates/autism-neurodiversity/structural-candidate.json`

It preserves the exact reciprocal legacy pair:

- Autism `narrower_than -> neurodiversity`, legacy note: `Autism is commonly situated within neurodiversity discourse.`;
- Neurodiversity `broader_than -> autism`, legacy note: `Autism is commonly discussed within the neurodiversity ecosystem.`

The candidate records the v0.2 typed targets but deliberately does **not** supply a `confidence` value. Both v0.1 relations lack confidence. D6 confirms that absence must remain visible rather than being filled by inference, default, or `not_applicable`.

D7 removes the Autism WHO Perspective framing owner-decision blocker from this candidate record. The Neurodiversity enrichment research is linked through:

`migration-candidates/autism-neurodiversity/neurodiversity-enrichment-research.json`

Therefore the candidate proves the pairing direction and reciprocal structural shape, but it does **not** claim full v0.2 Concept validity.

## Multi-source migration tooling defect found and repaired

The migration manifest schema already permits more than one source object, but `scripts/validate_migration.py` previously flattened every source inventory into a single `set[str]`.

That was unsafe for a real paired package because two source objects can legitimately contain identical preservation-unit strings. The migration-only repair is backward-compatible: multi-source preservation entries are scoped by source object, while existing single-source packages remain valid.

No authoritative knowledge schema or authoritative graph validator was changed.

## Reproducible package builder

`scripts/build_paired_migration_candidate.py` still generates the formal migration-contract package from the exact source blobs, existing accepted Autism decisions, and explicit unresolved Neurodiversity requirements.

The new Neurodiversity research record is intentionally separate from the formal generated enrichment ledger because its source-reconciliation and Perspective choices have not yet been accepted. This prevents research proposals from masquerading as completed migration state.

The package remains `owner_decision_pending` and `authoritative_replacement: false`.

## Disconfirming finding: the D5 pair is not full structural closure

Neurodiversity v0.1 also contains:

`broader_than -> adhd`

That does **not** invalidate D5's rule that Autism and Neurodiversity must be paired to preserve their reciprocal relationship. It does mean the pair is not the complete structural closure of a future authoritative Neurodiversity v0.2 object.

The ADHD edge remains a separate unresolved structural dependency.

## Neurodiversity enrichment research result

Detailed proof:

`docs/migration-proofs/NEURODIVERSITY_ENRICHMENT_RESEARCH.md`

Machine-readable record:

`migration-candidates/autism-neurodiversity/neurodiversity-enrichment-research.json`

Key findings:

- Singer title and authorship are verified, but source date/edition identity is unresolved because the legacy citation points to a 2016 Kindle edition while the Wellcome locator describes a 2017 print edition.
- Singer is `compatible` support for both Neurodiversity claims, with explicit limitations; the source is not promoted to stronger support merely because its narrative is historically central.
- Botha title, 2024-03-12 date and six-author authorship are verified.
- The legacy Botha DOI conflicts with the cited publication record. The verified paper DOI is `10.1177/13623613241237871`; correction is proposed for a future non-authoritative v0.2 Evidence object only.
- Botha is `supportive` for the collective-origins claim, but its letter format and selected archival scope remain explicit limitations.
- Both Neurodiversity Perspective framing sets now have evidence-backed proposals, but neither is accepted by the research pass.

## Remaining blockers

### 1. Reciprocal structural relation confidence — policy resolved, representation unresolved

D6 forbids inferred/defaulted confidence. No confidence value is present.

### 2. Autism uncertainty shape

D3 preserves Autism's list-valued uncertainty reduction conditions as legacy-unmapped. No flattening is authorised.

### 3. Autism WHO Perspective framing — accepted by D7

No longer an owner-decision blocker.

### 4. Neurodiversity Singer edition/date reconciliation

The future v0.2 Evidence record cannot safely combine 2016 Kindle and 2017 print metadata. An owner decision is required before a schema-valid full date is supplied.

### 5. Neurodiversity Botha citation correction

The DOI correction is evidence-backed but still requires explicit owner acceptance before it becomes the future v0.2 citation value.

### 6. Neurodiversity uncertainty mapping

Both legacy Neurodiversity uncertainties retain list-valued `what_would_reduce_it` arrays. No flattening or schema change is authorised.

### 7. Neurodiversity Perspective framing

Evidence-backed `held_by.scope`, `reasoning`, and `scope` proposals are prepared for both legacy Perspectives. Both remain owner decisions.

### 8. Neurodiversity ↔ ADHD structural dependency

The legacy `broader_than -> adhd` edge remains unresolved and outside the D5 candidate.

## Result

The knowledge state has advanced from “Neurodiversity enrichment unknown” to **explicit evidence-backed proposals plus named unresolved decisions**.

No source conflict has been hidden, no Perspective framing has been silently accepted, no uncertainty array has been flattened, and no missing structural confidence has been invented.

The D5 structural dependency remains open because an exact paired v0.2 candidate must eventually validate reciprocal structure without weakening the reciprocity rule and without fabricating required relation semantics.

No authoritative object, site, deployment, DNS, analytics configuration, or production state is changed by this proof.

# Autism + Neurodiversity paired migration candidate proof

Status: **non-authoritative paired candidate prepared; D6 confidence policy accepted; enrichment and other owner decisions remain pending**.

Prepared on 2026-08-11 against protected repository `main`:

`1b7e4261c70bd6a86346d34a1f08abf90c3deece`

D6 structural-confidence policy accepted on 2026-08-11 against protected repository `main`:

`653938871190b454696df12abcc5bc0260ce19fd`

Source anchors:

- `objects/concepts/autism.json` — blob `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`;
- `objects/concepts/neurodiversity.json` — blob `5a38bc4250079412dd3f4da1d598dfcab984ca66`.

## Authorised scope

D5 authorises preparation of a **paired non-authoritative Autism + Neurodiversity migration candidate** so their reciprocal legacy structural relationship is not broken merely to migrate one side first.

D6 governs the missing structural confidence field: do not infer or default it, and do not use `not_applicable` merely to satisfy validation. The field stays absent until evidence-backed enrichment or a separately accepted structural-confidence schema policy supplies a non-fabricating representation.

These decisions do not authorise:

- mutation of either authoritative v0.1 object;
- authoritative v0.2 replacement;
- weakening the v0.2 reciprocity validator;
- invention or defaulting of relation confidence;
- use of `not_applicable` as a schema-completion shortcut;
- automatic expansion of the candidate to ADHD;
- silent acceptance of pending Perspective or other semantic choices.

## Candidate prepared

The committed structural slice is:

`migration-candidates/autism-neurodiversity/structural-candidate.json`

It preserves the exact reciprocal legacy pair:

- Autism `narrower_than -> neurodiversity`, legacy note: `Autism is commonly situated within neurodiversity discourse.`;
- Neurodiversity `broader_than -> autism`, legacy note: `Autism is commonly discussed within the neurodiversity ecosystem.`

The candidate records the v0.2 typed targets but deliberately does **not** supply a `confidence` value. Both v0.1 relations lack confidence. D6 confirms that absence must remain visible rather than being filled by inference, default, or `not_applicable`.

Therefore the candidate proves the pairing direction and reciprocal structural shape, but it does **not** claim full v0.2 Concept validity.

## Multi-source migration tooling defect found and repaired

The migration manifest schema already permits more than one source object, but `scripts/validate_migration.py` previously flattened every source inventory into a single `set[str]`.

That is unsafe for a real paired package because two source objects can legitimately contain identical preservation-unit strings, especially shared provenance values. Such units were falsely classified as inventory collisions.

The repair is migration-only and backward-compatible:

- `preservation-ledger-v0.2.json` permits optional `source_object_id`;
- single-source packages may continue omitting it;
- multi-source packages must identify the source object for every preservation entry;
- uniqueness and coverage are checked on `(source_object_id, unit)` rather than `unit` alone.

No authoritative knowledge schema or authoritative graph validator is changed.

## Reproducible package builder

`scripts/build_paired_migration_candidate.py` generates a full contract package from the two exact source blobs and the accepted Autism migration records.

The generated package contains:

- a two-source manifest;
- source-scoped preservation ledger entries for every deterministic v0.1 preservation unit;
- the existing Autism enrichment record plus explicit pending Neurodiversity enrichment requirements;
- structural dependency records;
- the committed structural candidate;
- the accepted Autism owner-decision record and an appended paired-candidate decision log.

After D6, the generated structural-confidence record is a **pending enrichment/schema-policy requirement**, not a pending invitation to choose a convenient confidence value. It proposes no value and explicitly records that `not_applicable` is not authorised as a validation shortcut.

The package remains `owner_decision_pending` and `authoritative_replacement: false` because other owner decisions remain unresolved.

## Disconfirming finding: the D5 pair is not full structural closure

Neurodiversity v0.1 also contains:

`broader_than -> adhd`

That does **not** invalidate D5's rule that Autism and Neurodiversity must be paired to preserve their reciprocal relationship. It does mean the pair is not the complete structural closure of a future authoritative Neurodiversity v0.2 object.

The ADHD edge is therefore retained as a separate unresolved structural dependency rather than being silently dropped or used to expand D5 authorisation.

## Remaining blockers

### 1. Reciprocal structural relation confidence — policy resolved, representation unresolved

The current v0.2 relation schema requires `confidence`. Neither v0.1 reciprocal relation supplies it.

D6 resolves the migration policy:

- do not infer confidence;
- do not default confidence;
- do not use `not_applicable` merely to make the candidate validate;
- keep the field absent until an evidence-backed confidence value or a separately accepted structural-confidence schema policy is reviewed.

So this is no longer an unresolved default-selection decision. It remains an explicit enrichment/schema-policy requirement.

### 2. Autism uncertainty shape

D3 deliberately retains Autism's list-valued `what_would_reduce_it` arrays as legacy-unmapped. The current v0.2 Claim schema still requires embedded Uncertainty records with a single `reopening_or_reduction_condition` string.

The candidate does not flatten those lists merely to pass schema validation.

### 3. Autism Perspective framing

The proposed `held_by.scope`, `reasoning`, and Perspective `scope` fields remain unaccepted.

### 4. Neurodiversity Evidence enrichment

The Neurodiversity sources have not yet had the evidence-backed v0.2 enrichment pass required for title/date/authorship and claim-specific Evidence Contributions.

The builder records those requirements as pending instead of guessing them.

### 5. Neurodiversity uncertainty mapping

Neurodiversity also uses list-valued legacy reduction conditions. No object-specific owner decision has yet authorised their v0.2 representation.

### 6. Neurodiversity Perspective framing

Both legacy Neurodiversity Perspectives lack v0.2 holder scope, reasoning, and Perspective scope.

### 7. Neurodiversity ↔ ADHD structural dependency

The legacy `broader_than -> adhd` edge remains unresolved and outside this D5 candidate.

## Result

The paired candidate has been prepared **without fabricating the missing semantics that would make it look complete**.

D6 further locks that principle for structural confidence: schema validity is not evidence. A confidence enum cannot be inserted simply because the schema requires one.

The D5 structural dependency remains open because its accepted closure condition is stronger than merely writing both IDs into one candidate: an exact paired v0.2 candidate must eventually validate reciprocal structure without weakening the reciprocity rule and without fabricating required relation semantics.

No authoritative object, site, deployment, DNS, analytics configuration, or production state is changed by this proof.

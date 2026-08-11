# Autism + Neurodiversity paired migration candidate proof

Status: **non-authoritative paired candidate prepared; owner decisions and enrichment remain pending**.

Prepared on 2026-08-11 against protected repository `main`:

`1b7e4261c70bd6a86346d34a1f08abf90c3deece`

Source anchors:

- `objects/concepts/autism.json` — blob `b2d3809ecfcdb1d81c793a2401f0533a4b17ea98`;
- `objects/concepts/neurodiversity.json` — blob `5a38bc4250079412dd3f4da1d598dfcab984ca66`.

## Authorised scope

D5 authorises preparation of a **paired non-authoritative Autism + Neurodiversity migration candidate** so their reciprocal legacy structural relationship is not broken merely to migrate one side first.

It does not authorise:

- mutation of either authoritative v0.1 object;
- authoritative v0.2 replacement;
- weakening the v0.2 reciprocity validator;
- invention of missing relation confidence;
- automatic expansion of the candidate to ADHD;
- silent acceptance of pending Perspective or other semantic choices.

## Candidate prepared

The committed structural slice is:

`migration-candidates/autism-neurodiversity/structural-candidate.json`

It preserves the exact reciprocal legacy pair:

- Autism `narrower_than -> neurodiversity`, legacy note: `Autism is commonly situated within neurodiversity discourse.`;
- Neurodiversity `broader_than -> autism`, legacy note: `Autism is commonly discussed within the neurodiversity ecosystem.`

The candidate records the v0.2 typed targets but deliberately does **not** supply a `confidence` value. Both v0.1 relations lack confidence and D5 did not authorise manufacturing one.

Therefore the candidate proves the pairing direction and reciprocal structural shape, but it does **not** claim full v0.2 Concept validity.

## Multi-source migration tooling defect found and repaired

The migration manifest schema already permits more than one source object, but `scripts/validate_migration.py` previously flattened every source inventory into a single `set[str]`.

That is unsafe for a real paired package because two source objects can legitimately contain identical preservation-unit strings, especially shared provenance values. Such units were falsely classified as inventory collisions.

The repair is migration-only and backward-compatible:

- `preservation-ledger-v0.2.json` now permits optional `source_object_id`;
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

The package remains `owner_decision_pending` and `authoritative_replacement: false`.

## Disconfirming finding: the D5 pair is not full structural closure

Neurodiversity v0.1 also contains:

`broader_than -> adhd`

That does **not** invalidate D5's rule that Autism and Neurodiversity must be paired to preserve their reciprocal relationship. It does mean the pair is not the complete structural closure of a future authoritative Neurodiversity v0.2 object.

The ADHD edge is therefore retained as a separate unresolved structural dependency rather than being silently dropped or used to expand D5 authorisation.

## Remaining blockers

### 1. Reciprocal structural relation confidence

The current v0.2 relation schema requires `confidence`. Neither v0.1 reciprocal relation supplies it.

A later owner decision must determine whether structural relations use an accepted confidence rule or whether the schema should distinguish structural assertions differently. Until then no confidence value is inserted.

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

The paired candidate has now been prepared **without fabricating the missing semantics that would make it look complete**.

The D5 structural dependency remains open because the accepted closure condition is stronger than merely writing both IDs into one candidate: an exact paired v0.2 candidate must eventually validate reciprocal structure without weakening the reciprocity rule.

No authoritative object, site, deployment, DNS, analytics configuration, or production state is changed by this proof.

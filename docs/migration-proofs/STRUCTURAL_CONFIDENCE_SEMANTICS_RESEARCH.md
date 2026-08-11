# Structural confidence / semantics research

Status: non-authoritative research candidate

Prepared against protected `main`:

`31c244ecff0a52c53c38f60cc57815587e9b0856`

## Question

Can the remaining D6 structural-confidence blocker be closed by assigning evidence-backed confidence to the current Autism/Neurodiversity structural pair, or by introducing a generic confidence representation for migrated relations with no legacy confidence?

## Result

**Not yet. Relation semantics need review first.**

The current paired candidate represents:

- Autism `narrower_than` Neurodiversity; and
- Neurodiversity `broader_than` Autism.

The same legacy pattern exists for ADHD and Neurodiversity outside the D5 pair.

But the authoritative v0.1 notes are weaker. They say Autism and ADHD are commonly situated within neurodiversity discourse/ecosystem. They do not explicitly assert a taxonomic class/subclass relation.

Current terminology evidence also distinguishes **neurodiversity** from **neurodivergence**:

- the National Autistic Society describes neurodiversity as diversity across all human brains and autism as a form of neurodivergence;
- the NHS describes autism as often called a type of neurodivergence;
- the NHS England independent ADHD Taskforce describes neurodiversity as population-level diversity and discusses ADHD as neurodivergence.

This makes the exact current `narrower_than` / `broader_than` proposition materially stronger than both the legacy note and the reviewed terminology evidence.

## D6 remains binding

D6 already forbids:

- inferred/defaulted confidence;
- `not_applicable` used merely to satisfy validation.

It permits either:

- evidence-backed confidence enrichment; or
- a separately accepted structural-confidence schema policy.

Neither route should be used to bypass a semantic problem in the relation itself.

## Options tested

### Assign confidence to the current edge

**Not ready.**

The reviewed evidence supports association with neurodiversity discourse and autism/ADHD as forms of neurodivergence, but does not cleanly establish the exact current taxonomy edge to the Neurodiversity concept.

### Use `not_applicable`

**Rejected.**

D6 forbids it as a validation shortcut, and it would leave the taxonomy question unresolved.

### Infer/default a confidence value

**Rejected.**

This is directly forbidden by D6.

### Add `unassessed` to the confidence enum

**Not recommended before semantic review.**

That mixes assessment state into an epistemic-confidence vocabulary and would make it easier to carry a questionable structural edge indefinitely.

### Make confidence silently optional

**Rejected.**

That weakens fail-closed validation and cannot distinguish deliberate preservation of absent legacy confidence from accidental omission.

### Explicit confidence-assessment state

A future schema policy could plausibly use an explicit state such as:

```yaml
confidence_assessment_state: assessed | legacy_not_recorded
```

with a conditional rule:

- `assessed` requires a confidence value;
- `legacy_not_recorded` prohibits one.

This would preserve absence without fabrication. It is **not** proposed for acceptance yet because the current relation mapping should be confirmed first.

## Recommended direction

1. Do not assign confidence to the current Autism/Neurodiversity or ADHD/Neurodiversity taxonomy edges.
2. Do not add a schema shortcut merely to make those edges validate.
3. Preserve D5 and D6 as historical accepted decisions.
4. Reopen the migration **relation semantics** for this structural family.
5. Only after the relation type/target is reviewed should the project decide whether any surviving structural relation still needs a generic `legacy_not_recorded` confidence representation.

## Boundary

This research does **not**:

- rewrite D5 or D6;
- change the v0.2 schema or validator;
- assign a confidence value;
- choose a replacement relation type;
- choose a replacement target such as a new Neurodivergence concept;
- expand the D5 pair to ADHD;
- mutate any authoritative v0.1 object;
- authorise authoritative v0.2 replacement, publication, or deployment.

## Owner decision candidate

`nd-structural-semantics-before-confidence`

Recommended acceptance:

> Accept only the research conclusion that the current neurodiversity structural family should receive neither confidence enrichment nor a schema shortcut until relation semantics are separately reviewed. Preserve D5 and D6 historically; do not yet choose a replacement relation type, target, confidence value, schema representation, authoritative migration, or ADHD expansion.

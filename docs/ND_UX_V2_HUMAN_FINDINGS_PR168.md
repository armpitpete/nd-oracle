# ND-UX-V2 human findings — PR #168

Date: 2026-09-22
Candidate before repair: `2bf24ca0b7009df2b493ce702e7b8c3090ebcf46`
Status: targeted human finding recorded; full fixed-journey human gate remains OPEN

## Privacy

The repository stores only the minimum usability evidence needed for disposition. Participant identity and diagnostic/medical details are not stored here.

## HF-001 — Resources first-choice overload

**Observed behaviour / feedback**

The Resources surface presented too many competing ways to begin: strategy choices, life-area choices and resource-family choices. The human feedback requested direct recognisable choices such as books, games and conditions instead of repeated “do this / do that” decisions.

**Severity:** MAJOR

**Disposition:** REPAIR

**Smallest justified repair**

- make the first Resources choice a single category set;
- use five direct recognition labels: **Books**, **Games**, **Conditions & topics**, **Apps & tools**, **Support & organisations**;
- remove the competing first-screen strategy grid and life-area grid from the Resources page;
- preserve Find, Needs, Places, Types and A–Z as existing governed routes rather than deleting capability;
- add regression coverage so the overloaded composition cannot silently return.

**Visual-evidence repair**

The prior A Kind of Spark viewport proved the route rendered but did not show the supplied cover within the screenshot. Exact-head visual evidence must use a taller A Kind of Spark capture so the authorised cover itself is directly reviewable.


## HF-002 — Home requires concrete categories before internal taxonomy

**Observed behaviour / feedback**

The current navigation model still makes abstract/internal labels too prominent. Human feedback states that choices should be recognisable things such as **books, games and conditions**, and freezes this acceptance criterion:

> **A new visitor can tell that ND Oracle contains things such as conditions, books, games and apps, and can reach them without first learning what “Resources”, “Topics”, “Needs” or similar internal categories mean.**

**Severity:** MAJOR

**Disposition:** CONTRACT REPAIR APPLIED / IMPLEMENTATION PENDING PHASE 2

**Smallest justified Phase 1 repair**

- freeze the concrete visitor-category contract;
- separate primary categories from secondary utilities and internal taxonomy;
- bind direct reachability and human acceptance criteria;
- do not modify governed knowledge or production state in this phase.

Phase 1 does not claim that the Home implementation already satisfies HF-002. That implementation and its visual/human evidence belong to Phase 2.

## Human gate

This finding is genuine human evidence for the Resources surface. It does **not** by itself satisfy all ten fixed journeys in `docs/ND_UX_V2_USER_TEST_PROTOCOL.md`.

The final human gate therefore remains OPEN until the fixed journeys are run on the repaired exact-head candidate and their results are recorded and dispositioned. Do not infer or fabricate PASS from automated checks or screenshots.

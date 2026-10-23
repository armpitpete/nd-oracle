# V2 navigation + responsive integration candidate

Date: 2026-10-24
Status: **Candidate only — NOT ACCEPTED, NOT DEPLOYED**

## Lineage

- Base: PR #168 exact head `be3f84ce19d7c73f42a337bd799a4a0b6e9cf062`.
- Responsive source: PR #170 exact head `7062ec39fd96a08aa6b4c1d7cc18ce2d95fb41cc`.
- Merged semantics on a new branch; PR #168 and #170 preserved unchanged.
- The new branch is **not** a new accepted human-test freeze.

## Applied changes

1. Preserve PR #168 six-route visitor navigation, glossary, real-human findings and governed content.
2. Port PR #170 question secondary composition; enforce 90% viewport shell (up to 1600px); keep 82ch prose measure.
3. Preserve PR #168 late information, glossary and evidence page layout repairs; remove their conflicting 90rem outer-shell cap.
4. Preserve PR #168 simplified screenshot workflow; add PR #170 CDP responsive verifier as a separate blocking step.
5. Carry over PR #170 responsive unit tests, verifier, design specification and pinned dependency.

## Required acceptance evidence

- Newly generated exact-head CI and visual-evidence workflow results.
- Inspect eight responsive sizes, including the six primary first-hop routes and Question pages.
- Prove the 450 canonical route contract, rights gating, privacy, no-drift and six Home choices are preserved.
- Real participant validation on a frozen accepted exact SHA; inherited findings are evidence of defects, **not final human PASS**.
- Separate explicit protected merge and deployment decisions; no production mutation from this integration candidate.

## Outstanding blockers

- A test-run report and actual human/assistive technology acceptance at this new exact SHA.
- Protected main merge, protected deployment, canonical-domain live verification, and production/public-state reconciliation.

This is an engineering integration attempt, not evidence that the complete 1,000-task backlog has been executed.

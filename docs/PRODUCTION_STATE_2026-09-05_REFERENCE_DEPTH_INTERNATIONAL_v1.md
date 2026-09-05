# ND Oracle production state — 2026-09-05 — Reference depth + international v1

Accepted production state recorded on 2026-09-05 after exact-SHA deployment and fresh network-backed verification of the reference-depth and international v1 programme merged through PR #151.

This document records an already completed production deployment and verification. It does not itself authorize or perform a deployment. It becomes the human-readable evidence record referenced by `contracts/current-production.json` after this reconciliation passes its protected merge gate.

The preceding `docs/PRODUCTION_STATE_2026-09-04_NHS_BULLETIN_PROMOTION_v1.md` remains immutable historical evidence for the immediately preceding accepted production.

## Identity

- Canonical site: `https://ndoracle.org`
- Public-site builder contract: `v1.2`
- Promotion PR: #151 — `ND Oracle: complete reference-depth and international v1 backlog`
- Exact tested PR head: `9e96093228537a7c2d0f9045243631818e09defa`
- Exact-head validation run: `33978403228` (#373), job `101339086679`
- Accepted production source SHA: `8e60f264adfda2822312a05e835bc352ef263225`
- Accepted production source tree: `e287f1a6003724b10ea130ef40d846b9837981de`
- Deployment workflow: `Deploy Cloudflare Pages (manual)`
- Successful deployment run: `33987304421` (run #26)
- Exact-main guard job: `101363155938`
- Direct Upload job: `101363174757`
- Generated artifact SHA-256: `d598e73f1403d11dc668bed209bd0c54218c587d65b3bd51e25215e26c5c2543`
- Cloudflare deployment identity: `https://9784eb1f.nd-oracle.pages.dev`
- Cloudflare project: `nd-oracle`
- Production branch: `main`
- Canonical custom-domain set verified by deployment workflow: `ndoracle.org`
- Fresh live-production verification run: `33987460412` (run #20)
- Fresh live-production verification job: `101363565001`

The exact tested PR #151 head `9e96093228537a7c2d0f9045243631818e09defa` and merged production source `8e60f264adfda2822312a05e835bc352ef263225` share tree `e287f1a6003724b10ea130ef40d846b9837981de`. The protected merge therefore changed commit identity but not the tested filesystem tree.

## Deployment proof

Deployment run #26 was dispatched on `main` with exact release SHA `8e60f264adfda2822312a05e835bc352ef263225`. Its protected guard independently confirmed that the requested SHA was still current protected `main` and that the pre-existing `cloudflare-pages-production` environment remained restricted to protected branches.

The Direct Upload job checked out that exact SHA, verified a clean checkout, compiled the Python sources, validated all **366 authoritative objects**, and ran the complete **467-test regression suite** before building the static artifact.

The workflow then enforced the static/no-runtime boundary, recorded artifact SHA-256 `d598e73f1403d11dc668bed209bd0c54218c587d65b3bd51e25215e26c5c2543`, verified pinned Wrangler `4.114.0`, and verified the pre-existing Direct Upload Cloudflare Pages project `nd-oracle` with:

- production branch `main`;
- project subdomain `nd-oracle.pages.dev`;
- exact custom-domain set `ndoracle.org`;
- no Git-integration source.

Immediately before upload it rechecked that current GitHub `main` still equalled the authorized source SHA and that the Cloudflare project identity/configuration still satisfied the protected release contract.

Cloudflare completed the production deployment as `https://9784eb1f.nd-oracle.pages.dev`.

No Pages project creation, DNS mutation, custom-domain mutation, secret mutation, or other production-configuration change was requested or performed by this release workflow.

## Corpus at acceptance

The accepted production corpus contains exactly **366 governed objects**:

- 20 reviewed Concept objects;
- 168 reviewed Resource objects;
- 175 reviewed Question objects;
- 3 normalized v0.2 Evidence objects.

Relative to the immediately preceding production state, this release adds exactly **41 governed objects**:

- 21 reviewed Resources;
- 20 bounded Questions;
- no new Concept;
- no new Evidence object.

The programme completes bounded reference-depth work for:

1. Books & media;
2. Sleep;
3. Food & eating;
4. Mobility & travel;
5. Republic-of-Ireland post-v1 readiness decisions;
6. Australia Assessment & diagnosis orientation;
7. Canada Assessment & diagnosis orientation with explicit Ontario implementation;
8. the three-package international architecture review.

The Evidence registry remains at 60 governed source records across 49 governed Claims. **All 49 Claims remain evidence-covered.**

Exact-head acceptance run #373 proved:

- 49/49 governed Claims covered;
- 0 Evidence gaps;
- 60 governed Evidence source records checked, 0 overdue;
- 366 governed objects checked, 0 overdue;
- 467/467 regression tests PASS;
- Question contract 175 PASS.

Resource inclusion remains **not endorsement**. Question routes retain the boundary **Relevant to inspect, not recommended**.

## Completed section boundaries

### Books & media

The release broadens governed media beyond the earlier autism/ADHD-heavy book seed with:

- dyspraxia/DCD lived experience;
- Tourette lived experience;
- cross-neurodivergent introductory material;
- podcast;
- documentary;
- accessible-format inspection.

Memoir, podcast, documentary and fiction remain perspective/representation formats rather than clinical authority.

### Sleep

The release adds Scotland, Wales and Northern Ireland insomnia navigation plus a child-sleep route while preserving:

- no diagnosis;
- no sleep-disorder inference from symptoms;
- no melatonin or medicine start/stop/increase/decrease authority;
- explicit local/specialist-pathway uncertainty where national first-party routing is not uniform.

### Food & eating

The release adds Scotland/Wales ARFID navigation, child restricted-eating orientation and dysphagia/swallowing safety separation.

Sensory eating, ARFID, pica and dysphagia remain distinct. A standalone national pica route and a fictional UK-wide dietetic referral route were deliberately not created where evidence did not support them.

### Mobility & travel

The release separates:

- Great Britain bus/coach accessibility requirements;
- Great Britain rail Passenger Assist;
- Northern Ireland Translink assistance;
- concessionary entitlement;
- practical sensory/cognitive/disruption planning.

Operator information is descriptive and does not become an ND Oracle provider-quality score.

## Republic of Ireland follow-on

The post-v1 Ireland readiness review is complete as an evidence decision:

- child ADHD was rechecked and remains deliberately deferred because current first-party evidence does not justify a strong uniform national access route;
- regional/Health Region implementation variation remains explicit;
- private-provider ranking remains prohibited;
- broader condition-specific Ireland routes were not duplicated without a useful maintainable pathway;
- no speculative second Ireland domain was activated.

This is a completed readiness decision, not an empty-country placeholder.

## International architecture

The accepted international proof now has three real non-UK packages:

1. Republic of Ireland;
2. Australia;
3. Canada.

Australia demonstrates national orientation plus material state/territory implementation variation.

Canada demonstrates federal orientation plus explicitly narrower provincial implementation through Ontario.

The three-package architecture review concludes:

- retain additive jurisdiction sidecars;
- do not migrate the core object geography schema;
- do not begin mass-country expansion;
- do not add a translation subsystem merely because international packages now exist;
- future country work remains one bounded evidence-driven package at a time.

## Public contract

Fresh live-production verification run `33987460412` revalidated all 366 governed objects and the complete 467-test regression suite, then passed every one of the **450 canonical routes** at `https://ndoracle.org`.

The live verifier concluded:

`Verified 450 canonical routes plus v1.0 governed discovery/evidence and frozen compatibility contracts at https://ndoracle.org.`

It also confirmed:

- Concept contract: 20;
- Question contract: 175;
- Resource contract: 168;
- frozen public compatibility: PASS;
- governed discovery/evidence contract: PASS.

## Discovery state

The accepted discovery scope is additive:

- frozen base scoped routes: 41;
- UK Assessment extension scoped routes: 29;
- Republic of Ireland Assessment extension scoped routes: 12;
- Australia Assessment extension scoped routes: 4;
- Canada/Ontario Assessment extension scoped routes: 4;
- total governed scoped routes: **90**.

The frozen `discovery/routing-policy-v1.1.json` and ranking weights remain unchanged. Australia and Canada are loaded through explicit additive sidecars with exact scope provenance and hostile cross-jurisdiction benchmarks.

## Temporary dispatch provenance

The connected GitHub integration does not expose direct `workflow_dispatch` writes. Two disposable helper branches were used only to dispatch the already-existing protected/read-only workflows. Neither entered `main`.

### Deployment dispatcher

- Branch: `release/temp-dispatch-reference-depth-international-2026-09-05-production`
- Temporary commit: `ce2641e6bbf773e48c0df1a765d9a6e7105c6503`
- Helper run: `33987298526`
- Helper job: `101363137703`

The helper verified that current `main` exactly equalled the authorized release SHA, then dispatched the existing protected `deploy-cloudflare-pages.yml` workflow on `main` with that exact SHA.

### Live-verification dispatcher

- Branch: `release/temp-dispatch-reference-depth-international-2026-09-05-live-verify`
- Temporary commit: `d718da3b6963f2a3b5135c9c3c6f42015c7ecbf6`
- Helper run: `33987453882`
- Helper job: `101363546504`

The helper verified successful deployment run `33987304421` against the exact authorized main SHA, then dispatched the existing read-only `live-production-verify.yml` workflow on `main`.

After both helper runs completed, both disposable branches were reset to exact production source SHA `8e60f264adfda2822312a05e835bc352ef263225`. No temporary helper workflow remains on their branch tips and no helper workflow entered protected `main`.

## Historical production evidence

`docs/PRODUCTION_STATE_2026-09-04_NHS_BULLETIN_PROMOTION_v1.md` remains the immutable record of the immediately preceding accepted production from source SHA `94d1ab0d8df5699b1316e64d70c28fe11b25b7cf`, with 325 governed objects, 409 canonical routes and artifact SHA-256 `2899f9c214f6eecded51c8cf64aa356fd76674b32bdd1b801dfa2ae5521aedbb`.

The Ireland, UK Reference Baseline and earlier production-state documents also remain immutable historical evidence.

## Acceptance statement

The deployed public production is the artifact generated from exact source SHA `8e60f264adfda2822312a05e835bc352ef263225`, tree `e287f1a6003724b10ea130ef40d846b9837981de`, with SHA-256 `d598e73f1403d11dc668bed209bd0c54218c587d65b3bd51e25215e26c5c2543`, deployed as `https://9784eb1f.nd-oracle.pages.dev` and served canonically at `https://ndoracle.org` with all **450 canonical routes freshly verified**.

**REFERENCE DEPTH + INTERNATIONAL v1 — PRODUCTION FINAL PASS** is warranted once this production-state reconciliation itself passes exact-head CI, hostile review and protected merge.

# ND-UX-V2 Navigation Phase 2 Implementation Receipt v1

Date: 2026-09-29
PR: #168
Authority: presentation/navigation only
Status: **REVISED AFTER HF-003 — SIX-CHOICE REPAIR CANDIDATE**

## Why the Phase 2 surface changed

The original Phase 2 implementation exposed nine concrete Home choices. Human review then identified a remaining first-choice overload problem: the visitor still had to process too many equally prominent routes and multiple classification groups.

That finding is recorded as **HF-003** in `docs/ND_UX_V2_HUMAN_FINDINGS_PR168.md`.

The repair is intentionally narrower than a wider ND Oracle redesign.

## Revised Home

Home now exposes exactly six primary choices:

1. **ADHD, autism & other neurodivergence**
2. **Help with everyday life**
3. **Books, films & media**
4. **Games & apps**
5. **Find support**
6. **Ask a question**

Search remains a separate escape route and does not count as a seventh category.

The old separate Home groups — Browse things, Get help with life and Check evidence — are removed from the primary surface.

## Secondary exploration

A collapsed **More ways to explore** disclosure preserves:

- Areas of life;
- Browse A–Z;
- Browse by place;
- Questions;
- Topics;
- All resources.

The global header is reduced to site identity plus visible **Search** and a native **Menu** disclosure.

## First-hop routes

The repair reuses existing governed and canonical content.

Two presentation aliases are added because the six-choice model needs them:

- `/everyday-help/` — links to existing life-area hubs;
- `/games-apps/` — exposes existing game/app/tool Resources without creating new authority.

Existing routes remain available, including `/conditions/`, `/books/`, `/games/`, `/apps-tools/`, `/organisations/`, `/work-education/`, `/health-diagnosis/`, `/daily-living/` and `/start/`.

`/books-media/` and `/questions/` remain existing canonical routes and are used directly by the revised Home.

## Support route adjustment

The `/organisations/` presentation alias now uses the visitor label **Find support** and includes governed `organisation`, `community` and `service` Resources.

This is a presentation projection only. It does not reclassify or duplicate governed Resources.

## Wrong-choice recovery

Every primary journey retains:

- a route back to Home/main choices;
- Search;
- normal browser Back behaviour.

Human testing now includes deliberate wrong-first-route recovery.

## Authority preservation

The six Home choices are not a replacement content taxonomy.

No governed object, Claim, Evidence record, source record, canonical URL, ranking/discovery policy, jurisdiction authority or production deployment pointer is changed merely to fit the Home model.

New presentation aliases remain `noindex, follow` and outside the accepted canonical sitemap identity until a later protected production-state reconciliation explicitly changes that authority.

## Recognition imagery

Existing visual-rights rules remain unchanged:

> **Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource.**

The Home repair does not widen image-rights scope.

## Scope guard

This repair is limited to:

- Home;
- minimal header/Search;
- collapsed secondary exploration;
- necessary first-hop presentation aliases;
- navigation/usability/accessibility evidence.

Broader destination restructuring and the separate book/textbook typography research remain outside this tranche unless real testing demonstrates a blocking problem.

## Human gate

Implementation is not acceptance.

The exact candidate still requires:

- first-impression testing;
- primary-label comprehension;
- representative task journeys;
- wrong-choice recovery;
- assistive-technology spot-check;
- real ND participant evidence;
- YP safeguards if actual minors are included.

Repairs after testing are limited to demonstrated problems.

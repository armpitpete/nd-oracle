# ND-UX-V2 Navigation Phase 2 Implementation Receipt v1

Date: 2026-09-23
PR: #168
Authority: presentation/navigation only

## Implemented

The frozen Navigation Contract v1 is implemented as a visitor-facing layer over existing governed content.

Home exposes nine concrete choices: **Conditions**, **Books**, **Games**, **Apps & tools**, **Organisations & peer groups**, **Work & education**, **Health & diagnosis**, **Daily living**, and **Evidence & research**.

Search, A–Z, Browse everything and Not sure where to start? remain secondary.

Direct presentation aliases are created for `/conditions/`, `/books/`, `/apps-tools/`, `/organisations/`, `/work-education/`, `/health-diagnosis/`, `/daily-living/` and `/start/`. `/games/` and `/evidence/` already exist and remain canonical.

## Authority preservation

The new aliases do not create or copy governed knowledge. They project existing Concept, Question and Resource objects and link to their existing canonical detail routes.

No governed object, Claim, Evidence record, source record, ranking/discovery policy, jurisdiction authority or production deployment pointer is changed.

The accepted production identity still records 450 canonical routes. Therefore the new aliases deliberately carry `noindex, follow` and are excluded from the sitemap until a later protected production-state reconciliation explicitly authorises a route-count change. `/games/` remains canonical and indexable.

## Recognition imagery

Books, Games and Apps & tools listings render a locally controlled visual only when the existing Resource Visual registry says the visual is both materially helpful and cleared.

The Pan Macmillan-supplied *A Kind of Spark* cover continues to be served byte-for-byte. CSS controls displayed size; the JPEG is not rewritten.

## Human gate

Implementation is not human acceptance.

The exact candidate must still receive the unprompted first-impression test plus the ten fixed journeys in `docs/ND_UX_V2_USER_TEST_PROTOCOL.md`. Findings are repaired only where demonstrated.

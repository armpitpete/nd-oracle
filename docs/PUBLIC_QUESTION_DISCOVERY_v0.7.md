# Public question-led discovery v0.7

## Purpose

Publish the first governed Question reading layer without introducing a chatbot, personalised ranking or generated-answer authority.

The public model is:

`ordinary need -> governed Question -> relevant reviewed Concepts/Resources -> inspectable uncertainty and provenance`

## Public routes

- `/questions/`
- `/questions/task-starting-and-organisation/`
- `/questions/low-time-pressure-games/`
- `/questions/workplace-support-great-britain/`
- `/questions/autism-information-and-support/`
- `/questions/autism-anxiety-tools/`

The homepage surfaces these practical routes before the existing topic-orientation questions. The ten v0.6 topic question links remain available.

## Reading contract

Every public Question page must show:

1. the ordinary-language question;
2. why the question matters;
3. visible review date and resolution status;
4. the boundary **Relevant to inspect, not recommended**;
5. current bounded understanding;
6. linked governed Concepts and Resources;
7. evidence still needed;
8. recorded dissent;
9. reopening conditions;
10. provenance and review state.

A Question page must not turn a Resource listing into an efficacy, safety, clinical, legal or personalised-fit claim.

## Compatibility approach

The proven v0.6 site generator and live verifier are retained byte-for-byte as compatibility modules. v0.7 extends them with Question loading, routes, sitemap entries, homepage discovery and a specific production contract.

This keeps all v0.6 regression and live verification assertions active while adding six new canonical routes.

## Expected public identity

The candidate contains 42 canonical indexable routes:

- 36 inherited v0.6 routes;
- 1 Question index;
- 5 Question detail routes.

`/oracle/` remains the only compatibility `noindex` route.

## Non-goals

v0.7 does not add:

- free-text question submission;
- an AI/chat answer surface;
- accounts or query storage;
- analytics or profiling;
- recommendation scores;
- personalised ranking;
- new efficacy or safety claims;
- a new schema version.

## Production boundary

This document defines a candidate contract only. Production remains the accepted v0.6 deployment until the public v0.7 PR is merged, an exact-main deployment is separately authorised, and the 42-route live verifier passes.

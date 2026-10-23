# ND-UX-V2 Navigation Phase 1 Decision Record v1

Date: 2026-09-23  
Status: **ACCEPTED — CONTRACT FREEZE**  
PR: #168

## Problem

Human feedback showed that ND Oracle can expose too many competing ways to begin and can ask visitors to understand project terms such as Resources, Topics or Needs before they understand what the site actually contains.

HF-001 already repaired overload on the Resources surface. The broader Home-level requirement is now recorded as HF-002: concrete visitor-recognisable categories must become the primary navigation model.

## Decision

Freeze `docs/ND_UX_V2_NAVIGATION_CONTRACT_v1.md` and `contracts/navigation-v1.json`.

The visitor-facing model is concrete first: Conditions, Books, Games, Apps & tools, Organisations & peer groups, Work & education, Health & diagnosis, Daily living, Evidence & research.

Search, A–Z, Browse everything and Not sure where to start? remain secondary utilities. Resources, Topics, Needs and Questions may remain internal/specialist or compatibility routes but are not required vocabulary for ordinary navigation.

## Why this is bounded

No governed knowledge is rewritten. The decision changes presentation/navigation authority only and provides Phase 2 with an unambiguous mapping target.

## Rejected alternatives

- Keep Resources/Topics/Needs as equal first-level choices: rejected because it preserves the demonstrated interpretation burden.
- Replace them with vague labels such as Explore/Discover: rejected because the visitor still has to infer what lies behind them.
- Delete compatibility routes: rejected because the usability problem is prominence and prerequisite vocabulary, not the existence of those routes.
- Redesign the entire site during Phase 1: rejected because implementation belongs to Phase 2 and should be judged against a frozen contract.

## Acceptance evidence required later

Phase 2 must implement the target, run full regression and desktop+narrow evidence, then expose the exact candidate to real human testing. Automated evidence cannot substitute for that human gate.

# ND-UX-V2.4 functional baseline

Date: 2026-09-09
Repository baseline: `0065ab8000bbb0020aa221f084525116f436b373`

## Frozen behaviour

V2.4 is the functional and compositional baseline for the V2 Public Baseline candidate.

The following behaviour is protected unless explicitly reopened:

- Home starts with four ordinary-language routes and eight areas of life.
- Questions starts with three routes, then area-of-life grouping and progressive disclosure.
- Resources keeps the complete catalogue available but secondary.
- Topics begins with recognition routes, grouped browsing and a complete A–Z.
- unfamiliar terminology may expose bounded word-part learning aids;
- discovery/index pages use desktop width when overview benefits from it;
- long-form reading remains width-controlled;
- page headings are directional landmarks, not hero cards;
- repeated cards/rounded panels are not the default grammar;
- Find remains deterministic, local and non-authoritative;
- canonical content remains useful without JavaScript;
- no analytics, accounts, query storage, personalised ranking or AI answer authority;
- evidence, jurisdiction, privacy and non-endorsement boundaries remain unchanged;
- the shared stylesheet URL is content-versioned.

## V2.5 permitted change

V2.5 may simplify presentation further when evidence shows a repeated element adds scanning or working-memory cost. It may not change governed meaning or invent new authority.

The first accepted simplification is to remove the legacy “More question shortcuts” catalogue from Home. Questions, Topics, Find and A–Z already preserve those routes, so duplicating them on Home adds page length without adding capability.

## Regression rule

A V2.5 candidate must preserve all V2.4 functional guarantees above and prove any subtraction does not remove canonical reachability.

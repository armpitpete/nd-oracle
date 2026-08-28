# ND Oracle ecosystem publication contract v0.6

Status: candidate. Schema/publication and production deployment remain protected changes under `GOVERNANCE.md`.

## Purpose

v0.6 begins exposing the wider ND Oracle ecosystem instead of presenting the project as only a ten-topic concept reader.

The public surface adds reviewed Resources for:

- tools and apps;
- games;
- practical/workplace support;
- organisations and support routes;
- books and other useful material as reviewed entries become available.

The release deliberately does **not** add recommendation scores, personalised ranking, accounts, profiling, analytics, forms or an AI answer surface.

## Core distinction: catalogued is not endorsed

A Resource is publishable when its identity and access route are current and its descriptive record is useful. Publication does not imply that:

- the resource is effective;
- it is safe for every person or context;
- it is appropriate for a particular diagnosis;
- a first-party marketing claim has been independently verified;
- popularity is evidence;
- ND Oracle recommends purchasing or using it.

A Resource may therefore have an empty `claims` array. If ND Oracle makes a serious testable proposition about efficacy, safety, compatibility, cost, eligibility or another claim, that proposition must use the normal v0.2 Claim → Evidence → Uncertainty route.

## Resource access contract

A public Resource must have at least one typed `locators` entry.

- Web resources use an HTTPS `url` locator.
- Other supported locator types may be used when appropriate.
- A locator establishes identity/reachability only; it is not evidence of efficacy or endorsement.

This closes a gap in the original v0.2 Resource shape, which could describe a useful thing without providing a governed route to reach it.

## Public routes

The candidate activates:

- `/resources/` — all reviewed resources;
- `/tools/` — tools, apps and adjacent practical resources;
- `/games/` — games described by play characteristics and limitations;
- `/community/` — services, organisations and community/support routes;
- `/resources/<id>/` — individual resource inspection pages.

`/resources/` appears in primary navigation as **Explore**.

The legacy `/oracle/` route remains a quiet `noindex` compatibility page. No chatbot is published merely to satisfy the product name.

## Resource page contract

Every individual public Resource page exposes, before provenance is opened:

1. resource type/category;
2. last-reviewed date;
3. an explicit **Listed, not endorsed** boundary;
4. intended use;
5. audience/context;
6. access locator(s);
7. related ND topics where available;
8. limitations and possible poor fit;
9. cost/access notes;
10. ownership/conflicts;
11. evidence status.

A claimless Resource must explicitly say that the listing makes no efficacy or safety claim.

## Games contract

Games are not classified as therapy unless evidence later supports an exact bounded claim. They are catalogued by useful characteristics such as:

- time pressure;
- reading demand;
- multiplayer/social demand;
- combat or failure pressure;
- sensory load;
- open-ended versus directed structure;
- accessibility options.

Positive labels such as “calm”, “relaxing”, “ADHD-friendly” or “autism-friendly” are not treated as universal facts.

## Commercial and organisational conflicts

Commercial ownership is not a reason to exclude a Resource, and nonprofit status is not treated as proof of neutrality.

The record preserves relevant conflicts such as:

- a product vendor describing its own product;
- a publisher describing its own book;
- a charity promoting its own programmes or fundraising;
- an advocacy organisation advancing explicit policy positions.

These disclosures are context, not automatic disqualifiers.

## Freshness

Resources can become stale more quickly than stable concepts. A current access route and review date are therefore mandatory publication signals.

A resource known to have closed, been withdrawn or become unavailable must not remain presented as an active current option. Historical significance can be preserved separately when useful.

The initial curation explicitly rejected ADHD Foundation as an active support listing after its official closure notice was found; this is the intended stale-directory behaviour.

## Initial candidate inventory

The first candidate contains 15 reviewed Resources across multiple categories. They are a seed corpus designed to prove the resource model and public browsing contract, not a claim of ecosystem completeness.

The next expansion should prioritise diversity of useful resource types and evidence quality rather than raw catalogue size.

## Acceptance tests

Before publication, the exact candidate must prove that:

- all authoritative v0.1 and v0.2 objects validate together;
- every Resource has a current typed access locator;
- no resource page silently implies endorsement;
- active resource routes are indexable and appear in the sitemap;
- `/oracle/` remains non-indexed until it is a real capability;
- all internal links resolve;
- all generated pages retain semantic navigation, descriptions and keyboard-accessible structure;
- no JavaScript, forms, trackers or externally loaded assets are introduced;
- the existing restrictive security headers remain unchanged;
- the ten-topic evidence-reading contract remains intact.

## Protected boundaries

This candidate includes a v0.2 Resource schema change and expands the public publication surface. Both require the repository's normal reviewed protected gate before merge/publication.

Production deployment remains a separate exact-main protected action after merge and release verification.

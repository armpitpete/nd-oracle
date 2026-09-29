# ND-UX-V2 Navigation Contract v1

Date: 2026-09-29  
Status: **REVISED — PHASE 2 REPAIR CANDIDATE**  
Authority: presentation/navigation only  
PR: #168

## Release-blocking acceptance rule

> **A new visitor can tell that ND Oracle contains things such as conditions, books, games and apps, and can reach them without first learning what “Resources”, “Topics”, “Needs” or similar internal categories mean.**

This applies to desktop and narrow/mobile layouts. Automated checks are necessary but cannot satisfy the human usability gate.

## Home choice budget

The Home page presents **one first decision only**.

Rules:

- exactly **six primary Home routes**;
- Search is a separate escape route, not a seventh category card;
- only one primary classification system is visible at a time;
- one short description per primary route;
- deeper browsing is collapsed or visually subordinate by default;
- adding a new primary route requires replacing or merging an existing route rather than increasing the count.

### Six primary routes

| Visitor label | Purpose | Target |
| --- | --- | --- |
| **ADHD, autism & other neurodivergence** | Learn about ADHD, autism and other kinds of neurodivergence. | `/conditions/` |
| **Help with everyday life** | School, work, communication, sensory needs, relationships and daily tasks. | `/everyday-help/` |
| **Books, films & media** | Stories and information about neurodivergent lives. | `/books-media/` |
| **Games & apps** | Games, apps and digital tools. | `/games-apps/` |
| **Find support** | Groups, services, charities and other places to get help. | `/organisations/` |
| **Ask a question** | Not sure where to start? Begin with what is happening. | `/questions/` |

The labels are intentionally concrete. The visitor is not asked to classify their own search behaviour before reaching content.

## Search and secondary exploration

**Search ND Oracle** remains visible as an immediate escape route.

The Home page then provides one collapsed **More ways to explore** disclosure containing:

- Areas of life;
- Browse A–Z;
- Browse by place;
- Questions;
- Topics;
- All resources.

These routes preserve power-user and compatibility access without competing with the six first choices.

The header is intentionally minimal: site identity, **Search**, and a native **Menu** disclosure. The menu does not repeat the six Home choices as another visible decision wall.

## Navigation taxonomy is not content taxonomy

The six Home routes are a **presentation layer**, not a replacement for ND Oracle's governed content model.

A governed object may be reachable from more than one visitor route without:

- cloning the object;
- changing its canonical URL;
- changing its governed category merely to fit the Home page;
- changing Claims, Evidence, provenance, ranking or discovery authority.

For example, one tool may be reachable from practical-help and digital-tool routes while remaining one governed Resource.

## First-hop boundary

This tranche does **not** authorise a broad destination-page redesign.

The allowed implementation surface is:

- Home;
- minimal header/Search;
- collapsed secondary exploration;
- first-hop presentation routes required by the six Home choices;
- tests and evidence needed to validate those changes.

Existing destination architecture is preserved unless human testing demonstrates a specific blocker.

Unrelated destination-page, typography or taxonomy improvements are recorded for a later tranche rather than absorbed here.

## Wrong-choice recovery

> **No first choice becomes a dead end.**

Every primary journey must allow the visitor to:

- return to the six Home choices;
- reach Search;
- use normal browser Back;
- change to a related route without restarting the whole journey.

Human testing includes a deliberate wrong-first-route recovery task.

## Direct reachability

The target pattern is:

**Home → clear first-hop route → item or next concrete choice**

An avoidable chain such as:

**Home → internal taxonomy term → catalogue → type → item**

fails the contract when a clearer route can expose the same governed content safely.

## Internal terminology boundary

`Resources`, `Topics`, `Needs` and `Questions` may remain as compatibility, specialist or secondary routes. A new visitor must not need to understand those terms to make the first decision.

Vague replacements such as “Explore” or “Discover” must not become another primary classification layer.

## Visual hierarchy

The existing V2.5 rules remain authoritative:

- colour is paired with non-colour structure;
- retain the accepted readable base text size;
- use typographic weight and headings for importance;
- keep related information physically grouped;
- avoid whitespace that separates mutually dependent information;
- recognition imagery remains secondary to the route label and rights-gated.

> **Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource.**

The separate book/textbook typography research is useful design-system work, but it is **not a dependency or scope expansion for this Home repair**.

## Protected authority boundary

This repair must not modify:

- governed Resource, Concept, Question, Claim, Evidence or source content merely to fit the Home;
- schemas or discovery/ranking policy;
- provenance or jurisdiction authority;
- `contracts/current-production.json`;
- production deployment workflow, DNS, Cloudflare project/configuration, secrets or domains.

## Human acceptance

Before fixed journeys, ask:

> **Without clicking anything, what kinds of things do you think you can find on this website?**

For each primary heading, also ask:

> **What would you expect to find here?**

Do not explain the route first.

Record:

- first choice;
- hesitation;
- wrong route;
- backtracking;
- label confusion;
- whether the correct option was visible without prompting;
- whether Search was obvious;
- whether wrong-choice recovery succeeded;
- **Found it / Confusing / Couldn't find it**.

Representative tasks include ADHD, a book, an app, sensory help, local peer support, school/study, work, starting without the correct term, and deliberate wrong-route recovery.

A repeated pattern of confusion is evidence of a design defect. Aesthetic preference alone is not.

## Young-person testing safeguard

If actual minors are included:

- define the age range first;
- use appropriate parent/guardian consent and participant assent where required;
- do not request diagnosis proof or unnecessary health disclosure;
- minimise identifiable data;
- obtain explicit permission before recording;
- define storage/deletion rules;
- prepare an appropriate safeguarding/escalation procedure before testing.

The interface can be tested without collecting a young person's medical history.

## Mandatory acceptance

The repair cannot pass unless:

- exactly six primary Home routes are rendered;
- Search remains separate;
- secondary exploration is collapsed or clearly subordinate;
- primary labels are understandable without teaching ND Oracle taxonomy;
- no repeated severe misrouting remains around one label;
- representative tasks can be completed without facilitator guidance;
- wrong-choice recovery succeeds;
- no blocking accessibility defect remains;
- canonical routes and protected authority remain intact.

## Machine acceptance

Repository tests bind:

- the six-route choice budget;
- exact primary labels and routes;
- Search as a separate utility;
- collapsed secondary exploration;
- minimal Search + Menu header;
- first-hop route generation;
- wrong-choice recovery links;
- noindex treatment for new presentation aliases;
- preservation of the accepted canonical sitemap identity.

Machine checks do not satisfy the human gate.

## Exit

The Phase 2 repair candidate is ready for human acceptance only after exact-head CI, visual/accessibility review and no-drift validation pass.

After real ND/YP testing: record and disposition findings, repair only demonstrated problems, re-run exact-head evidence, then continue through the existing protected merge and deployment gates.

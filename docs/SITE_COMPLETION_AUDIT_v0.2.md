# ND Oracle whole-site completion audit v0.2

**Audit base:** protected `main` `18fa32c32be66447d1625d763bcb20c01c209220`  
**Lane:** public-site completion, not knowledge migration  
**Authority boundary:** no authoritative knowledge-object mutation

## Completion question

Does the current public product let a real visitor arrive, understand what the site is for, find the useful material that exists now, read it without learning the internal ontology first, inspect evidence when wanted, recover from mistakes, and avoid being sent into advertised empty features?

## Baseline finding

The Site Shell v0.1 foundation was technically sound but product-incomplete.

The largest user-journey defect was structural: the primary navigation and homepage advertised Tools, Games, Resources, Community and Oracle even though those destinations were intentionally inactive placeholders. Five of six primary navigation destinations therefore communicated future architecture rather than current usefulness.

Other completion gaps:

- the homepage led with product architecture instead of ordinary user questions;
- concept pages exposed evidence routing and internal identifiers too early in the reading flow;
- related concepts displayed machine-facing target IDs rather than human names;
- there was no dedicated explanation of how confidence, evidence and uncertainty should be read;
- there was no generated 404 recovery page;
- there was no sitemap or robots file for the useful public routes;
- the public copy still described itself as a “Site Shell”, reinforcing the sense of an unfinished product.

## Implemented repair

The v0.2 completion pass:

1. reduces primary navigation to active destinations only: Understand, How it works, About;
2. changes the homepage to ordinary-language entry questions and the five current topics;
3. keeps the complete corpus browsable in one scan under `/understand/`;
4. makes topic pages human-first: summary and scope first, then bounded claims;
5. moves claim-level evidence and uncertainty into native `<details>` progressive disclosure;
6. keeps uncertainties, perspectives, sources and provenance inspectable without forcing them into the first read;
7. renders related concepts by their human names;
8. adds `/how-it-works/` to explain confidence, evidence, uncertainty and the non-diagnostic boundary;
9. adds a useful non-indexed `404.html` recovery page;
10. generates `sitemap.xml` and `robots.txt` for the useful public routes;
11. retains the old future-feature routes only as non-indexed compatibility pages, absent from primary navigation and sitemap;
12. preserves the static no-JavaScript, no-form, no-account, no-tracking security/privacy baseline.

## Search decision

A separate search runtime is deliberately not required for this completion lane. With five topic pages, the homepage ordinary-language entry questions plus a complete `/understand/` listing make the corpus directly scannable without adding JavaScript or server-side search infrastructure.

Search becomes a genuine product requirement when the corpus grows enough that scanning the topic list stops being easier than searching it.

## Not part of this lane

The following are not blockers for the current public reading product:

- Singer 2016 bibliographic refinement;
- Autism/Neurodiversity v0.2 authoritative migration;
- Neurodiversity↔ADHD semantic disposition;
- accounts, comments or community submissions;
- games or tool implementations;
- a resource catalogue without actual resource content;
- AI-generated Oracle answers;
- analytics.

These may become separate useful features or knowledge lanes later. They should not be advertised as active product areas before they provide value.

## Verification contract

Acceptance requires:

- repository validation passes;
- complete regression suite passes;
- generated internal links resolve;
- all authoritative concept objects remain byte-for-byte untouched by the site build;
- no generated JavaScript, forms or inline style attributes;
- restrictive Cloudflare header policy remains unchanged;
- legacy placeholder routes are `noindex` and absent from the sitemap;
- exact-head pull-request CI passes before integration.

## Live-verification limitation

During this audit, the available browser/search environment could not resolve `ndoracle.org`, and the public site was not indexed by the web search service. The repository and generated-site contract can therefore be verified here, but a claim about the visual state of the currently deployed production pages requires a later reachable live check. This limitation must not be rewritten as a successful visual inspection.

## Completion definition

This lane is complete when the exact implementation passes the verification contract and is integrated. Production publication remains subject to the repository's existing exact-main deployment controls.

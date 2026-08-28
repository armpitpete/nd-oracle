# Ecosystem v0.6 acceptance checklist

Candidate acceptance requires all items below at one exact head.

- [ ] Repository validator accepts all authoritative Concept and Resource objects.
- [ ] Full unit-test discovery passes.
- [ ] Resource v0.2 schema requires at least one typed access locator.
- [ ] HTTPS is required for Resource URL locators.
- [ ] The 15 seed Resources validate with current review dates and explicit limitations/conflicts.
- [ ] Homepage exposes the populated ecosystem without displacing the ordinary-question route.
- [ ] `/resources/`, `/tools/`, `/games/` and `/community/` are active, canonical and indexable.
- [ ] Every Resource has a canonical `/resources/<id>/` page.
- [ ] Every Resource page says `Listed, not endorsed`.
- [ ] Claimless Resources explicitly state that no efficacy or safety claim is being made.
- [ ] Resource access links are present and external links do not load third-party assets into ND Oracle.
- [ ] The sitemap includes active ecosystem routes and Resource pages.
- [ ] `/oracle/` remains noindex until it is a real governed discovery capability.
- [ ] Topic evidence/uncertainty routes still render.
- [ ] Perspective evidence links use real citations instead of generic `source` labels.
- [ ] Existing security headers remain unchanged.
- [ ] Generated public pages contain no JavaScript, forms, trackers or inline styles.
- [ ] Exact-head CI passes.
- [ ] Protected schema/publication review is explicitly accepted before merge.
- [ ] Production deployment is separately authorised against exact protected `main` after merge.

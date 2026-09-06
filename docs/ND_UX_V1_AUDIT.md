# ND Oracle UX / Graphic Design Pass v1 — heuristic audit

Baseline: `185582736ea6df097c742c0f592feee1f21538c9`

Severity means user/product impact, not governance severity.

## Findings

### Major — page type is under-signalled

**Surface:** Question, Resource, Concept and Evidence detail pages.

**Observed problem:** Titles and content differ, but the global shell does not explicitly identify the semantic page type near the heading.

**User impact:** A first-time reader can arrive deep-linked and need to infer whether they are reading an explanation, governed Question, catalogue Resource or Evidence record.

**Direction:** Add a restrained non-colour-only page-kind label in the shared shell.

### Major — jurisdiction scope is not early enough

**Surface:** jurisdiction-dependent Questions and Resources.

**Observed problem:** Resource scope exists but can appear after intended-use/navigation material; governed Questions can state jurisdiction only inside prose.

**User impact:** A reader can begin acting on content before noticing that it applies to Great Britain, England, Northern Ireland, Republic of Ireland, Australia, Canada, Ontario or another bounded scope.

**Direction:** Surface a presentation-only scope panel before actionable content. Derive only from already governed wording; never infer eligibility.

### Major — Find is useful but visually secondary

**Surface:** global navigation and `/find/`.

**Observed problem:** Find is reachable from Home but is not a primary navigation destination. Input, action and results use largely browser-default presentation.

**User impact:** People who know their problem but not ND Oracle taxonomy have a weaker entry route than people who already know where to browse.

**Direction:** Put Find in primary navigation; group the labelled input and action; make local processing and “relevance is not recommendation” explicit.

### Medium — global product identity is too terse

**Surface:** header/footer.

**Observed problem:** The product name stands alone and the footer does not expose the Evidence catalogue directly.

**User impact:** New visitors have fewer immediate trust/orientation cues.

**Direction:** Add a short product-purpose descriptor and a direct Evidence footer route without adding a dense sitemap.

### Medium — semantic warnings share too much presentation

**Surface:** notices, scope, uncertainty and authority boundaries.

**Observed problem:** Different semantic roles often use the same neutral panel treatment.

**User impact:** Important scope/boundary distinctions require more reading effort.

**Direction:** Introduce restrained scope and boundary roles using text labels, border treatment and colour together. Meaning must not depend on colour.

### Medium — narrow interaction targets are not explicit enough

**Surface:** header navigation and Find controls.

**Observed problem:** links are accessible but do not have an explicit minimum target height; search controls have little project-level styling.

**User impact:** Touch use can be less deliberate on narrow screens.

**Direction:** Set minimum target heights, stack Find controls narrowly, and keep keyboard focus clearly visible.

### Medium — forced-colour behavior is implicit

**Surface:** semantic panels/cards.

**Observed problem:** default CSS should degrade reasonably, but there is no explicit forced-colours boundary treatment.

**User impact:** panel distinctions can weaken under user-forced colour schemes.

**Direction:** add explicit border fallbacks under `forced-colors: active`.

### Medium — browse views use reading-page width

**Surface:** Home and browse/landing pages.

**Observed problem:** the same 68ch column is used for reading and multi-entry navigation surfaces.

**User impact:** desktop browse surfaces can feel unnecessarily narrow and vertically long.

**Direction:** keep detail pages at reading width while allowing Home/browse layouts to use the wider shared shell.

### Polish — spacing and semantic radii are implicit

**Surface:** shared stylesheet.

**Observed problem:** values are coherent but not fully tokenised.

**User impact:** low immediate impact; higher maintenance drift risk.

**Direction:** name the spacing/radius roles used by the pass.

## Existing strengths preserved

- static, readable HTML;
- no analytics or tracking;
- strong visible focus;
- restrained palette;
- short reading measure on detail pages;
- skip navigation;
- no required JavaScript outside Find;
- “Listed, not endorsed” Resource boundary;
- “Relevant to inspect, not recommended” Question boundary;
- inspectable uncertainty/provenance;
- deterministic discovery;
- explicit 404 recovery routes.

## Audit conclusion

No framework replacement or knowledge-model change is justified. The appropriate pass is a bounded evolution of the existing shell, CSS tokens and generated semantic markup.

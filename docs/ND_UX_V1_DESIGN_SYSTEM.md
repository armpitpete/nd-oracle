# ND Oracle UX / Graphic Design Pass v1 — design system

## Design doctrine

1. Reading first.
2. Evidence before decoration.
3. Scope must be visible.
4. Uncertainty must remain visible.
5. Serious boundaries must not hide in footnotes.
6. Visual hierarchy must reduce cognitive effort.
7. Interfaces should be calm rather than dense.
8. No persuasive dark patterns.
9. No engagement optimisation.
10. Accessibility is part of the design, not post-processing.

## Typography

- Body/UI: system sans-serif stack.
- Headings/product name: system serif stack.
- Base size: approximately 17px desktop, 16.5px narrow.
- Detail reading measure: 68ch.
- Heading scale remains fluid with `clamp()`.

No external font dependency is introduced.

## Layout

- Detail pages remain reading-width.
- Home and browse surfaces may use the shared wider container.
- Shared shell maximum: 76rem.
- Primary narrow breakpoint remains 44rem.
- An additional 28rem rule prevents primary navigation overflow on very narrow screens.
- Long tables must be wrapped where used rather than forcing the page itself to overflow.

## Core token roles

### Surfaces

- `--background`: page ground.
- `--surface`: primary raised/contained reading surface.
- `--surface-soft` / `--surface-wash`: low-emphasis grouping.

### Text

- `--text`: primary content.
- `--text-soft`: metadata and secondary explanation.

### Semantic roles

- `--accent`: ordinary navigation/interactive emphasis.
- `--scope` / `--scope-soft`: jurisdiction and applicability scope.
- `--boundary` / `--boundary-soft`: limitations and authority boundaries.
- `--uncertainty`: unresolved/uncertainty surface.
- `--focus`: keyboard focus.

Semantic role is always reinforced by text, border shape, heading/label or position. Colour is never the sole carrier of meaning.

## Semantic visual vocabulary

| Role | Presentation contract |
| --- | --- |
| Question | Explicit “Question” page-kind label; governed-answer boundary remains visible. |
| Resource | Explicit “Resource” label; “Listed, not endorsed” remains visible. |
| Concept | Explicit “Concept” label; reading-first explanation precedes technical evidence detail. |
| Evidence | Explicit “Evidence” / “Evidence record” label; source-is-not-conclusion boundary remains. |
| Jurisdiction | Early “Scope before you act” panel and text badge when governed wording supports a scope. |
| Limitation | Boundary panel/notice plus explicit language; never icon-only. |
| Uncertainty | Existing uncertainty block and explanatory text. |
| Evidence status | Existing Evidence/Claim terminology plus page/type labeling. |
| Practical route | Ordinary links/lists; no recommendation score or engagement ranking. |
| Lived experience | Retains governed source-kind text; no special authority styling. |
| Clinical boundary | Explicit language in governed content; boundary treatment may strengthen visibility but not authority. |

## Page hierarchy

Where semantically applicable, core detail pages follow:

1. page type;
2. title;
3. purpose/summary;
4. review/status metadata;
5. jurisdiction/scope;
6. critical boundary/limitation;
7. primary content;
8. related useful routes;
9. Evidence/uncertainty/dissent;
10. provenance/review detail.

Not every page needs every layer. Missing governed data is not invented to fill the visual system.

## Interaction rules

- primary navigation exposes Find directly;
- active navigation uses `aria-current="page"`;
- controls retain visible `:focus-visible`;
- primary navigation and Find controls use explicit touch-friendly minimum heights;
- Find stays local/same-origin and retains deterministic governed routing;
- successful Find results show governed result type and route scope when a scope is already present in the static discovery index;
- no motion is required for comprehension;
- smooth scrolling is enabled only when reduced motion is not requested;
- forced-colour mode retains visible structural borders.

## Component rule

Presentation remains project-centralised:

- shared CSS in `site/styles.css`;
- shared generated shell/components in `scripts/build_site.py`;
- shared Find interaction in `scripts/discovery_browser.js`;
- Evidence projection in `scripts/evidence_public.py`.

No inline page-owned CSS or duplicated page-owned JavaScript is introduced.

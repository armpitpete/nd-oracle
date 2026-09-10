# ND-UX-V2.5 design system — quiet, obvious, directional

Date: 2026-09-10

## Governing target

**Quiet, obvious and controllable.**

V2.5 is not a new component library. It is a constraint system for composing ND Oracle pages with less interpretation and less visual repetition.

## Composition

- Page first, components second.
- No hero-and-card default grammar.
- A border, panel or background requires a functional reason.
- Prefer headings, bounded colour regions, rules and left-edge landmarks to repeated containers.
- Discovery surfaces use the desktop viewport; reading surfaces keep a controlled measure.
- Do not centre a phone-width page inside a large desktop viewport.
- The complete catalogue is an escape hatch, not the first view.
- Related information should remain within the same visual field where practical. Do not use generous whitespace in a way that pushes mutually dependent information onto separate screens.
- Use larger spacing to show a real change of subject; use tighter spacing within one conceptual group.

## Typography and importance

The current readable body size is retained. Text size is not the default repair for weak hierarchy.

Use weight to make importance scannable:

- **critical / decision information:** extra-bold treatment where justified;
- **important supporting information:** bold;
- **ordinary explanation:** regular weight;
- **metadata / provenance:** quieter treatment.

Weight never carries the whole meaning by itself. Headings, wording, position and semantic structure must continue to communicate the hierarchy.

Other typography rules remain:

- system sans-serif;
- left-aligned body text;
- short paragraphs;
- visible heading hierarchy;
- body text at the existing 16.5–17px baseline;
- restrained line length for reading;
- no long all-caps prose;
- underlines remain for real links.

## Colour and section boundaries

Colour marks **where a conceptual section starts and stops**, not merely category decoration. A page with several information types should not read as one continuous beige field.

- related material may share one calm surface family;
- a genuine change of subject should be visibly detectable through a different surface/edge treatment;
- warnings/limitations receive stronger visual priority than ordinary descriptive material;
- evidence/provenance remains visibly separate from practical decision information;
- every colour signal is paired with a heading, label, structural position or other non-colour cue;
- avoid a high-saturation rainbow effect: surfaces remain calm and low-intensity.

## Recognition visuals

For recognisable resources such as books, games, apps, films, physical products and other media, a useful product visual should normally be shown when ND Oracle has a lawful asset to publish.

The visual exists for **recognition** — helping somebody confirm “yes, that is the thing I meant” — not decoration or evidential authority.

Every rendered product visual requires:

- a local controlled asset rather than arbitrary hotlinking;
- recorded source/provenance;
- an explicit rights basis permitting ND Oracle publication;
- useful alt text;
- a text-complete no-image fallback;
- no implication that the image supports efficacy, safety, suitability or endorsement.

If rights are unknown or permission is required, the image stays absent. Missing imagery is not permission to scrape, hotlink, copy a cover/logo, or fabricate a lookalike.

The implementation contract is `docs/RESOURCE_VISUAL_ASSET_POLICY_v1.md` and `site/resource-visuals.json`.

## Language

Recognition precedes specialist vocabulary. Pages should let a user begin from what they notice or need to do.

Word-part aids are permitted only when linguistically defensible and must state that they are learning aids, not definitions or diagnostic rules.

## Interaction

- no autoplay;
- no surprise layout movement;
- no modal dependency;
- no account required;
- progressive disclosure uses native semantics where possible;
- keyboard, forced-colour and zoom use are first-class acceptance surfaces.

## Resource-detail acceptance

A resource-detail page should be visually scannable without changing the readable base text size.

- key warnings and decision boundaries must carry stronger typographic weight;
- scope, fit/context, access, exploration, limitations/cost and evidence/provenance must not blur into one continuous surface;
- section spacing must be compact enough that related information can be perceived together;
- books/games/apps/media/products should render a cleared recognition visual when one exists;
- an absent visual must never break the page or weaken the textual identity of the resource.

## Page acceptance questions

Every page must answer quickly:

1. Where am I?
2. What is this page for?
3. What can I do next?
4. What is authoritative here?
5. How do I return to the previous level?

A page fails if subtracting a repeated box, label or duplicated catalogue makes the task easier without losing information, or if related information is visually separated enough that a user has to hold one screen in memory while reading the next.

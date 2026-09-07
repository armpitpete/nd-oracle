# ND-UX-V2.4 design correction — composition, recognition and language learning

Date: 2026-09-07
Baseline main: `b165ebb88141a2ce4e0f92a1ca5b64537b6aae49`
Programme: ND-UX-V2
Slice: V2.4 — Topics discovery

## Why this correction exists

V2.1–V2.3 improved cognitive-load control, route coverage and visual wayfinding, but the accepted pages exposed a design-method failure:

- a narrow reading measure was applied to discovery pages that needed horizontal overview;
- repeated hero panels and cards became the default way to create hierarchy;
- desktop layouts often behaved like narrow layouts placed in the middle of a large viewport;
- local component consistency was allowed to outrank whole-page composition;
- cognitive accessibility was treated too often as separation into boxes rather than reduction of interpretation, scrolling and working-memory demand.

The result was calm and technically accessible, but more cognitively demanding than it looked.

V2.4 corrects the design method. It does not change canonical knowledge, evidence ownership or discovery authority.

## Superseding design rules

These rules supersede any earlier V2 recommendation that treats equally sized cards, bounded panels or a universal narrow column as the default.

### 1. Page first, components second

Design the whole page and its information landscape before selecting components.

A heading, list, rule or spacing change is preferred when it communicates the hierarchy without adding another object to parse.

### 2. Width follows task

- Long-form reading keeps a controlled line length.
- Search/forms use a focused but wider working area.
- Discovery, indexes and navigation use substantially more of the desktop viewport.
- Responsive design recomposes at different widths; it does not merely stack a phone-shaped layout.

### 3. Cards are exceptional

A card is justified only when an item is genuinely independent, self-contained and benefits from an enclosing boundary.

Cards are not the default for categories, navigation links, section introductions or visual hierarchy.

### 4. Directional anchors before containers

Use headings, whitespace, rules and strong left-edge colour markers to show:

- where a region begins;
- what belongs together;
- where the eye should return after distraction.

Colour is always paired with text, position or structure and never carries meaning alone.

### 5. Recognition before recall

A user should not need to know ND Oracle's taxonomy or specialist vocabulary before finding a useful route.

Prefer ordinary descriptions such as:

- “I cannot get started even when I want to”
- “Noise, light or touch becomes too much”
- “I do not notice hunger or thirst”

Then introduce the governed term.

### 6. Teach unfamiliar language rather than hiding it

Where useful and linguistically defensible, show:

> word → meaningful parts → what the parts suggest → whole plain-language meaning

Example:

> **Monotropism** → **mono** – **trop** – **ism**

Word-part explanations are learning and memory aids. They are not diagnostic rules, formal definitions or claims that modern meaning can be derived mechanically from historical roots.

### 7. Preserve spatial overview

Desktop layouts should expose relationships and neighbouring choices when doing so reduces scrolling and working-memory load.

A large unused desktop viewport is a design defect unless the content is deliberately being constrained for reading.

### 8. Accessibility includes cognitive composition

For users who may be stressed, literal, unfamiliar with specialist language, or unable to hold several navigation choices in working memory, every page should make clear:

1. where am I?
2. what is this page for?
3. what can I do next?

The interface must not require understanding the site's ontology before receiving help.

## Hostile design gate

Before a DES page can be accepted, inspect the full page at desktop and narrow widths and answer:

| Test | Failure |
| --- | --- |
| Whole-page composition | The page looks like stacked reusable components rather than one deliberate composition. |
| Viewport use | Desktop space is materially wasted without a reading reason. |
| Container necessity | A box/card/background exists without functional justification. |
| Information overview | The user must scroll excessively to understand the available routes. |
| Recognition | A user must know internal or specialist terminology to find the right route. |
| Subtraction | Removing borders, containers, labels or repeated explanation improves the page. |
| Direction | The page lacks stable visual landmarks for reorientation after distraction. |

Any failure returns the page to design rather than treating it as an engineering-only defect.

## V2.4 Topics acceptance

The Topics index must:

- provide ordinary-language recognition routes before the specialist catalogue;
- group all governed Topics without changing canonical ownership;
- preserve a complete A–Z route;
- use no hero card and no card grid;
- use a wide desktop composition;
- expose word-part learning where helpful;
- keep colour supplementary to text and structure;
- preserve keyboard, forced-colour, text-scaling and narrow-screen usability.

Representative topic detail pages must show the word-part pattern without weakening or replacing the governed definition and evidence route.

## Wider V2 implication

V2.4 also applies the corrected composition rules to Home, Find, Questions, Resources and Needs presentation. V2.3's information architecture remains accepted; its card-heavy visual implementation is not frozen as a design doctrine.

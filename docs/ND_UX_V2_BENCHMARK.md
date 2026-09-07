# ND-UX-V2 benchmark — neurodivergent and cognitive-accessibility patterns

Date: 2026-09-07
Baseline main: `33677f8fbe110c95adeedb9e90dd62c503d8c15c`
Programme: #155
First slice: #156

## Why this benchmark exists

ND-UX-V1 proved technical accessibility, governed scope visibility and responsive consistency, but the live Resources page still behaved like a database export: every reviewed resource was expanded in one long, visually repetitive list.

V2 therefore treats **cognitive usability as a first-class acceptance property**, not as a side-effect of semantic HTML or WCAG mechanics.

This benchmark deliberately separates:

- evidence-backed accessibility guidance;
- useful patterns observed on neurodiversity/disability websites;
- patterns that are attractive but should *not* be copied into ND Oracle.

## Strongest evidence base

### National Autistic Society + Hassell Inclusion — Autism Accessibility Guidelines

Source:
https://www.autism.org.uk/accessibility
https://dy55nndrxke1w.cloudfront.net/file/24/E0xBd-SE0PKVva5E0f_ZEHKO6YP/Autism%20Accessibility%20Guidelines%20Research%20Final%20Report%20-%20HI%20for%20National%20Autistic%20Society%20-%20tagged.pdf

The 2019 research combined desk research, expert interviews, a survey of 398 autistic respondents and user research with 17 autistic web users. The report proposes 49 guidelines.

High-value findings for ND Oracle:

- clear, clutter-free pages;
- page length appropriate to purpose;
- clearly separated page regions;
- important information near the top;
- a short summary of each page and its purpose;
- consistent, symmetrical grids for browse pages and single-column reading pages;
- simple and consistent navigation;
- fewer sequential menu choices;
- visibly clickable links and controls;
- muted colours rather than large bright areas;
- sufficient spacing between paragraphs and lines;
- short paragraphs and short lines;
- no autoplay or unexplained movement;
- clear, concise, literal language;
- customisation because autistic preferences conflict rather than converge on one perfect colour/font scheme.

The report is especially important for V2 because it found that **62% of survey respondents found too many choices confusing** and that excessive scrolling could be overwhelming for autistic users.

### W3C Cognitive Accessibility / COGA

Sources:
https://www.w3.org/TR/coga-usable/
https://www.w3.org/WAI/WCAG2/supplemental/patterns/o5p03-manageable-quantity/
https://www.w3.org/WAI/WCAG2/supplemental/patterns/o5p02-short-paths/
https://www.w3.org/WAI/WCAG2/supplemental/patterns/o2p03-page-structure/

Transferable rules:

- make the most important task easy to find;
- use clear visual boundaries and logical sections;
- keep critical paths short;
- reduce unnecessary content;
- where possible keep main choices to roughly five or fewer at one decision point;
- place extra choices behind clear progressive disclosure;
- provide search;
- use headings/signposts that let someone reorient after distraction;
- make simplified views from the same underlying content rather than deleting information.

This directly supports replacing the 168-resource expanded wall with a short discovery surface plus a deliberate full-catalogue fallback.

### British Dyslexia Association style guidance

Sources:
https://www.bdadyslexia.org.uk/
https://cdn.bdadyslexia.org.uk/uploads/documents/Advice/style-guide/BDA-Style-Guide-2023.pdf

Transferable rules:

- readable sans-serif fonts are a strong default;
- 16–19px-equivalent body text is appropriate for many readers;
- generous line and paragraph spacing;
- avoid excessive italics/underlining for emphasis;
- avoid long all-cap text;
- keep line lengths controlled;
- left-aligned, clearly separated content.

V2 decision: ND Oracle will use one consistent system sans-serif stack across navigation, headings and body text. Underlining remains for actual links because link recognition is an accessibility affordance.

## Website pattern scan

### Understood

Source:
https://www.understood.org/

Useful:

- starts from the user's situation rather than requiring taxonomy knowledge;
- search/ask is prominent;
- large content estate is divided into recognisable domains such as school/learning and daily life;
- “start your journey” and task-oriented labels create obvious entry points;
- articles use explicit key takeaways.

Do not copy:

- personalised/assistant authority;
- marketing density;
- newsletter/donation/partner surfaces;
- US-specific service taxonomy.

ND Oracle transfer:
**ordinary-language Find + life-problem routes + bounded category cards.**

### National Autistic Society

Sources:
https://www.autism.org.uk/
https://www.autism.org.uk/accessibility

Useful:

- advice is exposed through recognisable topic groups;
- dedicated audience routes;
- site search is prominent;
- explicit accessibility options;
- Vivid/Calm colour choice;
- research-backed commitment to clutter-free consistent design.

Do not copy:

- fundraising and campaign surfaces competing with support discovery;
- third-party accessibility overlay as a substitute for accessible core design.

ND Oracle transfer:
**support discovery first, preference controls later, no commercial/fundraising distraction.**

### Autistic Self Advocacy Network (ASAN)

Sources:
https://autisticadvocacy.org/resources/
https://autisticadvocacy.org/resources-3/accessibility/

Useful:

- separates resources into meaningful classes;
- repeatedly offers Easy Read and Plain Language versions;
- long toolkits are split into named parts;
- glossaries reduce vocabulary barriers;
- self-advocate purpose is explicit.

ND Oracle transfer:
**progressive disclosure, plain-language-first labels, and eventual alternative reading depth rather than forcing all detail into the first view.**

### Ambitious about Autism — young-person routing

Sources:
https://www.ambitiousaboutautism.org.uk/
https://www.ambitiousaboutautism.org.uk/what-we-do/services/i-am-an-autistic-young-person

Useful:

- the home/services architecture offers explicit audience routes such as “I am autistic” rather than making young people infer that the organisation is for them;
- the young-person page states age range and purpose immediately;
- opportunities are chunked into recognisable tasks such as community, employment and wellbeing;
- the organisation explicitly says autistic young people are involved in shaping its work.

ND Oracle transfer:
**later V2 young-person testing should ask whether a young person can recognise “this is for me” and reach school/college, wellbeing and community routes without knowing service-system vocabulary.** This is a content/navigation problem, not a reason to add juvenile decoration.

### British Dyslexia Association resource library

Source:
https://www.bdadyslexia.org.uk/resources

Useful:

- downloadable resources are presented as discrete, recognisable items with clear purpose;
- resource format/action (“Download”, “View booklet”) is obvious;
- visual card treatment prevents the page from becoming a continuous paragraph/list texture.

ND Oracle transfer:
**resource/category cards should look like choices, not rows in a ledger.**

### Neurodivergent Insights

Source:
https://neurodivergentinsights.com/

Useful:

- strong visual grouping of offerings;
- clear human-readable categories;
- visual identity makes major sections recognisable.

Do not copy:

- long commercial landing-page structure;
- repeated promotional calls to action;
- decorative density.

ND Oracle transfer:
**stronger section identity without marketing clutter.**

### Scope

Source:
https://www.scope.org.uk/news-and-stories/inclusion-and-accessibility-for-our-new-website

Useful process lesson:

- accessibility expertise was included throughout design/development rather than only at the end;
- disabled-user feedback was treated as an ongoing product input.

ND Oracle transfer:
**V2 cannot be closed by automated screenshots alone; real ND/young-person task testing must become an explicit later acceptance gate.**

## V2 synthesis

ND Oracle should not become visually loud or “gamified for neurodivergent people”.

The better target is:

> **Quiet, obvious and controllable.**

A strong ND Oracle discovery page should have:

1. one sentence saying what the page is for;
2. no more than four primary ways to start in the first decision region;
3. clear, equally sized, visibly clickable cards;
4. ordinary language rather than internal taxonomy;
5. restrained colour used to separate purposes, not decorate;
6. substantial whitespace between different tasks;
7. a prominent escape hatch to Find;
8. complete information preserved behind explicit “show everything” disclosure;
9. no animation, autoplay, pop-ups or surprise layout changes;
10. a consistent sans-serif reading system;
11. scope and non-endorsement visible before a user acts on a resource;
12. later user-controlled display preferences without requiring an account.

## V2.1 Resources design decision

The Resources landing page will change from:

> title → non-endorsement → category subnav → **168 expanded rows** → browse links

to:

> title + purpose → **four primary ways to start** → non-endorsement → common needs → resource families → **deliberate complete catalogue disclosure**

The four first decisions are:

- **Describe what you need** → Find;
- **Start from a life problem** → Needs;
- **Check what applies where I live** → Places;
- **Browse by kind of resource** → Types.

The complete alphabetical resource set remains present in static HTML, directly addressable, no-script compatible and available from both A–Z and an explicit native disclosure on the Resources page.

## What V2 will not claim

This benchmark does not establish that one design works for every neurodivergent person. The strongest autism research explicitly found conflicting preferences.

V2 therefore aims for:

- good low-overload defaults;
- conventional interaction;
- preserved information;
- progressive disclosure;
- future customisation;
- and real user testing.

It must not claim “neurodivergent-friendly” merely because a checklist passes.

## V2.4 design-method correction

The V2.1–V2.3 implementation exposed a weakness in this benchmark: it over-weighted bounded cards and separation while under-weighting whole-page composition, desktop overview and the cognitive cost of repeated containers.

The earlier recommendation for “clear, equally sized, visibly clickable cards” is therefore **superseded as a default**. Cards remain available only when an item is genuinely independent and benefits from an enclosing boundary.

From V2.4 onward:

- page composition is decided before component selection;
- long-form reading keeps a controlled measure, while discovery/index pages use the desktop viewport for overview;
- typography, spacing, rules and directional left-edge colour markers are preferred to hero panels and card grids;
- responsive design means recomposition, not merely stacking;
- ordinary-language recognition routes come before specialist taxonomy;
- unfamiliar specialist words may be split into meaningful parts as a learning aid, followed by the whole plain-language meaning;
- colour must be paired with text, position or structure and never be the only signal;
- every candidate receives a full-page hostile design review for viewport use, scrolling, container necessity, recognition load and subtraction opportunities.

The detailed governing correction is recorded in `docs/ND_UX_V2_4_DESIGN_CORRECTION.md`.

# ND Oracle Responsive Layout Standard v2.5

Status: candidate implementation for site-wide responsive acceptance.

## Purpose

Prevent public pages from collapsing into a narrow desktop "pencil" while preserving readable line length and simple mobile reflow.

## Layout contract

- The shared public page shell uses **90% of the available viewport width**.
- The shell is capped at **1600px** on very large screens.
- Reading measure is controlled inside the shell with a default **82ch** prose limit.
- The page canvas must not be narrowed merely to make prose readable.
- Headings are not constrained to the former 20ch measure.
- Question-page secondary material uses the available desktop canvas in two columns and collapses to one column before it becomes cramped.

## Responsive behaviour

The same 90% shell is retained from large desktop to small phone. Internal composition progressively collapses:

- very large desktop: full 90% shell, capped at 1600px;
- normal desktop/laptop: multi-column layout where it remains useful;
- mid-width/tablet: two-column structures reduce or collapse;
- phone: single-column composition;
- very small phone: single-column composition with long-heading wrapping protected.

The implementation uses content-driven breakpoints at 87.5rem, 62.5rem, 56rem, 43.75rem and 28rem.

## Standard acceptance viewports

1. 1920 × 1080
2. 1440 × 900
3. 1280 × 800
4. 1024 × 768
5. 768 × 1024
6. 430 × 932
7. 390 × 844
8. 320 × 568

The browser gate uses Chrome DevTools Protocol device-metrics emulation so the
430px, 390px and 320px cases are real CSS viewport widths rather than
headless Chrome's approximately 500px minimum outer-window width.

At every viewport the responsive browser gate must prove:

- the main shell is approximately 90% of the browser client width until the 1600px cap is reached;
- no horizontal overflow;
- the page heading remains inside the shell;
- the Question secondary grid collapses before narrow columns become unusable.

## Question-page composition

The Question renderer keeps the main answer in a readable prose measure and wraps these secondary sections in one responsive composition:

- Related things to inspect
- Related questions
- What evidence is still needed
- Where people may disagree
- When this answer should be revisited

This keeps the answer readable while allowing the wider desktop canvas to carry useful supporting material instead of leaving most of the page empty.

## Enforcement

The contract is enforced in four layers:

1. shared CSS tokens and shell rules;
2. Question renderer structure;
3. unit tests in `tests/test_responsive_layout_v25.py`;
4. exact-viewport Chrome DevTools Protocol width and overflow checks in `.github/workflows/ux-visual-evidence.yml` using `scripts/verify_responsive_layout_v25.py`.

The existing UX screenshot evidence remains in place for representative public routes.

## Acceptance boundary

The candidate can be marked final only after:

- repository validation is GREEN;
- visual-evidence workflow is GREEN;
- the eight-viewport responsive gate is GREEN;
- a human review confirms the original narrow Question-page failure is gone.

Production deployment remains a separate protected release action.

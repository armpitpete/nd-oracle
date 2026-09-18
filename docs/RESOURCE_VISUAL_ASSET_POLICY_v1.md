# Resource visual asset policy v1

Date: 2026-09-10
Status: V2.5 presentation contract

## Purpose

Books, games, apps, films, media and recognisable products benefit from a visual identity because a reader can recognise the item before processing all of its text. ND Oracle therefore treats product imagery as an accessibility/navigation aid when it can lawfully publish the asset.

**Canonical usefulness rule:** **Render a cleared visual when it materially helps the user recognise, distinguish or understand the resource.**

Usefulness is the first gate. Finding an image, owning a local copy or having permission does not by itself justify displaying it. A visual that does not materially help is recorded as `not-useful` and stays absent.

The image is **recognition material, not evidence**. It must never imply endorsement, efficacy, safety, suitability or a stronger evidence status.

## Registry

`site/resource-visuals.json` is the controlled sidecar for resource imagery. Every governed Resource must have an explicit registry entry. In a production/full-corpus build, absence from the registry is an error rather than an implicit no-image decision.

A registry item may have one of these states:

- `cleared` — rights basis has been reviewed and a local asset may render;
- `permission-required` — a useful image exists but ND Oracle has no recorded permission/licence to republish it;
- `rights-unknown` — provenance or rights are not sufficiently established;
- `not-useful` — an image would not materially improve recognition.

Only `cleared` may render, and only when `materially_helpful` is true with one or more recorded usefulness reasons: `recognise`, `distinguish`, or `understand`. Rendering is derived from those fields; the registry does not contain an independent `render` switch.

## Required fields for a rendered visual

A `cleared` entry must record:

- exact Resource ID;
- local repository asset path under `site/resource-media/`;
- useful alt text;
- source URL or other provenance locator;
- rights holder or licensor where known;
- explicit rights basis/licence/permission;
- date checked;
- optional attribution text when required.

The build must fail closed if a `cleared` entry lacks the local file or required rights/provenance fields.


## Asset format and size boundary

Publishable local assets are limited to PNG, JPEG, WebP and SVG. A single source asset must be no larger than 1.5 MB. Presentation CSS preserves the useful source aspect ratio rather than forcing every resource into a square thumbnail. Cropping must not remove identifying information such as a book title, game identity or app mark.

The source file remains local under `site/resource-media/`; the generated public path is `/resource-media/<filename>`. Remote image URLs are provenance only and are never used as the rendered image source.

## Prohibited shortcuts

Do not:

- hotlink third-party covers, logos or screenshots;
- scrape images because they appear on a public website;
- copy a product image merely because ND Oracle is non-commercial;
- create a lookalike image and present it as the product;
- infer permission from a wiki/community upload policy that applies only to that site;
- allow imagery to change resource ranking, evidence status or recommendation language.

A missing visual is preferable to an unlicensed or misleading one. A Resource that fails the usefulness gate is explicitly recorded as `not-useful`; it is not silently omitted from the registry.

## Stardew Valley disposition

`stardew-valley` is currently `permission-required`.

The official Stardew Valley terms state that website images and other site materials are protected, restrict reproduction/public display/republishing, and state that relevant marks require prior written permission. ND Oracle therefore does not copy or hotlink official Stardew Valley artwork under this policy without a separately recorded permission or other reviewed rights basis.

Source checked: `https://www.stardewvalley.net/terms/` on 2026-09-10.

This disposition does **not** prevent the text Resource listing, official access link, descriptive metadata or governed navigation from being published.

## Accessibility

- Alt text identifies the item and the useful recognition content; it does not repeat every visible word on a cover.
- Decorative crop choices must not remove information needed to recognise the product.
- Images must reflow without horizontal scrolling and must not push the resource title/essential warning below an unreasonable first-screen distance.
- When images are unavailable, the page remains structurally complete and understandable.

## Review trigger

Reopen an entry when:

- the rights holder grants permission;
- a clearly compatible licence becomes available;
- ND Oracle receives an authorised press/media asset licence;
- the source or rights status changes;
- a visual stops being useful or becomes misleading.

# The Neurodiverse Oracle — repeat production release contract v0.2

Status: release-path repair candidate; no deployment performed by this record

Date: 2026-08-12

## Why this repair exists

Site Shell v0.1 has already been accepted in production at `https://ndoracle.org`, with the apex domain attached to the existing `nd-oracle` Cloudflare Pages Direct Upload project.

The original guarded deployment workflow was deliberately written for the first deployment. It therefore refused to upload whenever `ndoracle.org` was already attached. That was safe before first activation, but after production acceptance it made every later production update fail closed for the wrong reason.

Whole-site v0.2 is now integrated on protected `main`, so the release path must distinguish accepted production state from an unexpected domain change.

A first repeat-release repair correctly allowed the accepted apex domain, but its live preflight exposed a Cloudflare API representation detail: the production project payload reports the built-in `nd-oracle.pages.dev` project subdomain both through the dedicated `subdomain` field and in the project `domains` collection. Treating every `domains` entry as a user-added custom domain therefore produced a false mismatch before upload.

## Repeat-release invariant

A production upload is permitted only when all of the following remain true at dispatch and immediately before upload:

- the requested release is an exact 40-character SHA;
- that SHA is the current protected `main`;
- the pre-existing `cloudflare-pages-production` GitHub environment is restricted to protected branches;
- repository validation, the complete regression suite, and the real static-site build pass from the exact release checkout;
- the deployment artifact remains static and contains no Pages Functions, Worker, symlink, or Wrangler configuration broadening;
- the Cloudflare Pages project is exactly `nd-oracle`;
- the project remains a Direct Upload project with production branch `main`;
- the dedicated Cloudflare project subdomain remains exactly `nd-oracle.pages.dev`;
- after normalizing that built-in project subdomain out of the project `domains` collection, the remaining custom-domain set is exactly `ndoracle.org`;
- Wrangler remains pinned to the repository-reviewed version;
- the workflow performs no custom-domain, DNS, redirect, or zone mutation.

If any of those invariants fails, the workflow refuses the upload.

The `www.ndoracle.org` redirect remains separate Cloudflare redirect/DNS state and must not silently become a second Pages custom-domain attachment.

## What changed from the first-release guard

The obsolete first-release condition was:

> refuse deployment if `ndoracle.org` is attached.

The first repeat-release repair changed that to an exact project `domains` set containing only `ndoracle.org`. Live preflight proved that assumption was too strict because the Cloudflare API also returned the built-in `nd-oracle.pages.dev` hostname in that collection.

The corrected repeat-release condition is:

> require the project `subdomain` field to remain exactly `nd-oracle.pages.dev`; normalize that provider-owned hostname out of the project `domains` collection; then require the remaining custom-domain set to remain exactly `ndoracle.org`.

This preserves fail-closed checking for missing or additional custom domains while accepting Cloudflare's observed project representation. It does not broaden accepted production state.

## Cloudflare model checked

Current Cloudflare Pages documentation identifies `subdomain` as the Cloudflare subdomain associated with the project and documents custom domains separately. Cloudflare also documents that each Pages project receives a `*.pages.dev` hostname. The live production preflight on 2026-08-12 established that the project payload for `nd-oracle` includes `nd-oracle.pages.dev` in `domains` as well as in `subdomain`, so the workflow normalizes the provider-owned hostname before comparing custom-domain state.

Current Cloudflare Pages documentation also describes Direct Upload as supporting subsequent deployments to the same project with `wrangler pages deploy`.

## Publication sequence for whole-site v0.2

1. merge this bounded release-path repair only after exact-head validation passes;
2. resolve the new exact protected `main` SHA after merge;
3. manually dispatch `Deploy Cloudflare Pages (manual)` from `main` with that exact SHA;
4. let the workflow revalidate, rebuild, digest, recheck GitHub/Cloudflare state, and upload the exact artifact;
5. verify the resulting production deployment on `https://ndoracle.org`, including the homepage, Understand, How it works, all five topic pages, 404 behavior, sitemap/robots, security headers, and `www` redirect;
6. record the new accepted production identity separately.

## Boundaries

This repair does not change knowledge objects, site copy, site CSS, schema, DNS, custom domains, redirects, Cloudflare project identity, analytics, accounts, forms, or personal-data collection. It does not make deployments automatic.

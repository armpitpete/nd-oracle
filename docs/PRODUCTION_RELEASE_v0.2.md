# The Neurodiverse Oracle — repeat production release contract v0.2

Status: release-path repair candidate; no deployment performed by this record

Date: 2026-08-12

## Why this repair exists

Site Shell v0.1 has already been accepted in production at `https://ndoracle.org`, with the apex domain attached to the existing `nd-oracle` Cloudflare Pages Direct Upload project.

The original guarded deployment workflow was deliberately written for the first deployment. It therefore refused to upload whenever `ndoracle.org` was already attached. That was safe before first activation, but after production acceptance it made every later production update fail closed for the wrong reason.

Whole-site v0.2 is now integrated on protected `main`, so the release path must distinguish an accepted existing production domain from an unexpected domain mutation.

## Repeat-release invariant

A production upload is permitted only when all of the following remain true at dispatch and immediately before upload:

- the requested release is an exact 40-character SHA;
- that SHA is the current protected `main`;
- the pre-existing `cloudflare-pages-production` GitHub environment is restricted to protected branches;
- repository validation, the complete regression suite, and the real static-site build pass from the exact release checkout;
- the deployment artifact remains static and contains no Pages Functions, Worker, symlink, or Wrangler configuration broadening;
- the Cloudflare Pages project is exactly `nd-oracle`;
- the project remains a Direct Upload project with production branch `main`;
- the accepted production domain `ndoracle.org` remains attached;
- no unexpected `*.ndoracle.org` Pages custom-domain attachment has appeared;
- Wrangler remains pinned to the repository-reviewed version;
- the workflow performs no custom-domain, DNS, redirect, or zone mutation.

If any of those invariants fails, the workflow refuses the upload.

## What changed from the first-release guard

The obsolete first-release condition was:

> refuse deployment if `ndoracle.org` is attached.

The repeat-release condition is:

> require the already accepted `ndoracle.org` attachment to remain present, reject unexpected ND Oracle subdomain attachments, and leave all domain/DNS state untouched.

This makes the release workflow reusable without turning deployment into an automatic merge side effect.

## Cloudflare model checked

Current Cloudflare Pages documentation describes Direct Upload as supporting first and subsequent deployments to the same project with `wrangler pages deploy`. Custom-domain association is managed separately from the asset upload. The workflow therefore treats the existing domain attachment as production state to verify, not state to create or remove.

## Publication sequence for whole-site v0.2

1. merge this bounded release-path repair only after exact-head validation passes;
2. resolve the new exact protected `main` SHA after merge;
3. manually dispatch `Deploy Cloudflare Pages (manual)` from `main` with that exact SHA;
4. let the workflow revalidate, rebuild, digest, recheck GitHub/Cloudflare state, and upload the exact artifact;
5. verify the resulting production deployment on `https://ndoracle.org`, including the homepage, Understand, How it works, all five topic pages, 404 behavior, sitemap/robots, security headers, and `www` redirect;
6. record the new accepted production identity separately.

## Boundaries

This repair does not change knowledge objects, site copy, site CSS, schema, DNS, custom domains, redirects, Cloudflare project identity, analytics, accounts, forms, or personal-data collection. It does not make deployments automatic.

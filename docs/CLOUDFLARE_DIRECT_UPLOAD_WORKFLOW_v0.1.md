# The Neurodiverse Oracle — Manual Cloudflare Direct Upload Workflow v0.1

Status: implementation candidate; no deployment performed

Date: 2026-08-10

## Purpose

`.github/workflows/deploy-cloudflare-pages.yml` provides a manual-only production release path for the static Site Shell.

The workflow is intentionally narrower than general CI/CD. A merge to `main` does not deploy anything. A release requires a separate `workflow_dispatch` action and an exact 40-character Git commit SHA.

## Release invariants

The workflow must fail unless all of these remain true:

1. the workflow was started explicitly with `workflow_dispatch`;
2. the selected workflow ref is `main`;
3. `release_sha` is an exact lowercase 40-character SHA;
4. that SHA is the current GitHub `main` when the guard runs;
5. the checkout resolves to that exact SHA and is clean;
6. repository validation and the complete regression suite pass again;
7. `dist/` rebuilds successfully from that checkout;
8. the release remains static: no `functions/`, `_worker.js` or Wrangler configuration is present;
9. the pinned deployment CLI reports Wrangler `4.114.0`;
10. Cloudflare credentials are present as GitHub Actions secrets;
11. an existing Pages project named `nd-oracle` is found;
12. the project production branch is `main`;
13. the project is Direct Upload rather than Git-integrated;
14. `ndoracle.org` is not attached as a custom domain;
15. immediately before upload, the release SHA is still current GitHub `main` and the Cloudflare project still satisfies the protected boundary.

If any invariant fails, deployment stops before the upload command.

## GitHub environment and secrets

Before the first dispatch, create a GitHub Actions environment named:

`cloudflare-pages-production`

Prefer storing the Cloudflare credentials as **environment secrets** rather than broad repository secrets. Configure the environment so deployments are allowed only from protected `main` where the repository plan/settings support deployment-branch restrictions.

Required secret names:

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

The Cloudflare token should be a least-privilege custom API token scoped to the intended account with **Cloudflare Pages Write** access. Do not give this release token DNS/zone-edit permissions; this workflow does not require them.

Do not commit either value to the repository.

## Existing Pages project requirement

This workflow deliberately does **not** create a Cloudflare Pages project.

Before it can deploy, an existing project must satisfy:

- project name: `nd-oracle`;
- hosting model: Direct Upload;
- production branch: `main`;
- `ndoracle.org` not attached.

Project creation is a separate production mutation and should retain its own acceptance evidence if it has not already occurred.

## Build and release proof

The deployment job repeats the same repository validation path used by normal CI, then explicitly builds `dist/`.

Before upload it records a deterministic SHA-256 digest over the generated artifact paths and bytes in the GitHub Actions run summary. This does not replace the Git release SHA; it provides an additional identity for the exact generated static artifact.

The deployment command is deliberately explicit:

```sh
npx --yes wrangler@4.114.0 pages deploy dist \
  --project-name="$PROJECT_NAME" \
  --branch=main \
  --commit-hash="$RELEASE_SHA" \
  --commit-dirty=false \
  --experimental-provision=false \
  --experimental-auto-create=false \
  --install-skills=false
```

The workflow does not contain project-create, custom-domain or DNS commands.

## How to run after merge

1. Resolve protected `main` immediately before release.
2. In GitHub Actions, choose **Deploy Cloudflare Pages (manual)**.
3. Select the `main` ref.
4. Paste the full current `main` SHA into `release_sha`.
5. Run the workflow.

Do not reuse a remembered SHA after another merge. If `main` changes between authorisation and upload, the workflow fails closed.

## What a successful run proves

A successful workflow run proves that:

- the supplied SHA was current `main` at the release guards;
- that exact commit was rebuilt and validated;
- the generated artifact satisfied the static release boundary;
- the intended existing Direct Upload project was used;
- Wrangler 4.114.0 completed a Pages Direct Upload with the exact commit metadata;
- this workflow did not request custom-domain or DNS mutation.

It does **not** by itself prove public acceptance of `ndoracle.org`, because that hostname remains outside this lane.

The next evidence step after an authorised deployment is live verification of the resulting `pages.dev` deployment: deployment identity, HTTPS response, `_headers`, navigation and content. Custom-domain attachment remains a later protected gate.

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
5. the GitHub environment `cloudflare-pages-production` already exists before dispatch;
6. that environment is restricted to protected branches rather than relying on implicit environment creation;
7. the checkout resolves to that exact SHA and is clean;
8. repository validation and the complete regression suite pass again;
9. `dist/` rebuilds successfully from that checkout;
10. the release remains static: no `functions/`, `_worker.js` or Wrangler configuration is present;
11. the pinned deployment CLI reports Wrangler `4.114.0`;
12. Cloudflare credentials are present as GitHub Actions secrets;
13. an existing Pages project named `nd-oracle` is found;
14. the project production branch is `main`;
15. the project is Direct Upload rather than Git-integrated;
16. `ndoracle.org` is not attached as a custom domain;
17. immediately before upload, the release SHA is still current GitHub `main` and the Cloudflare project still satisfies the protected boundary.

If any invariant fails, deployment stops before the upload command.

## GitHub environment and secrets

Before the first dispatch, create a GitHub Actions environment named:

`cloudflare-pages-production`

Configure its deployment branches to **Protected branches only**. The release workflow's first `guard` job checks the GitHub environment API before the deployment job starts and refuses to continue unless the environment already exists with `protected_branches=true`, `custom_branch_policies=false`, and a branch-policy protection rule.

This extra guard is intentional. GitHub documents that running a workflow which references an environment that does not exist can create the environment automatically. Production must not depend on that implicit path because it could create an environment without the intended protection policy.

Prefer storing the Cloudflare credentials as **environment secrets** rather than broad repository secrets.

Required secret names:

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

The Cloudflare token should be a least-privilege custom API token scoped to the intended account with **Cloudflare Pages Write** access. Do not give this release token DNS/zone-edit permissions; this workflow does not require them.

Do not commit either value to the repository.

### Current prerequisite state checked 2026-08-10

Repository environment inspection found:

- `cloudflare-pages-production`: **absent**;
- `github-pages`: present.

The existing `github-pages` environment does not satisfy this workflow and must not be substituted for the Cloudflare production environment.

Because the GitHub connector available during implementation has read access to environment metadata but not environment-administration or secret-management operations, creation of `cloudflare-pages-production`, its protected-branch policy, and its two secrets remains an explicit GitHub settings action before first dispatch.

For private repositories, GitHub currently requires GitHub Pro, Team, or Enterprise for environment secrets and deployment-branch restrictions. If the repository plan does not expose those controls, do not weaken this workflow silently; choose and review an alternative secret/isolation design first.

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

1. Verify `cloudflare-pages-production` exists and is restricted to protected branches.
2. Verify its two Cloudflare environment secrets are set.
3. Verify the existing Cloudflare Pages project satisfies the Direct Upload requirements.
4. Resolve protected `main` immediately before release.
5. In GitHub Actions, choose **Deploy Cloudflare Pages (manual)**.
6. Select the `main` ref.
7. Paste the full current `main` SHA into `release_sha`.
8. Run the workflow.

Do not reuse a remembered SHA after another merge. If `main` changes between authorisation and upload, the workflow fails closed.

## What a successful run proves

A successful workflow run proves that:

- the supplied SHA was current `main` at the release guards;
- the production environment already existed with protected-branch restriction before the deployment job;
- that exact commit was rebuilt and validated;
- the generated artifact satisfied the static release boundary;
- the intended existing Direct Upload project was used;
- Wrangler 4.114.0 completed a Pages Direct Upload with the exact commit metadata;
- this workflow did not request custom-domain or DNS mutation.

It does **not** by itself prove public acceptance of `ndoracle.org`, because that hostname remains outside this lane.

The next evidence step after an authorised deployment is live verification of the resulting `pages.dev` deployment: deployment identity, HTTPS response, `_headers`, navigation and content. Custom-domain attachment remains a later protected gate.

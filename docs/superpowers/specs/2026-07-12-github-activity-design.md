# GitHub Activity Section Design

## Goal

Add an elegant, automatically updated GitHub activity section to the profile
README. The section should communicate project impact and open-source
contribution strength without presenting repository ownership statistics that
are technically correct but unhelpful, such as `Owned repository stars: 0`.

## Scope

### In scope

- Add a `GitHub Activity` section near the top of `README.md`, after the
  introduction and before the detailed project sections.
- Highlight Fulling separately as a maintained project with its repository star
  count labeled explicitly as `Fulling stars`.
- Render five automatically refreshed metrics: Fulling stars, merged pull
  requests, pull requests, commits, and contributed projects.
- Add a repository-local Python script that reads public GitHub API data and
  rewrites only a marked activity block in `README.md`.
- Add a GitHub Actions workflow that updates the block on a schedule, on pushes
  to `main`, and through manual dispatch.
- Keep the activity section free of third-party image/stat services.

### Out of scope

- Do not show `Owned repository stars`.
- Do not count Fulling stars as personal stars; label them as project-level
  impact.
- Do not change the existing contribution-role descriptions or owned-project
  descriptions except for inserting the new activity section.
- Do not add private repository data or expose tokens in the README.
- Do not push changes as part of implementation.

## Activity metrics

The generated block will use the following definitions:

- **Fulling stars:** `stargazers_count` for `FullAgent/fulling`, displayed as a
  repository-level project impact metric.
- **Merged PRs:** GitHub search count for PRs authored by `Che-Zhu` and merged
  on GitHub.
- **Pull Requests:** GitHub search count for PRs authored by `Che-Zhu`.
- **Commits:** GitHub search count for commits authored by `Che-Zhu`.
- **Contributed projects:** number of distinct repositories appearing in the
  authored PR search results.

The search metrics represent public GitHub activity visible to the workflow's
token. Counts are formatted with thousands separators for readability.

## README presentation

The activity section will follow this structure. The metric values are inserted
by the generator; the stable layout is shown here:

```md
## GitHub Activity

<p align="center">
  <a href="https://github.com/FullAgent/fulling">
    <strong>Fulling</strong><br />
    <sub>Lead maintainer · project reach</sub>
  </a>
</p>

<!-- ACTIVITY:START -->
<table align="center">
  <tr>
    <td align="center"><sub>Fulling stars</sub></td>
    <td align="center"><sub>Merged PRs</sub></td>
    <td align="center"><sub>Pull Requests</sub></td>
    <td align="center"><sub>Commits</sub></td>
    <td align="center"><sub>Contributed projects</sub></td>
  </tr>
</table>
<!-- ACTIVITY:END -->

<p align="center">
  <sub>Updated automatically from GitHub.</sub>
</p>
```

The role-oriented project sections remain the main narrative. The activity
table supports that narrative with transparent, contribution-relevant signals.

## Automation design

### `scripts/update_github_activity.py`

- Use Python standard-library HTTP and JSON support so the workflow needs no
  third-party dependency installation.
- Read `GITHUB_TOKEN` and use `GITHUB_USERNAME=Che-Zhu` by default.
- Fetch Fulling repository metadata and paginate authored PR search results.
- Use GitHub search totals for authored PRs, merged PRs, and authored commits.
- Derive contributed-project count from unique repository URLs in authored PR
  results.
- Replace only the content between `ACTIVITY:START` and `ACTIVITY:END`.
- Fail clearly if the markers are missing or an API request fails.

### `.github/workflows/update-github-activity.yml`

- Run on a twice-daily schedule, on pushes to `main`, and through
  `workflow_dispatch`.
- Grant only `contents: write` permission needed to commit the generated
  README block.
- Run the script with the repository's `GITHUB_TOKEN`.
- Commit only `README.md` when the generated content changes.

## Acceptance criteria

- The README contains the two-level activity presentation and no owned-stars
  zero metric.
- Fulling stars are labeled as project-level stars and link to Fulling.
- The five metrics are generated from GitHub API data, not hardcoded.
- The script updates only the marked block and preserves the rest of README.
- The workflow has schedule, push, and manual triggers and does not require
  third-party stats services.
- Python syntax, Markdown whitespace, marker presence, and workflow YAML are
  verified locally.

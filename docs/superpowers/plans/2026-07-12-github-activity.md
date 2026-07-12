# GitHub Activity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a repository-local, automatically refreshed GitHub Activity section that highlights Fulling's project reach and Che-Zhu's open-source contribution activity.

**Architecture:** A standard-library Python script will fetch GitHub REST API data, compute five metrics, and replace only the marked activity block in `README.md`. A GitHub Actions workflow will run the script twice daily, on pushes to `main`, and on manual dispatch, then commit `README.md` only when the block changes.

**Tech Stack:** Python 3 standard library (`urllib`, `json`, `re`); GitHub REST API; GitHub Actions; GitHub-Flavored Markdown and HTML.

## Global Constraints

- Do not show `Owned repository stars`.
- Do not count Fulling stars as personal stars; label them as project-level impact.
- Do not change the existing contribution-role descriptions or owned-project descriptions except for inserting the new activity section.
- Do not add private repository data or expose tokens in the README.
- Keep the activity section free of third-party image/stat services.
- Do not push changes as part of implementation.

---

### Task 1: Add the GitHub activity generator

**Files:**
- Create: `/Users/che/Documents/GitHub/che-zhu/scripts/update_github_activity.py`

**Interfaces:**
- Consumes: `GITHUB_TOKEN` and optional `GITHUB_USERNAME`; `README.md` markers `ACTIVITY:START` and `ACTIVITY:END`.
- Produces: A generated HTML table with Fulling stars, merged PRs, pull requests, commits, and contributed projects.

- [ ] **Step 1: Create the generator with explicit API headers and pagination**

Implement the script with this behavior:

```python
#!/usr/bin/env python3

import json
import os
import re
import urllib.parse
import urllib.request


API_BASE = "https://api.github.com"
README_PATH = "README.md"
USERNAME = os.environ.get("GITHUB_USERNAME", "Che-Zhu")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
PAGE_SIZE = 100


def request_json(path, params=None):
    query = urllib.parse.urlencode(params or {})
    url = f"{API_BASE}{path}"
    if query:
        url = f"{url}?{query}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Che-Zhu-readme-activity",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def search_count(endpoint, query):
    result = request_json(f"/search/{endpoint}", {"q": query, "per_page": 1})
    return result["total_count"]


def get_fulling_stars():
    repository = request_json("/repos/FullAgent/fulling")
    return repository["stargazers_count"]


def get_contributed_projects():
    repositories = set()
    page = 1

    while True:
        result = request_json(
            "/search/issues",
            {
                "q": f"author:{USERNAME} is:pr",
                "per_page": PAGE_SIZE,
                "page": page,
            },
        )
        items = result.get("items", [])
        repositories.update(
            item["repository_url"]
            for item in items
            if item.get("repository_url")
        )
        if len(items) < PAGE_SIZE:
            break
        page += 1

    return len(repositories)


def get_metrics():
    return {
        "fulling_stars": get_fulling_stars(),
        "merged_prs": search_count(
            "issues", f"author:{USERNAME} is:pr is:merged"
        ),
        "pull_requests": search_count("issues", f"author:{USERNAME} is:pr"),
        "commits": search_count("commits", f"author:{USERNAME}"),
        "contributed_projects": get_contributed_projects(),
    }


def format_number(value):
    return f"{value:,}"


def build_activity_block(metrics):
    cards = [
        ("Fulling stars", metrics["fulling_stars"]),
        ("Merged PRs", metrics["merged_prs"]),
        ("Pull Requests", metrics["pull_requests"]),
        ("Commits", metrics["commits"]),
        ("Contributed projects", metrics["contributed_projects"]),
    ]
    cells = [
        f'    <td align="center"><strong>{format_number(value)}</strong><br /><sub>{label}</sub></td>'
        for label, value in cards
    ]
    return "\n".join(
        [
            "<!-- ACTIVITY:START -->",
            '<table align="center">',
            "  <tr>",
            *cells,
            "  </tr>",
            "</table>",
            "<!-- ACTIVITY:END -->",
        ]
    )


def update_readme(metrics):
    with open(README_PATH, "r", encoding="utf-8") as file:
        readme = file.read()

    pattern = r"<!-- ACTIVITY:START -->.*?<!-- ACTIVITY:END -->"
    if re.search(pattern, readme, flags=re.DOTALL) is None:
        raise RuntimeError("Activity markers were not found in README.md")

    updated = re.sub(
        pattern,
        build_activity_block(metrics),
        readme,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(updated)


if __name__ == "__main__":
    update_readme(get_metrics())
```

The implementation must preserve the existing API headers, fail on missing
markers, paginate authored PR results, and write only the marked block.

- [ ] **Step 2: Run Python syntax validation**

Run:

```bash
python3 -m py_compile scripts/update_github_activity.py
```

Expected: exit status `0` and no output.

### Task 2: Add the generated README section and workflow

**Files:**
- Modify: `/Users/che/Documents/GitHub/che-zhu/README.md`
- Create: `/Users/che/Documents/GitHub/che-zhu/.github/workflows/update-github-activity.yml`

**Interfaces:**
- Consumes: `scripts/update_github_activity.py` from Task 1.
- Produces: A marked activity block and an automated update workflow.

- [ ] **Step 1: Insert the stable activity presentation after the introduction**

Insert this exact static structure after the introductory paragraph and before
`## Selected Contributions`:

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
    <td align="center"><strong>2,425</strong><br /><sub>Fulling stars</sub></td>
    <td align="center"><strong>183</strong><br /><sub>Merged PRs</sub></td>
    <td align="center"><strong>195</strong><br /><sub>Pull Requests</sub></td>
    <td align="center"><strong>760</strong><br /><sub>Commits</sub></td>
    <td align="center"><strong>29</strong><br /><sub>Contributed projects</sub></td>
  </tr>
</table>
<!-- ACTIVITY:END -->

<p align="center">
  <sub>Updated automatically from GitHub.</sub>
</p>
```

The generator will replace the five values on every run. These values are the
current API snapshot used for the initial block and are not manually maintained.

- [ ] **Step 2: Create the GitHub Actions workflow**

Write `.github/workflows/update-github-activity.yml` as:

```yaml
name: Update GitHub activity

on:
  schedule:
    - cron: "17 */12 * * *"
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Update activity
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_USERNAME: Che-Zhu
        run: python3 scripts/update_github_activity.py

      - name: Commit activity update
        run: |
          if git diff --quiet -- README.md; then
            echo "No activity changes."
            exit 0
          fi
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git commit -m "docs: update GitHub activity"
          git push
```

- [ ] **Step 3: Validate workflow YAML and markers**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file(".github/workflows/update-github-activity.yml"); puts "valid YAML"'
rg -n "GitHub Activity|ACTIVITY:START|ACTIVITY:END|Fulling stars|Merged PRs|Contributed projects" README.md
```

Expected: Ruby prints `valid YAML`; the second command finds the activity
heading, both markers, and all generated metric labels.

### Task 3: Run the generator and verify the final artifact

**Files:**
- Modify: `/Users/che/Documents/GitHub/che-zhu/README.md` through the generator.

**Interfaces:**
- Consumes: GitHub API data using the local authenticated token.
- Produces: A README block containing fresh current metric values.

- [ ] **Step 1: Run the generator against GitHub**

Run:

```bash
GITHUB_TOKEN="$(gh auth token)" python3 scripts/update_github_activity.py
```

Expected: exit status `0`; only the values between the activity markers change.

- [ ] **Step 2: Verify formatting and scope**

Run:

```bash
git diff --check
git diff -- README.md
git status --short
```

Expected: no whitespace errors; the diff contains the new activity section and
generated values but no third-party stats image; the only implementation files
are `README.md`, `.github/workflows/update-github-activity.yml`, and
`scripts/update_github_activity.py`.

- [ ] **Step 3: Commit the local implementation**

Run:

```bash
git add README.md .github/workflows/update-github-activity.yml scripts/update_github_activity.py
git commit -m "feat: add automated GitHub activity section"
```

Expected: a local commit is created; no `git push` command is run.

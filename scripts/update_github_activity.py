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

# GitHub Profile README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the stats-only profile README with a concise, credible English-language profile centered on verified upstream contributions and two original projects.

**Architecture:** Keep the profile as one Markdown document with a linear recruiter-friendly reading order: positioning, selected contributions, original projects, focus areas, and supporting GitHub stats. No application code, dependencies, or external services are involved.

**Tech Stack:** GitHub-Flavored Markdown; existing GitHub Readme Stats image.

## Global Constraints

- Do not mention `guixu`.
- Do not modify any repository other than this profile repository.
- Do not add unverified contact details, inflated metrics, or claims of sole ownership over upstream or forked projects.
- Do not push changes to GitHub.
- Keep the README concise enough to scan quickly and suitable for recruiters and engineering collaborators.

---

### Task 1: Rewrite the profile README

**Files:**
- Modify: `/Users/che/Documents/GitHub/che-zhu/README.md`

**Interfaces:**
- Consumes: The approved profile design in `/Users/che/Documents/GitHub/che-zhu/docs/superpowers/specs/2026-07-12-github-profile-readme-design.md`.
- Produces: A self-contained GitHub profile README with the sections `Selected Contributions`, `Original Projects`, and `Focus`.

- [ ] **Step 1: Replace the stats-only content with the approved structure**

Write the README with this content shape:

```md
# Che Zhu

Software Engineer contributing to AI-native developer platforms and cloud infrastructure.

I work across AI agents, developer tooling, cloud infrastructure, and full-stack product engineering.

## Selected Contributions

- [Fulling](https://github.com/FullAgent/fulling) — Contributed to GitHub integrations, asynchronous task workflows, sandbox runtime, database lifecycle, and deployment flows.
- [Codex Gateway](https://github.com/labring/codex-gateway) — Contributed to the Rust gateway runtime, session handling, turn interruption, Devbox runtime, logging, and CI.
- [Sealos Brain](https://github.com/labring/brain) — Contributed to Skills workflows, database handling, template caching, quota UI, and Kubernetes-backed product flows.
- [ShipRepo](https://github.com/labring/ShipRepo) — Contributed to stateless deployment APIs, GitHub OAuth, kubeconfig bootstrap, and AI proxy provisioning.
- [Sealos](https://github.com/labring/sealos) — Contributed to desktop, database-provider, and app-launchpad workflows.

## Original Projects

- [brain-skills-benchmark](https://github.com/Che-Zhu/brain-skills-benchmark) — An end-to-end benchmark for Devbox, Codex Gateway, Sandbox, and AI skill workflows.
- [brain-sandbox-skills](https://github.com/Che-Zhu/brain-sandbox-skills) — Sandbox deployment skills covering BuildKit, GHCR, and Crossplane workflows.

## Focus

`TypeScript` · `React` · `Next.js` · `Rust` · `Python` · `Kubernetes` · `PostgreSQL` · `AI Agents` · `Developer Tools`

![My GitHub stats](https://github-readme-stats.vercel.app/api?username=che-zhu&show_icons=true&theme=dark&count_private=true)
```

Use contribution-oriented verbs for upstream work and keep the stats image at the bottom. Do not add `guixu` or any unverified personal links.

- [ ] **Step 2: Check the Markdown diff for whitespace errors**

Run:

```bash
git diff --check
```

Expected: no output and exit status `0`.

- [ ] **Step 3: Check the required content and forbidden name**

Run:

```bash
rg -n "Selected Contributions|Original Projects|Focus|Fulling|Codex Gateway|Sealos Brain|ShipRepo|brain-skills-benchmark|brain-sandbox-skills" README.md
rg -ni "guixu" README.md
```

Expected: the first command finds all required sections and projects; the second command finds no matches.

- [ ] **Step 4: Review the final diff and repository scope**

Run:

```bash
git diff -- README.md
git status --short
```

Expected: only `README.md` is modified for the implementation, with no remote operation performed.

- [ ] **Step 5: Commit the local README update**

Run:

```bash
git add README.md
git commit -m "docs: refresh GitHub profile README"
```

Expected: a new local commit is created; no `git push` command is run.

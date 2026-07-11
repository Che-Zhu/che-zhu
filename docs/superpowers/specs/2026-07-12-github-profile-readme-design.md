# GitHub Profile README Design

## Goal

Update the `Che-Zhu/che-zhu` profile repository's `README.md` so it presents a
clear, credible English-language job-seeking profile. The page should emphasize
ongoing contributions to real AI and cloud-platform projects rather than imply
that forked repositories are original work.

## Scope

### In scope

- Replace the current stats-only README with a contribution-led profile.
- Describe selected contributions to Fulling, Codex Gateway, Sealos Brain,
  ShipRepo, and Sealos.
- List `brain-skills-benchmark` and `brain-sandbox-skills` separately as
  original projects.
- Keep GitHub stats at the bottom as secondary information.
- Use concise English suitable for recruiters and engineering collaborators.

### Out of scope

- Do not mention `guixu`.
- Do not modify any other repository.
- Do not add unverified contact details, inflated metrics, or claims of sole
  ownership over upstream or forked projects.
- Do not push changes to GitHub.

## Information architecture

1. `# Che Zhu`
2. One-sentence professional positioning focused on AI-native developer
   platforms and cloud infrastructure.
3. A short introductory paragraph covering developer tooling, AI agents, and
   full-stack/platform engineering.
4. `## Selected Contributions` with concise, contribution-oriented bullets for
   the five selected projects.
5. `## Original Projects` with the two confirmed original repositories.
6. `## Focus` with the relevant technology and domain keywords.
7. GitHub stats image at the bottom as supporting information.

## Writing rules

- Use wording such as “Contributed to” and “Worked on” for upstream work.
- Keep ownership and contribution relationships explicit where useful.
- Prefer concrete areas of work—GitHub integrations, agent runtimes,
  deployment systems, Kubernetes workflows, and developer tooling—over vague
  self-descriptions.
- Keep the README short enough to scan quickly and avoid turning it into a
  full resume.

## Acceptance criteria

- The README immediately communicates a coherent engineering profile.
- Forked or upstream projects are not presented as personal originals.
- The two original projects are visibly separated from selected contributions.
- `guixu` does not appear anywhere in the README.
- Markdown structure and links render cleanly.
- Only local files are changed; no remote push is performed.

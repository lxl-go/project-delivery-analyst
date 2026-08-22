# Project Delivery Analyst

Version: `v1.3.0`

This repository packages the main delivery-router skill for Codex. It now covers project understanding, PRD and design work, AI workflow gating, OpenSpec / Loops routing, task trace, release preparation, and compliance review.

## What changed in v1.3.0

- Added repository-native workflow routing for batch gates and chain contracts.
- Added explicit OpenSpec / Loops references for bounded execution.
- Rewrote the entry skill to behave like a main router instead of a flat checklist.
- Reworked this README into a release-oriented package guide.

## What it can do

- Turn vague ideas, PRDs, logs, and inherited repos into scoped delivery artifacts.
- Produce PRD, technical plan, database, interface, and frontend/backend closure documents.
- Route AI workflow work through batch isolation, affected-file lists, and evidence labels.
- Produce task trace, release notes, and compliance outputs without expanding scope.

## Routing map

- New idea or unclear scope: `references/project-startup.md`, `references/interview-questions.md`, `references/prd-branch-flow.md`
- Repo understanding: `references/project-understanding.md`
- PRD and delivery docs: `references/prd-template.md`, `references/output-modes.md`, `references/doc-gen-rules.md`
- AI workflow and gates: `references/repository-workflow.md`, `references/ai-constraints.md`, `references/workflow.md`
- OpenSpec and Loops: `references/openspec-loops.md`
- Release: `references/release-checklist.md`, `references/releases-v1.3.0.md`

## Package layout

```text
project-delivery-analyst/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
│   └── validate_project_delivery.py
└── tests/
```

## Validation

Run the built-in structural check:

```bash
python scripts/validate_project_delivery.py --skill-root .
```

This is only the first screen. Keep a human semantic review before treating the skill as ready.

## Release notes

- `v1.3.0`: main-router upgrade, AI workflow routing, OpenSpec / Loops support, README refresh.
- `v1.2.0`: evidence-driven database modeling workflow.

## Installation

Clone the repository into the Codex skill directory you actually use, then reload Codex if needed.

```bash
git clone https://github.com/lxl-go/project-delivery-analyst.git ~/.codex/skills/project-delivery-analyst
```

PowerShell example:

```powershell
git clone https://github.com/lxl-go/project-delivery-analyst.git "$env:USERPROFILE\.codex\skills\project-delivery-analyst"
```

## Authors

Original author: 李小龙 / lxl-go

Collaboration improvements: 张浩宇 / haolihai-zhy

Collaboration repository: https://github.com/zhanghaoyu494-cell/project-delivery-analyst

If you use, modify, or redistribute this skill, keep the original author, repository source, and contributor acknowledgement.

## License

Apache License 2.0

---
name: project-delivery-analyst
description: 项目交付分析、PRD 确认、竞品分析、二次开发项目理解、前后端闭环设计、接口代码级落地指导、AI 约束规则生成、开发/修复门禁、任务追溯、上线前纠偏与合规校验一体化技能。用于从 0-1 新项目想法、二次开发项目 README/代码仓库、工单、PRD、日志、报错、竞品材料中梳理需求，产出 PRD、前端页面布局说明书、前后端闭环说明书、接口功能实现过程指导文档、接口文档、数据库设计、需求分析、技术评审、项目 AI 约束规则、docs/task-trace 任务追溯文档和合规报告。当用户说“梳理需求”“写 PRD”“出技术方案”“数据库设计”“交付文档”“技术评审”“约束规则”“合规校验”“二次开发”“项目画像”“功能修复”“逻辑修复”“接口落地指导”“从想法到项目文档”时使用。
---

# Project Delivery Analyst

## Overview

Use this skill as a combined product manager, full-stack architect, delivery compliance reviewer, and AI development guardrail designer. It merges four strengths:

- Requirements Analyst: clarify vague ideas through conversation, then produce PRD, diagrams, technical plan, and database design.
- DOC-GEN-CHECK style delivery control: split pure business, hybrid requirement, and technical review outputs, enforce red lines, and generate actionable compliance reports.
- Secondary-development analyst: help the user understand an existing project before changing it.
- Development/fix gatekeeper: prevent unbounded scanning, speculative fixes, fake completion, hard-coded implementation, and production-unready code.

## Core Rules

1. Determine the user's current intent and flow weight before producing artifacts: discussion/documentation light flow, read-only analysis medium flow, or development/fix strong flow.
2. If the request starts from a vague idea, interview first. Do not produce formal documents until the user confirms the requirement summary.
3. If the user asks for a single artifact, produce only that artifact. Do not expand into the full chain unless explicitly requested.
4. Keep pure business requirements free of technical implementation terms. Put technical content only in hybrid requirement controlled sections or technical design/review documents.
5. Do not invent project facts, metrics, tools, roles, or workflows. Mark unknown values as "待确认" and include a missing-input checklist.
6. Use Mermaid for all diagrams.
7. Run two review passes for full-chain work: first for document quality and completeness, second for compliance and traceability.
8. Write final artifacts to files when the environment allows it. Use `.draft.md` for drafts and stable names for final deliverables.
9. For development, fixes, or high-risk changes, do not modify code until the current batch, allowed scope, forbidden scope, chain contract, affected files, root cause or implementation plan, and human confirmation are established.
10. For every conclusion, label its evidence state: `文档已确认`, `代码已存在`, `已测试通过`, or `仍未闭环`.

## Workflow Router

Read [workflow.md](references/workflow.md) first for the detailed sequence.

- Project startup, project type classification, or flow-weight selection: read [project-startup.md](references/project-startup.md).
- New idea, unclear scope, or 0-1 project discovery: read [interview-questions.md](references/interview-questions.md), collect context one question at a time, present a summary, and wait for confirmation.
- 0-1 project or secondary-development PRD branch: read [prd-branch-flow.md](references/prd-branch-flow.md).
- Secondary-development project understanding or read-only project portrait: read [project-understanding.md](references/project-understanding.md).
- Interface implementation guide or frontend/backend closed-loop design: read [interface-implementation-guide.md](references/interface-implementation-guide.md).
- AI project constraints, batch gate rules, or development guardrails: read [ai-constraints.md](references/ai-constraints.md).
- Development, feature fix, logic fix, logs, root-cause analysis, or repair flow: read [dev-and-fix-flows.md](references/dev-and-fix-flows.md).
- Task trace documents: read [task-trace-template.md](references/task-trace-template.md).
- Release readiness or上线前纠偏: read [release-checklist.md](references/release-checklist.md).
- Cross-platform installation or using this skill outside Codex: read [cross-platform-adapter.md](references/cross-platform-adapter.md).
- PRD only: read [prd-template.md](references/prd-template.md).
- Diagrams only: read [diagrams-template.md](references/diagrams-template.md).
- Technical plan only: read [tech-plan-template.md](references/tech-plan-template.md).
- Database design only: read [database-template.md](references/database-template.md).
- Pure business, hybrid requirement, technical review, or project rules: read [output-modes.md](references/output-modes.md) and [doc-gen-rules.md](references/doc-gen-rules.md).
- Review or compliance-only: read [review-template.md](references/review-template.md) and [compliance-rules.md](references/compliance-rules.md).

## Standard Artifacts

Discovery and design artifacts:

- `PRD.draft.md` / `PRD.md`
- `diagrams.draft.md` / `diagrams.md`
- `tech-plan.draft.md` / `tech-plan.md`
- `database.draft.md` / `database.md`
- `frontend-layout.md`
- `frontend-backend-closed-loop.md`
- `interface-implementation-guide.md`
- `project-understanding.md`

Delivery and compliance artifacts:

- `business-requirements.md`
- `hybrid-requirements.md`
- `technical-review.md`
- `.dev-rules/rule/` project rule documents
- `project-ai-constraints.md`
- `docs/task-trace/README.md`
- `docs/task-trace/YYYY-MM-DD/task-001-name.md`
- `release-checklist.md`
- `cross-platform-adapter.md`
- `compliance-report.md`
- `review-1.md` and `review-2.md`

## Mode Gate Summary

- Light flow: pure discussion or document generation. Use concise boundary reminders, ask one focused question at a time, and do not scan or modify project code unless requested.
- Medium flow: read-only project analysis or secondary-development understanding. State the read scope first, inspect only that scope, and produce a project portrait or reusable-resource analysis. Do not modify code.
- Strong flow: development, feature fixes, logic fixes, high-risk modules, or code changes. Start with batch isolation, gate table, chain contract, affected-file list, evidence-labeled diagnosis or plan, and wait for human confirmation before editing.

## Validation

For quick structural checks, run:

```bash
python scripts/validate_project_delivery.py --skill-root .
python scripts/validate_project_delivery.py --doc path/to/document.md --mode pure-business
python scripts/validate_project_delivery.py --doc path/to/document.md --mode hybrid
python scripts/validate_project_delivery.py --doc path/to/document.md --mode technical
```

The script is an initial screen only. Always perform a human-quality semantic review after the script passes.

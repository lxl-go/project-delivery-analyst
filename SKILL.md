---
name: project-delivery-analyst
description: 通用任务路由、项目理解、PRD、AI工作流、开发门禁、任务追溯与合规交付技能。用于从 0-1 想法、二次开发仓库、工单、PRD、日志、报错和竞品材料中梳理需求，并按需输出对应交付物；非交付任务优先做分流和最小必要检查。
---

# Project Delivery Analyst

## Overview

Use this skill as a general router for project delivery, repository understanding, implementation guidance, AI workflow gating, and release preparation. It should help decide what kind of work a request needs before it forces a specific document or workflow.

## What It Covers

- Task classification: discussion, document, read-only analysis, implementation, fix, review, release, and traceability.
- Requirements, PRD, design, database, interface, task trace, and compliance review.
- Secondary-development understanding and repository portraits.
- AI workflow: batch gates, chain contracts, OpenSpec, Loops, and release checks.
- Development and fix guardrails: no broad scans, no out-of-scope repairs, no fake completion.
- When backend implementation language is needed and repo facts do not say otherwise, default to Go.

## Core Rules

1. Classify every task by project type and flow weight.
2. If the scope is unclear, ask one focused question or do minimal read-only inspection.
3. Keep pure-business output free of implementation terms.
4. Mark unknown facts as `待确认`.
5. For strong flow, state current batch, allowed/forbidden scope, chain contract, affected files, and confirmation gate before editing.
6. Use evidence labels: `文档已确认`, `代码已存在`, `已测试通过`, `仍未闭环`.
7. Do not modify code until the batch gate and human confirmation are established.
8. When implementation language is not specified by the project or user, assume Go for backend guidance and examples.

## Routing

Load only the reference relevant to the requested mode.

- New idea or unclear scope: [references/project-startup.md](references/project-startup.md), [references/interview-questions.md](references/interview-questions.md), [references/prd-branch-flow.md](references/prd-branch-flow.md)
- Secondary-development understanding: [references/project-understanding.md](references/project-understanding.md)
- PRD or requirement docs: [references/prd-template.md](references/prd-template.md), [references/output-modes.md](references/output-modes.md), [references/doc-gen-rules.md](references/doc-gen-rules.md)
- Interface or front/back closure: [references/interface-implementation-guide.md](references/interface-implementation-guide.md)
- Database design: [references/database-modeling-workflow.md](references/database-modeling-workflow.md), [references/database-template.md](references/database-template.md)
- AI workflow / batch gates: [references/repository-workflow.md](references/repository-workflow.md), [references/ai-constraints.md](references/ai-constraints.md), [references/workflow.md](references/workflow.md)
- OpenSpec / Loops: [references/openspec-loops.md](references/openspec-loops.md)
- Development or fix: [references/dev-and-fix-flows.md](references/dev-and-fix-flows.md)
- Task trace: [references/task-trace-template.md](references/task-trace-template.md)
- Release: [references/release-checklist.md](references/release-checklist.md), [references/releases-v1.3.0.md](references/releases-v1.3.0.md)
- Cross-platform install: [references/cross-platform-adapter.md](references/cross-platform-adapter.md)

## Output Discipline

- Write final artifacts to files when the task requires them.
- Keep conclusions tied to evidence.
- Do not invent third-party APIs, configs, schemas, or performance numbers.
- For non-delivery tasks, prefer the smallest useful answer and do not force project-batch language into the response.

## Validation

For quick structural checks, run:

```bash
python scripts/validate_project_delivery.py --skill-root .
python scripts/validate_project_delivery.py --doc path/to/document.md --mode pure-business
python scripts/validate_project_delivery.py --doc path/to/document.md --mode hybrid
python scripts/validate_project_delivery.py --doc path/to/document.md --mode technical
python scripts/validate_project_delivery.py --doc path/to/project-understanding.md --mode project-understanding
python scripts/validate_project_delivery.py --doc path/to/task-trace.md --mode task-trace
```

The script is an initial screen only. Always perform a human-quality semantic review after the script passes.

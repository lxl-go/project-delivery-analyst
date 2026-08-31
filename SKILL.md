---
name: project-delivery-analyst
description: 通用任务路由、项目理解、PRD、AI工作流、开发门禁、仓库规则工作流包、任务追溯与合规交付技能。用于从 0-1 想法、二次开发仓库、工单、PRD、日志、报错和竞品材料中梳理需求，并按需输出对应交付物；非交付任务优先做分流和最小必要检查。
---

# Project Delivery Analyst

## Overview

Use this skill as a general router for project delivery, repository understanding, implementation guidance, AI workflow gating, and release preparation. It should help decide what kind of work a request needs before it forces a specific document or workflow.

## Operating Layers

Use four layers in order:

1. Entry layer: classify whether the request is question answering, troubleshooting, document writing, code change, planning, review, release, or recap. This layer routes the task; it does not force PRD, batch gates, or chain contracts onto low-risk work.
2. Persona layer: identify the reader or working identity before choosing document depth. Product managers need business requirements and acceptance language; project managers need scope, milestones, risk, and traceability; Go full-stack engineers need technology stack, framework, middleware, API, DTO, database, transaction, idempotency, logging, and test guidance; testers need scenarios, boundaries, exceptions, and regression checks.
3. Evidence layer: treat finalized user-confirmed documents as the source of truth for implementation and review. If document facts, code facts, runtime evidence, or third-party details conflict or are missing, mark the item as `仍未闭环` or ask one focused question instead of inventing facts.
4. Specialty layer: load only the relevant reference for product prototype and interaction documents, PRD, database, interface, release, task trace, OpenSpec/Loops, repository rulepacks, document/code alignment, production code standards, or development/fix gates.

## What It Covers

- Task classification: discussion, document, read-only analysis, implementation, fix, review, release, and traceability.
- Product prototype and interaction requirements documents for app, mini program, and H5 pages.
- Requirements, PRD, design, database, interface, task trace, and compliance review.
- Persona-specific document output for product managers, project managers, Go full-stack engineers, and testing/acceptance readers.
- Standardized deliverables for frontend interaction, PRD, technical design/review, API documents, database table design, AI constraints, and task trace.
- Secondary-development understanding and repository portraits.
- AI workflow: batch gates, chain contracts, OpenSpec, Loops, and release checks.
- Repository rulepack generation: AGENTS.md, aiDoc, workflow, work items, OpenSpec changes, test reports, release plans, learnings, and waivers.
- Development and fix guardrails: no broad scans, no out-of-scope repairs, no fake completion.
- Document-to-code alignment audits: verify whether implementation follows confirmed documents and whether the documented function actually runs.
- Production-readiness gates: prevent single-file fake implementation, architecture bypass, module-boundary bypass, and unverified local-only behavior.
- When backend implementation language is needed and repo facts do not say otherwise, default to Go.

## Core Rules

1. Classify every task by project type and flow weight.
2. If the scope is unclear, ask one focused question or do minimal read-only inspection.
3. Identify the target reader before producing a document. If the user states an identity, use it; if not, infer from the requested artifact and mark the inferred persona.
4. Keep pure-business output free of implementation terms.
5. Mark unknown facts as `待确认`.
6. For strong flow, state current batch, allowed/forbidden scope, chain contract, affected files, and confirmation gate before editing.
7. Use evidence labels: `文档已确认`, `代码已存在`, `已测试通过`, `仍未闭环`.
8. Do not modify code until the batch gate and human confirmation are established.
9. During development and repair, confirmed documents are the primary implementation basis. Code that cannot be traced to the documents must be marked as a gap, not silently accepted.
10. Do not accept one-file, frontend-only, mock-only, or architecture-bypassing implementations as production-ready.
11. When implementation language is not specified by the project or user, assume Go for backend guidance and examples.

## Routing

Load only the reference relevant to the requested mode.

- New idea or unclear scope: [references/project-startup.md](references/project-startup.md), [references/interview-questions.md](references/interview-questions.md), [references/prd-branch-flow.md](references/prd-branch-flow.md)
- Product prototype and interaction doc: [references/prototype-interaction-doc.md](references/prototype-interaction-doc.md)
- Secondary-development understanding: [references/project-understanding.md](references/project-understanding.md)
- PRD or requirement docs: [references/prd-template.md](references/prd-template.md), [references/output-modes.md](references/output-modes.md), [references/doc-gen-rules.md](references/doc-gen-rules.md)
- Interface or front/back closure: [references/interface-implementation-guide.md](references/interface-implementation-guide.md)
- Database design: [references/database-modeling-workflow.md](references/database-modeling-workflow.md), [references/database-template.md](references/database-template.md)
- AI workflow / batch gates: [references/repository-workflow.md](references/repository-workflow.md), [references/ai-constraints.md](references/ai-constraints.md), [references/workflow.md](references/workflow.md)
- Repository rulepack: [references/repository-rulepack.md](references/repository-rulepack.md)
- OpenSpec / Loops: [references/openspec-loops.md](references/openspec-loops.md)
- Development or fix: [references/dev-and-fix-flows.md](references/dev-and-fix-flows.md), [references/production-code-standards.md](references/production-code-standards.md)
- Code follows documents / reverse audit: [references/document-code-alignment.md](references/document-code-alignment.md), [references/production-code-standards.md](references/production-code-standards.md)
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
python scripts/validate_project_delivery.py --doc path/to/prototype.md --mode prototype
python scripts/validate_project_delivery.py --doc path/to/document.md --mode pure-business
python scripts/validate_project_delivery.py --doc path/to/document.md --mode hybrid
python scripts/validate_project_delivery.py --doc path/to/PRD.md --mode prd
python scripts/validate_project_delivery.py --doc path/to/document.md --mode technical
python scripts/validate_project_delivery.py --doc path/to/api.md --mode api
python scripts/validate_project_delivery.py --doc path/to/database.md --mode database
python scripts/validate_project_delivery.py --doc path/to/alignment.md --mode alignment
python scripts/validate_project_delivery.py --doc path/to/project-understanding.md --mode project-understanding
python scripts/validate_project_delivery.py --doc path/to/task-trace.md --mode task-trace
```

The script is an initial screen only. Always perform a human-quality semantic review after the script passes.

# Integrated Workflow

## 1. Classify The Request And Flow Weight

Classify every task by both project type and flow weight.

Project type:

| Type | Meaning |
| --- | --- |
| 0-1 project | New project from idea to delivery documents |
| Secondary development | Existing project, codebase, README, or inherited system |
| Document task | PRD, design, database, interface, review, compliance, or rules only |
| Feature fix | Error, broken button, failed API, page exception, unavailable function |
| Logic fix | Business rule, status flow, permission, or data-display logic mismatch |

Flow weight:

| Weight | Use When | Gate |
| --- | --- | --- |
| Light | Pure discussion or pure document generation | Concise boundary reminder; no code scan unless requested |
| Medium | Read-only project analysis or secondary-development understanding | State the smallest useful read scope before scanning; no code changes |
| Strong | Development, feature fix, logic fix, high-risk change, or any code modification | Batch statement, gate table, chain contract, affected files, human confirmation |

If the user intent is unclear, ask one clarifying question. Safe read-only inspection may continue only when it can resolve ambiguity with project evidence. Do not modify code while the task mode is still unclear.

## 2. Project Startup

Start with [project-startup.md](project-startup.md) when the user is starting a project, preparing development, asking for project rules, or giving an ambiguous request.

General startup chain:

```text
项目启动
-> 判断项目类型：0-1 新项目 / 二次开发 / 文档任务 / 修复任务
-> 判断任务模式：讨论、文档、只读分析、开发、功能修复、逻辑修复
-> 根据风险选择轻流程 / 中流程 / 强流程
-> PRD 需求确认
-> 生成项目专属 AI 约束规则
-> 人工确认
-> 再进入开发或修复
-> 输出验收材料和任务追溯文档
```

## 3. Discovery And PRD Branches

For vague ideas, ask one focused question at a time. Cover business background, target users, roles, core flow, MVP scope, non-functional needs, technical constraints, competitors, and expected outputs.

- For 0-1 projects, read [prd-branch-flow.md](prd-branch-flow.md).
- For secondary development, first ask whether the user understands the project. If not, read [project-understanding.md](project-understanding.md) and run a read-only project portrait using the smallest useful evidence set.
- Present a concise requirement summary and wait for explicit confirmation before writing formal artifacts.

## 4. Draft, Review, Finalize

For full-chain work:

1. Create or update the frontend layout description, frontend/backend closed-loop description, interface implementation guide, PRD draft, diagrams draft, technical plan draft, and database draft as required.
2. Create `review-1.md` using document-quality checks.
3. Ask the user to decide how to handle review issues.
4. Revise drafts according to the user's decisions.
5. Create `review-2.md` using compliance and traceability checks.
6. Finalize stable files only when serious issues are resolved or explicitly accepted by the user.

For single-artifact work, run a focused self-check and deliver only the requested file.

## 5. Development And Fix Gate

For any code modification or high-risk fix, read [dev-and-fix-flows.md](dev-and-fix-flows.md) and [ai-constraints.md](ai-constraints.md). Before editing, output:

1. Current batch and single target.
2. Allowed and forbidden scope.
3. Complete chain contract when frontend/backend/data flow is involved.
4. Affected-file list.
5. Root cause or implementation plan with evidence labels.
6. Human confirmation request.

Do not expand the batch when a scan reveals unrelated issues. Register them as follow-up items only.
Safe diagnosis and read-only inspection do not replace the human confirmation gate for code modification.

## 6. Delivery Standardization

After PRD and technical drafts exist, generate delivery documents as requested:

- Pure business requirement: product/business view only.
- Hybrid requirement: business plus controlled non-functional, technical acceptance, work-order matrix, and service constraints.
- Technical review: architecture, modules, data, APIs, exceptions, performance, risks, traceability.
- Project rules: reusable development constraints under `.dev-rules/rule/` or project-confirmed rule locations.
- Task trace: human-readable and AI-readable records under `docs/task-trace/`.

## 7. Compliance Loop

For compliance-only requests:

1. Identify the document type and baseline materials.
2. Check red-line violations, missing sections, unsupported claims, and traceability gaps.
3. Do not rewrite the original document unless the user asks for remediation.
4. Output specific issue locations and an actionable remediation list.

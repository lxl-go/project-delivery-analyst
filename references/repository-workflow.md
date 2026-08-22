# 仓库原生研发闭环

This reference captures the batch-gate and task-trace behavior that turns the skill into a main router for delivery work.

## 1. Task classification

Classify every request by both project type and flow weight:

- 0-1 project
- Secondary development
- Document task
- Feature fix
- Logic fix

Flow weight:

- Light: pure discussion or pure document generation
- Medium: read-only project analysis or secondary-development understanding
- Strong: development, fix work, high-risk change, or any code modification

If the request is unclear, ask one focused question or do the smallest useful read-only inspection.

## 2. Batch gate

For strong-flow work, do not edit anything until the batch gate is explicit:

- current batch
- allowed scope
- forbidden scope
- core acceptance standard
- chain contract
- affected-file list
- human confirmation

Keep one batch focused on one clear goal. Register unrelated findings as follow-up items only.

## 3. Chain contract

When frontend/backend/data flow is involved, the contract should cover:

- frontend trigger or page entry
- frontend API wrapper
- backend route
- DTOs
- service method
- database impact
- status flow
- transaction, idempotency, and concurrency points
- affected files

## 4. Evidence labels

Use the same four labels across conclusions and task traces:

- `文档已确认`
- `代码已存在`
- `已测试通过`
- `仍未闭环`

Do not present unverified work as complete.

## 5. Task trace and release

Before closing a batch, record:

- modified file list
- self-test commands
- actual results
- known risks
- follow-up items

Release-readiness must stay separate from implementation claims. If the work is not tested, mark it `仍未闭环`.

## 6. When to read

Read this file when the user asks for AI workflow, batch isolation, chain contracts, or repository-native delivery behavior. For deeper stage rules, also read [openspec-loops.md](openspec-loops.md) and [ai-constraints.md](ai-constraints.md).

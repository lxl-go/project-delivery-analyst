# Development And Fix Flows

Use this reference for project development, feature fixes, logic fixes, log analysis, root-cause analysis, and any code modification.

## 1. Development Flow

```text
确认项目是不是二次开发
-> 根据项目生成 AI 约束规则
-> 人工确认约束和本批次范围
-> 进行项目开发
-> 自测验收
-> 写入任务追溯文档
```

Before coding, output:

- Current batch and single goal.
- Allowed modification scope.
- Forbidden modification scope.
- Chain contract.
- Affected-file list.
- Implementation plan.
- Task trace file path under `docs/task-trace/YYYY-MM-DD/`.
- Human confirmation request.

## 2. Feature Fix Flow

Use for errors, failed APIs, broken buttons, page exceptions, and unavailable functions.

```text
读取需求
-> 查看日志
-> 复现问题
-> 定位错误
-> 给出具体详细报错原因
-> 给出解决方案
-> 人工核实确认
-> 修复
-> 自测
-> 输出验收材料
-> 写入任务追溯文档
```

Rules:

- Do not guess when logs, request parameters, response results, or reproduction steps are missing.
- Root cause must map to a concrete file, function, interface, field, config, or data condition.
- Do not fix unrelated issues found during scanning.
- If another issue is strongly related to the current task, label it and include it in the final follow-up list; do not silently expand the fix.
- Verify the real functional closed loop after repair.

## 3. Logic Fix Flow

Use for wrong business rules, status transitions, permissions, or data-display rules.

```text
读取需求
-> 单问题循环追问
-> 需求定稿
-> 核对原有代码和规则
-> 比对差异
-> 给出修复方案
-> 人工核实确认
-> 修复
-> 自测
-> 输出验收材料
-> 写入任务追溯文档
```

Rules:

- Ask one question at a time.
- Confirm the business rule before reading implementation differences.
- Do not change logic before requirement finalization.
- Treat orders, payments, authentication, permissions, and status flows as high risk.

## 4. Acceptance Material

After a development or fix batch, output:

- All modified file paths.
- Complete self-test commands, such as Go unit tests, frontend build, interface tests, and targeted scripts.
- Per-scenario results: normal flow, boundary flow, exception flow, idempotency flow.
- Current uncovered risks.
- Follow-up issues outside the current batch.


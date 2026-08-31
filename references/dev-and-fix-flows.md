# Development And Fix Flows

Use this reference for project development, feature fixes, logic fixes, log analysis, root-cause analysis, and any code modification.

## 0. Diagnose Before Editing

Read-only diagnosis may proceed before a change confirmation gate when it is necessary to establish evidence. Inspect only the target-related code, logs, configuration, requests, responses, data conditions, or reproduction steps.

Root-cause findings must map to concrete evidence such as a file, function, route, field, config, request/response, data condition, log, or reproduction result. If evidence is incomplete, label the conclusion as `仍未闭环` and do not present it as final.

Read-only diagnosis never authorizes editing. Before any code modification, still complete the affected-file list, chain contract when applicable, implementation or repair plan, and human confirmation.

## 1. Development Flow

```text
确认项目是不是二次开发
-> 根据项目生成 AI 约束规则
-> 人工确认约束和本批次范围
-> 对齐已确认文档和代码落点
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
- Document-to-code alignment target.
- Module/service/layer ownership for each planned file.
- Production-readiness checks for permissions, validation, transactions, idempotency, concurrency, logs, exceptions, and performance.
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
- Do not present mock, frontend-only, local-only, or sample behavior as a real fix.
- Do not treat a single-file bypass of established architecture as a real fix.

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
- Treat destructive data operations, schema migrations, production incidents, secrets, third-party callbacks, and irreversible external side effects as high risk.

## 4. Progress State Machine

Use this state machine when a task is looping or not moving:

```text
需求读取
-> 缺口提问
-> 需求定稿
-> 文档/代码依据对齐
-> 方案设计
-> 人工确认
-> 实施
-> 自测
-> 文档同步
-> 任务追溯
-> 交付
```

Rules:

- Each state must have an exit condition.
- If blocked by missing requirement, ask one focused question.
- If blocked by missing logs/runtime evidence, state the exact evidence needed.
- If implementation cannot be traced to a confirmed document, stop and use [document-code-alignment.md](document-code-alignment.md).
- If implementation would bypass module/service boundaries, stop and use [production-code-standards.md](production-code-standards.md).
- Do not keep repeating analysis after the next required evidence or decision is known.

## 5. Acceptance Material

After a development or fix batch, output:

- All modified file paths.
- Document/code alignment result.
- Module/service/layer compliance result.
- Complete self-test commands, such as Go unit tests, frontend build, interface tests, and targeted scripts.
- Per-scenario results: normal flow, boundary flow, exception flow, idempotency flow.
- Current uncovered risks.
- Follow-up issues outside the current batch.

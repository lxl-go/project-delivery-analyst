# Project Startup And Flow Gates

Use this reference when starting a project, classifying a task, generating project AI constraints, or deciding whether the task should use light, medium, or strong flow.

## 1. Startup Classification

Before producing artifacts or touching code, classify the task:

| Dimension | Values |
| --- | --- |
| Project type | 0-1 new project, secondary-development project, document-only task, feature fix, logic fix |
| User intent | Discussion, document generation, read-only analysis, development, repair, compliance review |
| Risk level | Low, medium, high, extreme |
| Required gate | Light, medium, strong |

If classification is unclear, ask one question and wait.

## 2. Flow Weight Rules

Light flow:

- Use for pure discussion, PRD drafting, document generation, diagrams, database design, technical review, and compliance-only requests.
- Output a concise scope reminder.
- Do not scan project code unless the user asks.
- Mark unknowns as `待确认` or `仍未闭环`.

Medium flow:

- Use for README reading, existing-project understanding, architecture analysis, codebase portrait, reusable-resource analysis, and secondary-development planning.
- State the read scope before scanning.
- Read only the agreed scope.
- Do not modify code.
- Output evidence-labeled findings.

Strong flow:

- Use for development, feature fixes, logic fixes, high-risk modules, database changes, permissions, authentication, orders, payments, status flows, production incidents, and any code modification.
- Output the fixed opening sentence if the project rules require it.
- Output the execution gate table, chain contract, affected-file list, and task trace plan.
- Wait for human confirmation before editing.

## 3. Gate Table Template

Use this template for strong flow, and for medium flow when read scope must be controlled:

```markdown
【执行门禁表】
当前批次：
允许修改范围：
禁止修改范围：
本轮核心验收标准：
发现非本批次问题处理规则：仅登记留存，不插入当前批次修复
```

For read-only medium flow, replace "允许修改范围" with "允许读取范围" and explicitly state "禁止修改任何文件".

## 4. Strong Flow Chain Contract

Before code changes, output every applicable item. If an item is not involved, say `不涉及`.

- 前端触发入口/页面按钮
- 前端封装 API 请求方法
- 后端网关/接口路由地址
- 请求入参 DTO 完整结构
- 响应出参 DTO 完整结构
- 后端对应业务服务方法
- 涉及数据库表、新增/修改字段
- 全流程订单/包裹/业务状态流转规则
- 事务、分布式锁、幂等防重设计点位
- 本次改动全部受影响文件清单

## 5. Evidence Labels

Every conclusion must carry one of these labels:

- `文档已确认`: requirements, rules, interfaces, or workflows come from documents or user confirmation.
- `代码已存在`: evidence comes from real code, routes, DTOs, database schemas, or config.
- `已测试通过`: evidence comes from executed commands, interface responses, build results, or reproducible tests.
- `仍未闭环`: information is missing, configuration is absent, reproduction failed, testing was not run, or a statement is only an inference.

## 6. Mandatory Stop Conditions

Stop and ask the user when:

- The project purpose or business process is unknown.
- Third-party API documentation, keys, callback rules, signing rules, SDK usage, or production configuration is missing.
- Database schema or migration rules are missing.
- The error cannot be reproduced.
- Required scope exceeds the current batch.
- The task would modify already verified core logic.
- The user's requested task conflicts with scanned issues.
- Local execution works but release conditions are not met.
- Required information can only be provided by a human.


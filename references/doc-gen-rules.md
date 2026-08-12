# Delivery Document Rules

## Global Red Lines

1. Do not create sections, templates, or validation standards that contradict this skill's output modes.
2. Do not mix implementation details into pure business requirements.
3. Do not add new business requirements in technical review documents.
4. Do not generate extra artifact types when the user requested a single artifact.
5. Do not rewrite document content during compliance-only review.
6. Do not copy competitor behavior wholesale. Mark sources and explain differentiation.
7. When non-compliant, output concrete remediation items.
8. Examples are structure references only; never treat example business content as project facts.
9. If project-level inputs are missing, output a missing-input checklist instead of promising high-completeness system review.
10. Do not treat local mock, sample code, temporary config, or unverified assumptions as production-ready.
11. Do not omit evidence labels for project understanding, development planning, fixes, or technical conclusions.

## Pure Business Requirement Structure

```markdown
# [产品/端/模块] 业务需求分析文档

## 1. 业务总览
## 2. 页面与交互规范
## 3. 功能点清单
## 4. 业务操作流程
## 5. 端到端业务闭环
## 6. 业务约束规则
## 7. 角色权限矩阵
## 8. 数据展示与导出规范
## 9. 定时或周期性业务任务
## 10. 业务联动规则
## 11. 待确认问题
```

## Hybrid Requirement Structure

```markdown
# [产品/端/模块] 混合型需求文档

## 1. 业务背景与目标
## 2. 用户角色与权限
## 3. 功能需求
## 4. 业务流程与异常场景
## 5. 业务约束与验收口径
## 6. 非功能指标
## 7. 技术验收约束
## 8. 工单矩阵
## 9. 服务边界与外部依赖
## 10. 待确认问题
```

## Technical Review Structure

```markdown
# [系统/模块] 技术评审文档

## 1. 评审范围与需求溯源
## 2. 架构总览
## 3. 模块职责与边界
## 4. 核心流程设计
## 5. 数据模型与存储设计
## 6. 接口与集成设计
## 7. 异常、安全、权限与审计
## 8. 性能、容量与稳定性
## 9. 发布、回滚与运维
## 10. 风险清单与应对方案
## 11. 评审结论与待确认问题
```

## Project Rules Suggested Dimensions

Use only dimensions supported by project facts:

- business_logic_rule.md
- architecture_rule.md
- api_rule.md
- database_rule.md
- security_rule.md
- testing_rule.md
- release_rule.md
- cooperation_flow_rule.md

Each rule file should include:

1. Dimension objective.
2. Hard red lines.
3. Recommended practices.
4. Correct and incorrect examples.
5. Self-check list.
6. Source or rationale.

## Document Synchronization Rules

When human review feedback or code changes affect existing artifacts, update all related documents:

- Page impact: update frontend layout description.
- Interface impact: update interface implementation guide and API document.
- Business-flow impact: update frontend/backend closed-loop description.
- Database impact: update database design.
- Technical implementation impact: update technical review.
- Requirement impact: update PRD or requirement analysis.
- Every development/fix task: update `docs/task-trace/YYYY-MM-DD/task-name.md`.

## Status Labels

Use these labels in findings, plans, and acceptance notes:

- `文档已确认`: source is a document or user confirmation.
- `代码已存在`: source is actual code, route, DTO, schema, or config.
- `已测试通过`: source is an executed command, response, build, or test.
- `仍未闭环`: source is missing, untested, unreproduced, not configured, or inferred.

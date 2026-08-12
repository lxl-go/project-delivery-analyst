# Technical Plan Template

Use this for `tech-plan.md`.

```markdown
# 技术方案

## 1. 技术选型总览

| 层级 | 技术选型 | 选择理由 | 约束来源 |
| --- | --- | --- | --- |

## 2. 方案对比

### 方案 A：[名称]
### 方案 B：[名称]

| 维度 | 方案 A | 方案 B | 权重 |
| --- | --- | --- | --- |

推荐方案：[方案名]

推荐理由：
1. ...
2. ...

风险与应对：

| 风险 | 影响 | 应对 |
| --- | --- | --- |

## 3. 架构设计

## 4. 模块设计

| 模块 | 职责 | 输入 | 输出 | 依赖 |
| --- | --- | --- | --- | --- |

## 5. 关键流程设计

## 6. 接口与数据交互说明

## 7. 异常、安全、权限与审计

## 8. 性能、容量与稳定性

## 9. 生产级落地约束

| 约束项 | 设计要求 | 依据 | 状态标签 |
| --- | --- | --- | --- |
| 权限校验 |  |  |  |
| 参数合法性校验 |  |  |  |
| 事务边界 |  |  |  |
| 幂等防重 |  |  |  |
| 并发控制 |  |  |  |
| 异常处理 |  |  |  |
| 日志记录 |  |  |  |
| 性能优化 |  |  |  |
| 第三方失败处理 |  |  |  |

## 10. 本地开发与上线前纠偏

| 项目 | 本地是否临时放宽 | 上线前纠正要求 | 状态标签 |
| --- | --- | --- | --- |

## 11. 排期估算

| 阶段 | 内容 | 工作量 | 风险 |
| --- | --- | --- | --- |

## 12. 待确认问题
```

Rules:

- If there are 2 or more viable approaches, include a comparison matrix.
- Never add business requirements that are absent from PRD or user confirmation.
- Mark assumptions and unknowns clearly.
- Tie non-functional recommendations to business needs.
- For implementation-oriented plans, describe logs, comments for key logic, exception handling, frontend/backend DTO matching, and release correction requirements.

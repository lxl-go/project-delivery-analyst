# Compliance Rules

## Scenario Selection

- Scenario 1: Work orders or confirmed requirements exist. Check traceability against them.
- Scenario 2: Existing project but no work orders. Check consistency with current project materials.
- Scenario 3: No project and no work orders. Check only structural quality, assumptions, and competitor-source boundaries.

## Universal Checks

| Check | Standard |
| --- | --- |
| Scope | Output matches the requested artifact type |
| Completeness | Required sections are present |
| Traceability | Requirements and technical decisions cite source material when available |
| No fabrication | Unknown values are marked as "待确认" |
| Mode separation | Pure business, hybrid, and technical content are separated |
| Testability | Requirements have acceptance criteria or observable outcomes |
| Risks | Technical risks include mitigation |
| Diagrams | Mermaid diagrams render and terminology matches text |

## Pure Business Red-Line Keywords

If these appear in a pure business requirement, flag them unless they are quoted as forbidden examples:

Redis, Kafka, RocketMQ, MySQL, PostgreSQL, MongoDB, Elasticsearch, WebSocket, HTTP, gRPC, API, interface, endpoint, SQL, table, field, index, database, cache, middleware, Docker, Kubernetes, K8s, CI/CD, DDD, Gin, Kratos, Vue, React, QPS, P99, pressure test, distributed lock, message queue, code.

Chinese equivalents to flag:

数据库、数据表、字段、索引、接口、入参、出参、缓存、中间件、消息队列、分布式锁、分库分表、代码、部署、镜像、流水线、压测、服务器、微服务、架构实现。

## Compliance Report Template

```markdown
# 文档合规校验报告

## 1. 校验对象

- 文档：
- 文档类型：
- 校验场景：
- 基准材料：

## 2. 总体结论

- 结论：通过 / 有条件通过 / 不通过
- 严重问题数量：
- 建议问题数量：
- 优化建议数量：

## 3. 问题明细

| 编号 | 严重级别 | 位置 | 问题 | 影响 | 整改建议 |
| --- | --- | --- | --- | --- | --- |

## 4. 缺失输入清单

| 缺失项 | 影响 | 建议补充方式 |
| --- | --- | --- |

## 5. 可落地整改清单

- [ ] ...

## 6. 复检结论

待整改后复检。
```


# Interface Implementation Guide

Use this reference to generate an interface/function implementation guide. This is not a normal API document; it is a code-level frontend/backend closed-loop implementation guide.

## 1. Required Granularity

For each function or interface, document:

- 功能名称
- 用户角色
- 前端页面入口
- 前端按钮 / 表单 / 交互动作
- 前端 API 封装方法
- 前端如何调用后端接口
- 请求 URL、method、headers、token
- 请求 DTO 字段、类型、必填、校验规则
- 响应 DTO 字段、类型、前端使用方式
- 后端路由
- controller 接收逻辑
- service 业务逻辑步骤
- dao / repository 数据访问逻辑
- 涉及数据库表、字段、索引
- 数据新增、修改、查询、删除过程
- 事务边界
- 分布式锁点位
- 幂等防重点位
- 第三方 API 调用点
- 第三方失败后的重试、补偿、降级
- 参数合法性校验
- 权限校验
- 状态流转
- 异常时如何处理
- 功能/接口实现的逻辑顺序步骤
- 并发风险
- 性能优化点
- 日志记录点
- 前端成功、失败、空数据、加载中、重复提交处理
- 功能如何完成前后端闭环验收
- 接口测试命令和联调验证点

## 2. Logic Process Format

Use this structure for implementation logic:

```markdown
### [功能名] 实现过程

1. 前端触发：[页面/按钮/表单]
2. 前端校验：[字段、规则、失败提示]
3. 前端请求：[API 方法、URL、method、DTO]
4. 网关/路由：[路由、权限、中间件]
5. Controller：[绑定参数、基础校验、调用 service]
6. Service：[业务校验、状态判断、事务、幂等、锁、第三方调用]
7. DAO/Repository：[查询、写入、更新、删除、索引要求]
8. 异常处理：[参数、权限、数据不存在、重复提交、第三方失败、数据库失败、并发冲突]
9. 响应返回：[响应 DTO、错误码、错误信息]
10. 前端闭环：[刷新、提示、跳转、状态更新、空态/失败态处理]
11. 验收：[接口测试、页面联调、异常和幂等验证]
```

## 3. Production Readiness

For production-oriented implementation guidance, include:

- Permission checks.
- Parameter legality checks.
- Transaction boundaries.
- Idempotency and duplicate-submit protection.
- Concurrent update protection.
- Error logging and key business logs.
- Database indexes, pagination, filters, and sorting for list endpoints.
- Cache, async task, batch query, or rate-limit suggestions when supported by project facts.
- Large integer ID handling across frontend/backend boundaries.
- Encoding checks for Chinese text.

Mark unsupported performance assumptions as `仍未闭环` instead of inventing QPS or capacity numbers.


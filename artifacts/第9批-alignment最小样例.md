# 文章保存文档倒推代码核验报告

## 1. 核验范围

本次只核验 PRD KB-01 文章保存，不扩展评论、订阅、团队空间和公开分享。核验范围覆盖前端保存入口、前端 API wrapper、后端 Gateway 路由、请求 DTO、响应 DTO、service/domain/RPC、repository/DAO、数据库表、事务与幂等、第三方或中间件依赖、日志 trace 安全规则和测试证据。

## 2. 核验依据

文档已确认：来源为 PRD KB-01、接口文档创建文章、数据库表设计 articles。

代码已存在：只能以实际页面、route、service、DTO、model、migration、config 或测试文件为证据。

已测试通过：只能以命令、真实请求响应、构建日志、数据库读写记录、运行日志或截图为证据。

仍未闭环：没有运行证据、未读取代码、文档冲突或仅靠推断的项保持未闭环。

## 3. 文档到代码对齐矩阵

| Document requirement | Source document and section | Expected code location | Actual code evidence | Runtime evidence | Status label | Gap / action |
| --- | --- | --- | --- | --- | --- | --- |
| 文章编辑页保存文章 | PRD KB-01 / 接口文档 3.1 | pages/article/edit, services/article.ts#createArticle, POST /api/v1/articles, core-rpc.CreateArticle, articles model | 仍未读取代码，不能确认 | 未执行接口测试 | 仍未闭环 | 进入代码核验批次读取页面、service、Gateway、RPC、model、测试 |
| 创建成功返回文章 ID | 接口文档响应 DTO | types CreateArticleResp, frontend rendering | 仍未读取代码，不能确认 | 未执行真实请求 | 仍未闭环 | 补充 API 测试和响应字段断言 |

## 4. 反向链路核验清单

- 前端入口/页面动作：文章编辑页保存按钮，仍未闭环。
- 前端 API wrapper/services：services/article.ts#createArticle，仍未闭环。
- 后端路由/Gateway：POST /api/v1/articles，仍未闭环。
- 请求 DTO：title/content/idempotency_key，仍未闭环。
- 响应 DTO：article_id/status/created_at，仍未闭环。
- Service/domain/RPC：core-rpc.CreateArticle，仍未闭环。
- Repository/DAO/数据库：articles/article_change_logs，仍未闭环。
- 事务、锁、幂等、状态、并发：MySQL 事务、idempotency_key、version，仍未闭环。
- 第三方 API/Redis/MQ/ES/object storage/model：Redis 幂等、MQ/ES 索引补偿，仍未闭环。
- 日志、trace、安全：trace_id、权限过滤、敏感数据脱敏，仍未闭环。
- 测试/live verification：未执行测试和真实请求，仍未闭环。

## 5. 运行证据

未执行测试、构建、接口请求或数据库迁移；所有缺少运行证据的项都标为仍未闭环。后续必须补充具体命令、响应、日志、数据库记录或截图，才能把状态提升为已测试通过。

## 6. 缺口与后续动作

进入下一批次前先确认允许读取文件清单，再读取页面、services、Gateway、RPC、model、migration、test，并执行对应测试。任何文档外实现、未跑通链路或未读取证据都只登记为仍未闭环，不作为完成结论。

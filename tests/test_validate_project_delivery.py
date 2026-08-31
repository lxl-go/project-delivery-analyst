import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_project_delivery.py"
SPEC = importlib.util.spec_from_file_location("validate_project_delivery", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class SkillValidationTests(unittest.TestCase):
    def validate_text(self, text, mode):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "document.md"
            path.write_text(text, encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                return VALIDATOR.analyze_doc(path, mode)

    def test_current_skill_structure_passes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(VALIDATOR.validate_skill(ROOT), 0)

    def test_keyword_only_documents_fail_all_modes(self):
        cases = {
            "pure-business": "# 空文档\n\n业务 角色 功能 流程 约束",
            "hybrid": "# 空文档\n\n业务 角色 功能 流程 验收 非功能",
            "api": "# 空文档\n\n接口 前端 后端",
            "database": "# 空文档\n\n字段 表 索引",
            "prd": "# 空文档\n\n需求 功能 用户",
            "prototype": "# 空文档\n\n页面 交互 跳转",
            "technical": "# 空文档\n\n业务 技术 架构 模块 风险 PRD",
            "project-understanding": "# 空文档\n\n读取范围 项目画像 可复用 目标差异 文档已确认 仍未闭环",
            "task-trace": "# 空文档\n\n当前批次 允许修改范围 禁止修改范围 文档已确认 代码已存在 已测试通过 仍未闭环",
        }
        for mode, text in cases.items():
            with self.subTest(mode=mode):
                self.assertEqual(self.validate_text(text, mode), 1)

    def test_substantive_pure_business_document_passes(self):
        text = """# 售后申请业务需求

## 业务背景与目标
购买者需要在订单完成后提交售后申请，并能持续看到处理进度。目标是减少人工沟通和重复登记。

## 用户角色与权限
购买者可以创建和查看本人申请；客服可以受理、补充说明和给出处理结果；主管可以处理升级事项。

## 功能需求
购买者选择订单、填写原因并提交。系统展示申请编号、当前状态、处理人和更新时间，并避免重复提交。

## 业务流程与异常场景
提交后进入待受理状态。资料不足时退回补充，符合条件时进入处理中，完成后展示结果。订单无效时明确提示原因。

## 业务约束与验收
同一订单的同一商品不能同时存在两条处理中申请。各角色只能执行被授权的操作。正常、退回和拒绝场景都应有可观察结果。

## 待确认问题
退款到账时限由财务规则决定，目前需要业务负责人确认。
"""
        self.assertEqual(self.validate_text(text, "pure-business"), 0)

    def test_unresolved_template_placeholder_fails(self):
        text = """# 技术评审

## 评审范围与需求溯源
来源：PRD-001，覆盖售后提交与状态查询。

## 架构设计
沿用现有分层，复用统一鉴权和错误处理。

## 模块职责与边界
[模块名] 负责接收请求，业务层负责校验状态，存储层负责持久化。

## 核心流程与接口
请求经过权限校验和业务校验后写入记录，并返回可追踪编号。

## 发布与回滚
采用兼容发布；异常时回滚应用版本并停用新入口。

## 风险与应对
重复提交可能产生重复记录，通过业务唯一约束和重复操作检查降低风险。
"""
        self.assertEqual(self.validate_text(text, "technical"), 1)

    def test_project_understanding_requires_hard_labels(self):
        text = """# 项目理解报告

## 读取范围
只读检查 README、路由、接口定义、模型文件和代表性服务实现，不修改任何项目文件。读取范围只覆盖当前目标所需证据，不扫描缓存、构建产物、历史归档和无关模块。

## 项目画像
文档已确认：项目目标来自 README。代码已存在：服务入口和页面入口已经在当前仓库中存在。当前项目采用页面入口调用统一请求封装，再进入服务层校验状态并返回结果的基本结构。

## 可复用内容
代码已存在：可以复用现有请求封装、状态枚举、错误处理和页面组件。复用这些内容可以降低改动范围，避免新增重复 API、重复状态常量和重复展示逻辑。

## 目标差异
文档已确认：本次只处理指定目标，不增加登录、通知、支付或数据库迁移。目标差异集中在状态展示和保存闭环，不改变既有角色权限、页面导航和服务部署方式。

## 闭环状态
仍未闭环：没有运行服务端联调。已测试通过：只读结构检查已经完成。后续如果进入开发批次，需要重新输出允许修改范围、禁止修改范围、影响文件清单和自测命令。
"""
        self.assertEqual(self.validate_text(text, "project-understanding"), 0)

    def test_task_trace_requires_batch_gate_and_hard_labels(self):
        text = """# 增加等待反馈状态

## 任务目标
补齐等待反馈状态，使页面、接口、数据和测试保持一致。目标不是重做工单模块，而是在既有状态模型上增加一个可追踪、可保存、可展示的新状态。

## 当前批次
本批次只处理状态闭环，不扩展其他工单能力。所有发现的通知提醒、权限细化、批量操作和报表统计需求，都不能插入本批次实现。

## 允许修改范围
允许修改服务、页面脚本、样式、测试和本任务追踪文档。允许范围必须能直接解释为等待反馈状态闭环的一部分，不能借机调整目录结构或公共依赖。

## 禁止修改范围
不修改登录、通知、数据库迁移、拖拽排序和其他无关功能。已经验证通过的查询、创建、删除和导出逻辑只作为依赖读取，不做二次改造。

## 本轮核心验收标准
页面可以展示等待反馈状态，接口可以保存并返回该状态，测试覆盖正常和异常场景。

## 发现非本批次问题处理规则
仅登记留存，不插入当前批次修复。

## 计划修改文件
服务文件增加状态校验，页面文件增加筛选和泳道，测试文件固化契约。每个文件改动都必须对应链路中的状态枚举、请求参数、响应展示或验证断言。

## 解决方案
复用既有状态模型，只把等待反馈加入统一枚举、筛选和看板渲染。不新建临时状态字段，不绕过服务端校验，也不使用前端假数据制造完成效果。

## 前后端链路
页面提交状态，服务校验后写入本地数据，再返回工单并刷新泳道。链路验收需要同时观察请求入参、响应状态、页面展示和持久化结果。

## 数据库、第三方、配置影响
不涉及数据库、第三方服务和生产配置，继续使用本地文件存储。

## 文档到代码贴合核验
文档已确认：状态来自需求文档。代码已存在：状态枚举、服务校验和页面展示均有代码落点。已测试通过：单元测试覆盖保存和展示。仍未闭环：接口联调待真实环境确认。

## 模块边界与生产级验收
代码已存在：状态校验位于服务层，页面只负责展示和提交，未出现单文件堆叠或绕过架构。已测试通过：测试覆盖正常、异常和重复提交场景。

## 本地开发临时放宽项
无。

## 上线前必须纠正项
仍未闭环：真实接口环境联调前不能发布。

## 自测命令和结果
已测试通过：执行单元测试和接口验证，测试通过。代码已存在：状态校验位于服务层。

## 未覆盖风险
仍未闭环：本地文件并发写入尚未验证，不属于当前单用户实验声明。

## 非本批次发现问题登记
文档已确认：通知提醒仅登记为范围外事项，不插入当前批次。
"""
        self.assertEqual(self.validate_text(text, "task-trace"), 0)

    def test_task_trace_without_hard_labels_fails(self):
        text = """# 任务追溯

## 当前批次
本批次只处理状态闭环，不扩展其他能力。

## 允许修改范围
允许修改服务和测试。

## 禁止修改范围
不修改通知和登录。

## 本轮核心验收标准
状态链路可以正常保存和展示。

## 发现非本批次问题处理规则
仅登记留存。

## 计划修改文件
服务文件和测试文件。

## 解决方案
增加状态枚举并补充测试。

## 前后端链路
页面请求服务，服务返回状态。

## 自测命令和结果
测试通过。

## 未覆盖风险
并发未验证。
"""
        self.assertEqual(self.validate_text(text, "task-trace"), 1)

    def test_prd_requires_requirement_ids_priorities_and_acceptance(self):
        weak_prd = """# 团队知识库 PRD

## 项目背景
团队需要沉淀知识内容，减少重复沟通。

## 产品定位
面向内部团队的轻量知识库。

## 目标用户
成员、管理员。

## 功能需求
支持创建文章、查看文章和搜索文章。

## 业务规则
成员只能编辑自己的文章。

## 验收标准
功能可用即可。
"""
        self.assertEqual(self.validate_text(weak_prd, "prd"), 1)

        strong_prd = """# 团队知识库需求分析文档 PRD

## 1. 项目背景
团队需要沉淀知识内容，减少重复沟通，并让新人能按分类查找历史经验。

## 2. 产品定位
面向内部团队的轻量知识库，第一版聚焦私有团队空间、文章管理、分类检索和权限控制。

## 3. 目标用户
普通成员负责创建和维护本人文章；管理员负责分类维护、成员权限和异常内容处理。

## 4. 版本范围
第一版要做文章创建、编辑、删除、列表、详情、分类和搜索。第一版不做公开社区、付费空间和多人实时协作。后续迭代再考虑评论和订阅。

## 5. 用户角色与权限
成员只能管理本人文章；管理员可以维护分类和处理异常内容；未登录用户不能进入私有空间。

## 6. 核心业务流程
成员登录后创建文章，选择分类并保存。系统进入列表可见状态，搜索时按标题、摘要和正文匹配本人可见内容。

## 7. 功能模块需求
| 需求ID | 需求描述 | 优先级 | 验收口径 | 备注 |
| --- | --- | --- | --- | --- |
| KB-01 | 支持文章创建 | P0 | 保存后可在本人列表和详情查看 | 第一版必需 |
| KB-02 | 支持文章搜索 | P0 | 输入关键词后返回本人可见文章 | 权限过滤 |

## 8. 业务规则
文章必须归属当前用户或当前团队；删除需要二次确认；分类删除前需要迁移文章。

## 9. 异常场景
未登录时引导登录；无权限访问时提示无权操作；搜索无结果展示空状态。

## 10. 非功能需求
列表查询需要分页；敏感内容不在前端缓存；接口异常时保留用户输入。

## 11. 验收标准
正常创建、边界校验、异常提示、权限隔离和重复提交均有可观察结果。

## 12. 待确认问题
仍未闭环：团队空间成员上限待确认。
"""
        self.assertEqual(self.validate_text(strong_prd, "prd"), 0)

    def test_api_document_requires_full_frontend_backend_contract(self):
        weak_api = """# 接口文档

## 文档边界
描述文章接口。

## 创建文章
POST /articles，传标题和内容，返回成功。
"""
        self.assertEqual(self.validate_text(weak_api, "api"), 1)

        strong_api = """# 团队知识库接口文档

## 1. 文档边界
本文档只覆盖文章创建接口。依据：PRD KB-01、交互文档文章编辑页保存按钮、数据库表设计 articles。

## 2. 通用约定
### 2.1 环境地址
本地 Base URL 为 http://localhost:18080。
### 2.2 请求头
私有接口必须带 Authorization，POST 请求使用 Content-Type: application/json，并透传 X-Trace-Id。
### 2.3 统一响应
| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| code | int | 是 | 0 成功，非 0 失败 |
| message | string | 是 | 前端提示文案 |
| data | object/null | 是 | 业务数据 |
| trace_id | string | 是 | 排障 ID |
### 2.4 通用错误码
参数错误返回 40001，未登录返回 40101，无权限返回 40301，重复提交返回 40901。

## 3. 文章服务接口
### 3.1 创建文章
| 项 | 内容 |
| --- | --- |
| 接口用途 | 保存文章 |
| 依据 | PRD KB-01；数据库表 articles |
| 前端入口 | 文章编辑页保存按钮 |
| 前端调用 | services/article.ts#createArticle |
| 后端路由 | POST /api/v1/articles |
| 是否鉴权 | 是 |
| 后端服务 | Gateway -> core-rpc.CreateArticle |
| 涉及表 | articles、article_change_logs |
| 涉及 Redis/MQ/ES | 删除列表缓存；投递搜索索引任务 |

#### 请求 DTO
| 字段 | 类型 | 必填 | 校验 | 说明 |
| --- | --- | --- | --- | --- |
| title | string | 是 | 1-80 字 | 文章标题 |
| content | string | 是 | 非空 | 正文 |
| idempotency_key | string | 建议 | 非空 | 防重复提交 |

#### 响应 DTO
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| article_id | string | 文章 ID |
| status | string | normal |
| created_at | string | 创建时间 |

## 4. 仍未闭环
仍未闭环：生产域名待部署前确认。
"""
        self.assertEqual(self.validate_text(strong_api, "api"), 0)

    def test_database_document_requires_fields_enums_and_idempotency(self):
        weak_database = """# 数据库表设计

## 文章表
articles 保存文章，有标题和内容。
"""
        self.assertEqual(self.validate_text(weak_database, "database"), 1)

        strong_database = """# 团队知识库数据库表设计文档

## 1. 建模依据
| 材料 | 来源 | 证据状态 | 用途 |
| --- | --- | --- | --- |
| PRD | docs/PRD.md | 文档已确认 | 明确文章创建范围 |
| 接口文档 | docs/API.md | 文档已确认 | 反查请求字段和响应字段 |

## 2. 总体建模结论
第一版按用户私有文章建模，MySQL 作为事实源，搜索索引只做检索加速。

## 3. 主键策略
文章 ID 使用 bigint unsigned 雪花 ID，前端以字符串传输，避免大整数精度丢失。

## 4. 乐观锁策略
文章编辑使用 version 字段控制并发更新。

## 5. 核心关系
users 与 articles 一对多，articles 与 article_change_logs 一对多。

## 6. core-rpc 文章服务
### 6.1 articles
| 字段名 | 类型 | 索引 | 空 | 备注 | 依据 |
| --- | --- | --- | --- | --- | --- |
| id | bigint unsigned | PK | 否 | 雪花 ID | article_id |
| user_id | bigint unsigned | IDX | 否 | 归属用户 | 权限过滤 |
| title | varchar(80) | IDX | 否 | 标题 | 请求 DTO |
| content | mediumtext | FULLTEXT 可选 | 否 | 正文 | 请求 DTO |
| status | varchar(20) | IDX | 否 | normal/deleted | 状态枚举 |
| version | int unsigned | - | 否 | 乐观锁 | 并发编辑 |
| created_at | datetime | IDX | 否 | 创建时间 | 审计 |
| updated_at | datetime | IDX | 否 | 更新时间 | 排序 |

## 7. 表关系清单
| 关系 | 类型 | 说明 |
| --- | --- | --- |
| users -> articles | 一对多 | 一个用户多篇文章 |

## 8. 枚举说明
| 字段 | 枚举 |
| --- | --- |
| articles.status | normal/deleted |

## 9. 事务、幂等与锁
| 场景 | 数据表 | 设计 |
| --- | --- | --- |
| 文章创建 | articles/article_change_logs | MySQL 事务；idempotency_key 防重复提交 |
| 文章编辑 | articles | version 乐观锁 |

## 10. 第一版不建表说明
| 能力 | 不建表原因 |
| --- | --- |
| article_comments | 第一版不做评论 |
"""
        self.assertEqual(self.validate_text(strong_database, "database"), 0)

    def test_prototype_document_requires_page_interaction_contract(self):
        weak_prototype = """# 团队知识库产品原型与交互需求文档

## 项目概述
团队知识库用于保存文章。

## 页面说明
有首页和文章页。

## 交互说明
用户点击保存。
"""
        self.assertEqual(self.validate_text(weak_prototype, "prototype"), 1)

        strong_prototype = """# 团队知识库-小程序端-产品原型 & 交互需求文档

## 1 项目概述
### 1.1 项目背景
团队需要在小程序里沉淀文章和经验，减少重复沟通。
### 1.2 版本目标
第一版包含首页、文章列表页、文章编辑页和我的页，不包含公开社区和付费空间。
### 1.3 目标用户
普通成员创建和查看本人文章；管理员维护分类和处理异常内容。
### 1.4 参考竞品清单
参考轻量笔记、知识库和待办工具，只借鉴页面组织方式，不复制业务内容。

## 2 整体业务流程图
### 2.1 用户主流程
用户登录后进入首页，点击文章入口进入列表，点击新建进入编辑页，保存成功后返回详情或列表。
### 2.2 关键分支流程
未登录时进入登录引导；保存失败时保留表单输入；无权限时提示无权操作。
### 2.3 核心交互闭环流程
文章创建从首页入口开始，经过编辑、保存、列表刷新和详情查看完成闭环。

## 3 页面原型总览
### 3.1 原型链接或访问地址
仍未闭环：原型链接待设计工具确认。
### 3.2 原型操作说明
按底部 Tab 进入首页和我的页，文章列表通过首页卡片进入。
### 3.3 页面清单
首页、文章列表页、文章编辑页、文章详情页、我的页。

## 4 分页面详细需求
### 4.1 首页
#### 页面元素
顶部欢迎语、今日文章数、最近文章、文章入口按钮。
#### 交互规则
点击文章入口进入文章列表；点击最近文章进入详情；下拉刷新重新拉取数据。
#### 异常情况
未登录展示登录引导；无数据展示空状态；网络失败展示重试按钮。
#### 页面跳转去向
文章入口跳转文章列表页，最近文章跳转文章详情页。

### 4.2 文章编辑页
#### 页面元素
标题输入框、正文输入框、分类选择、保存按钮。
#### 交互规则
标题为空时禁止保存；保存中按钮 loading；保存成功返回详情页。
#### 异常情况
接口失败保留输入；重复点击只提交一次；无权限时提示无权操作。
#### 页面跳转去向
保存成功跳转文章详情页，取消返回文章列表页。

## 5 全局通用规则
### 5.1 导航栏与底部 Tab
底部 Tab 包含首页、文章、我的。返回按钮遵循页面栈。
### 5.2 加载、空页面、报错弹窗
列表加载展示骨架屏，空数据展示引导入口，错误弹窗提供重试。
### 5.3 返回按钮通用逻辑
编辑页有未保存内容时返回需要二次确认。

## 6 非功能要求
### 6.1 适配平台
适配微信小程序主流屏幕。
### 6.2 性能要求
列表分页加载，首屏避免阻塞。
### 6.3 弹窗规则
删除和放弃编辑需要二次确认。
### 6.4 可访问性与可用性
按钮文案明确，错误提示贴近对应输入项。

## 7 附录
### 7.1 竞品截图素材包
| 序号 | 页面 | 图片路径 |
| --- | --- | --- |
| 1 | 首页 | docs/prototype-images/home.png |
### 7.2 修改记录
| 日期 | 版本 | 说明 |
| --- | --- | --- |
| 2026-08-31 | v0.1 | 初版交互文档 |
"""
        self.assertEqual(self.validate_text(strong_prototype, "prototype"), 0)

    def test_task_trace_requires_document_code_and_production_sections(self):
        weak_trace = """# 保存文章

## 任务目标
实现文章保存，使页面、接口、数据和测试保持一致。目标不是重做知识库模块，而是在既有文章模型上补齐一个可追踪、可保存、可验证的新功能。

## 当前批次
本批次只做文章保存闭环，不扩展评论、订阅、团队空间和公开分享。

## 允许修改范围
允许修改文章编辑页、前端 API 封装、后端文章服务、文章仓储和本任务测试。

## 禁止修改范围
不修改登录、支付、消息通知、公开社区和团队成员管理。

## 本轮核心验收标准
页面可以提交文章，接口可以保存并返回文章 ID，服务端执行权限和参数校验，测试覆盖正常、异常和重复提交。

## 发现非本批次问题处理规则
仅登记留存，不插入当前批次修复。

## 计划修改文件
文档已确认：文章保存来自 PRD KB-01。代码已存在：文章页面、API 封装、服务层和仓储层均有计划落点。

## 解决方案
复用既有文章模块，只新增保存链路，不把所有逻辑堆到页面或 controller。

## 前后端链路
前端页面触发保存，调用 API 封装，后端 handler 绑定参数，service 校验权限和状态，repository 写入数据库，返回文章 ID 并刷新页面。

## 数据库、第三方、配置影响
文档已确认：涉及 articles 表。仍未闭环：不涉及第三方 API。

## 自测命令和结果
文档已确认：有需求。代码已存在：有接口。已测试通过：测试通过。仍未闭环：线上未测。

## 未覆盖风险
仍未闭环：真实接口环境未联调。

## 非本批次发现问题登记
文档已确认：评论和订阅仅登记为后续事项。
"""
        self.assertEqual(self.validate_text(weak_trace, "task-trace"), 1)

    def test_technical_document_rejects_single_file_fake_implementation(self):
        weak_technical = """# 文章模块技术评审

## 评审范围与需求溯源
来源：PRD KB-01，覆盖文章创建。

## 架构设计与技术选型
使用 Go 和现有 HTTP 服务。

## 模块职责与边界
为了快速通过验收，直接在一个文件中完成页面、接口、业务逻辑和数据库写入。

## 核心流程与接口
前端提交后接口直接写库并返回结果。

## 发布与回滚
异常时回滚应用版本。

## 风险与应对
重复提交通过页面按钮禁用降低风险。
"""
        self.assertEqual(self.validate_text(weak_technical, "technical"), 1)

        strong_technical = """# 文章模块技术评审

## 评审范围与需求溯源
来源：PRD KB-01 和接口文档创建文章接口，覆盖文章创建，不扩展评论、订阅和公开分享。

## 架构设计与技术选型
沿用 Go HTTP Gateway、core-rpc 服务、MySQL 事实源、Redis 幂等缓存和 MQ 异步索引任务。

## 模块职责与边界
前端页面只负责表单和状态展示；前端 service 统一封装 URL、method、headers 和 DTO；Gateway 负责鉴权、参数绑定和 trace ID；core service 负责业务校验、事务和幂等；repository 负责 articles 表写入；adapter 负责 MQ 投递。

## 核心流程与接口
文章编辑页保存按钮调用 services/article.ts#createArticle，经 POST /api/v1/articles 进入 Gateway，再调用 core-rpc.CreateArticle。请求 DTO 包含 title、content、idempotency_key；响应 DTO 返回 article_id、status、created_at。

## 数据模型与存储设计
articles 表保存文章事实，article_change_logs 记录创建审计。创建文章和审计日志在同一 MySQL 事务内提交，idempotency_key 防重复提交。

## 集成与运行验证
接口测试覆盖成功创建、参数错误、未登录、重复提交和 MQ 失败降级。已测试通过：目标单元测试和接口测试通过。

## 发布与回滚
采用兼容发布；异常时回滚应用版本并关闭文章保存入口；MQ 异常时保留主库成功并由任务表补偿。

## 风险与应对
重复提交风险通过 idempotency_key 和唯一约束降低；MQ 失败通过补偿任务应对；真实生产域名仍未闭环，部署前确认。
"""
        self.assertEqual(self.validate_text(strong_technical, "technical"), 0)


if __name__ == "__main__":
    unittest.main()

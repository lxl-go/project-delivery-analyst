# PRD Branch Flow

Use this reference for 0-1 new projects and secondary-development PRD confirmation.

## 1. Shared Question Rule

- Ask one key question at a time.
- Explain briefly why the question matters.
- After the user answers, summarize the answer before asking the next question.
- Do not produce formal documents until the user confirms the requirement summary.
- Mark missing or inferred items as `仍未闭环`; do not invent facts.

## 2. 0-1 New Project Flow

Use when the product starts from an idea or no reusable project exists.

```text
循环追问
-> 确认项目方向
-> 确认项目解决的问题
-> 拆分用户角色
-> 从不同角色角度分析服务内容
-> 找竞品
-> 分析竞品模块、功能、端、技术栈
-> 分析并确认项目的模块、功能、端、技术栈、框架、目录
-> 设计前端页面布局说明书
-> 人工审核调整
-> 生成前后端闭环说明书
-> 生成接口功能实现过程指导文档
-> 人工核查
-> 根据反馈同步更新相关文档
-> 定稿
-> 批量生成接口文档、数据库设计文档、需求分析文档、技术评审文档
-> 根据探讨内容和已有框架生成最终 PRD
```

Minimum question order:

1. 做哪方面的项目？
2. 项目要解决什么问题？
3. 分为哪些角色？
4. 不同角色分别需要什么服务？
5. 是否有参考竞品？
6. 准备用什么端、技术栈、语言、框架？

Technical exploration must cover:

- How many ends are needed.
- Modules in each end.
- Features and interfaces in each module.
- Performance optimization direction.
- Technology stack, language, framework, framework directory.
- Code style, code layers, and coding rules.
- Database modeling inputs: business facts that must be persisted, business objects with independent lifecycles, business actions, state machines, business constraints, query/statistics scenarios, audit requirements, and data lifecycle. Read [database-modeling-workflow.md](database-modeling-workflow.md) before producing `database.md`.

## 3. Secondary Development PRD Flow

Use when there is an existing project, README, framework, codebase, or partial implementation.

Do not force a project portrait at the start. First ask whether the user understands the project and ask them to describe:

- 项目是做什么的
- 业务流程是什么
- 做了哪些端
- 分了哪些模块
- 已经有哪些功能接口
- 代码风格和规范大概是什么
- 当前负责哪个端、角色、模块或任务
- 准备怎么开发

Assess the answer:

- If the user understands the project, proceed to requirement splitting and solution design.
- If the user does not understand the business, flow, ends, modules, interfaces, code style, framework, or directories, run the read-only project portrait in [project-understanding.md](project-understanding.md).

Then continue:

```text
竞品调研
-> 单问题循环追问
-> 拆分需求
-> 判断项目中可复用内容
-> 输出前端页面布局说明书
-> 人工核实调整
-> 输出前后端闭环说明书
-> 输出接口功能实现过程指导文档
-> 人工核查
-> 定稿
-> 生成接口文档、数据库设计文档、需求分析文档、技术评审文档、PRD
```

Requirement splitting must answer:

- Which end is involved.
- Which role is involved.
- Which module is involved.
- Which features or interfaces are required.
- Which existing components, APIs, tables, services, or utilities can be reused.
- Which differences exist between the new requirement and the existing project.
- Which existing tables and fields are reused, extended, or avoided.
- Whether any new table is necessary, and why existing tables cannot safely carry the new business fact.
- Whether any database change affects old data, old APIs, old pages, reports, scheduled jobs, cache, import/export, or migration scripts.
- For database design or database changes, read [database-modeling-workflow.md](database-modeling-workflow.md) before producing `database.md` or DDL guidance.


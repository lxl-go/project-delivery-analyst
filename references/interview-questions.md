# Interview Questions

Ask only the next useful question. For this user's workflow, prefer exactly one key question per turn when requirements are unclear, especially for secondary development and logic fixes.

## Startup

Before detailed questions, classify the task:

- Is this a 0-1 new project, secondary-development project, document task, feature fix, or logic fix?
- Is the user asking for discussion, document generation, read-only analysis, development, repair, or compliance review?
- Does the task require light, medium, or strong flow?

If the user may be working on a secondary-development project, first ask whether they understand the project and ask them to describe it in their own words before scanning code.

## 0-1 New Project Minimum Path

Ask in this order unless the user has already answered:

1. 做哪方面的项目？
2. 项目要解决什么问题？
3. 分为哪些角色？
4. 不同角色分别需要什么服务？
5. 是否有参考竞品？
6. 准备用什么端、技术栈、语言、框架？

## Secondary Development Understanding

Ask the user to describe:

- 项目是做什么的
- 业务流程是什么
- 做了哪些端
- 分了哪些模块
- 已经有哪些功能接口
- 代码风格和规范大概是什么
- 当前负责哪个端、角色、模块或任务
- 准备怎么开发

If the description is incomplete, propose a read-only project portrait instead of directly developing.

## Business

- What problem does this product or feature solve?
- Who is the primary user, and what situation are they in when they need it?
- What is painful or inefficient in the current process?

## Scope

- What must be included in the first version?
- What can wait for a later iteration?
- Are there any features that are explicitly out of scope?

## Roles And Permissions

- What user roles exist?
- What can each role view, create, update, approve, export, or delete?
- Which operations must be restricted?

## Core Flow

- What is the main user journey from start to finish?
- What are the important decision points?
- What abnormal cases must be handled?

## Non-Functional Needs

- Expected user count, peak traffic, or data volume?
- Any target for response time, availability, security, audit, or compliance?
- Any special needs for export, reporting, notification, payment, location, or search?

## Technical Context

- Is there an existing tech stack that must be used?
- Are there existing systems, APIs, tables, or services to reuse?
- Any deployment or environment constraints?

## Competition And References

- Which products or internal systems should be referenced?
- What should be copied as inspiration, and what must be differentiated?

## Output Confirmation

Use this summary format before formal generation:

```markdown
我理解的需求如下，请确认：

【任务模式】
【项目类型】
【产品定位】
【目标用户】
【核心业务流程】
【用户角色与权限】
【MVP 范围】
【非功能需求】
【技术约束】
【流程轻重】
【待确认信息】
【本次输出物】
```

For development or fix tasks, do not proceed from this summary directly into code. Switch to strong flow and output the execution gate table, chain contract, affected-file list, and confirmation request.

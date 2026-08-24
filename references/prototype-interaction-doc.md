# Product Prototype And Interaction Requirements Document

Use this reference when the user wants a page-oriented product prototype and interaction requirements document as the first deliverable, whether the project is 0-1 or secondary development.

This document is both:

- A standalone output when the user only wants the prototype and interaction requirements doc.
- The first input artifact for later PRD, module analysis, feature decomposition, interface design, or implementation planning.

## 1. Purpose

This document freezes page structure, navigation, interaction behavior, shared rules, and the visible user journey before deeper analysis begins. It is especially important for app, mini program, and H5 projects.

Use it to answer:

- What pages exist?
- What does each page contain?
- How do users move between pages?
- What happens on success, failure, empty state, or network error?
- What global rules apply across all pages?

If project facts are missing, mark them as `待确认` instead of inventing product, design, or flow details.

## 2. When To Use

Use this reference when:

- The user asks for a product prototype and interaction requirements document.
- A page-based project must produce a prototype before PRD or module analysis.
- The user wants only this document and nothing else.
- A secondary-development project needs to record the current UI and interaction baseline before refactoring.

Do not use it for backend-only work, API-only work, or simple text-only requirements unless the task includes page structure or interaction behavior.

## 3. Recommended Document Title

Use a title in this form:

`XX(名称)-X端-APP/小程序/H5/... 产品原型 & 交互需求文档`

Adjust `X端` and channel names to match the real product. Keep the naming consistent within the repo.

## 4. Required Outline

Generate the document with these sections in order:

### 1 项目概述

Include:

- 1.1 项目背景
- 1.2 版本目标（要做哪些功能、哪些暂时不做）
- 1.3 目标用户
- 1.4 参考竞品清单（截图参考的 APP / 小程序 / H5 名字）

### 2 整体业务流程图

Include:

- 2.1 用户主流程
- 2.2 关键分支流程（异常、弹窗、失败提示）

### 3 页面原型总览

Include:

- 原型链接或访问地址
- 原型操作说明
- 页面清单：全部页面名称列表

### 4 分页面详细需求

For each page, include:

- 页面原型截图或原型页引用
- 页面元素
- 交互规则
- 异常情况
- 页面跳转去向

### 5 全局通用规则

Include:

- 导航栏、底部 tab 栏
- 加载动画、空页面、报错弹窗样式
- 返回按钮通用逻辑

### 6 非功能要求

Include:

- 适配平台
- 性能
- 弹窗规则

### 7 附录

Include:

- 竞品截图素材包
- 修改记录

## 5. Writing Rules

- Keep the document page-first, not backend-first.
- Separate visible UI behavior from deeper module analysis.
- Write the interaction flow in explicit trigger -> condition -> result form.
- List page-level states and transitions.
- Use the document as the source for later PRD and module decomposition.

## 6. Output Expectations

When generating this document, produce:

- A clear title.
- A page list.
- A flow summary.
- Per-page interaction details.
- Global rules.
- Non-functional constraints.
- An appendix block for assets and revisions.

If the user only wants this document, stop here and do not expand into PRD or implementation unless asked.

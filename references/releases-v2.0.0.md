# v2.0.0 发布公告

## 版本概述

本版本将 `project-delivery-analyst` 从项目交付工作流路由 Skill 升级为更严格的项目文档与代码核验 Skill。重点补齐身份分流、标准化交付文档、AI 执行门禁、文档作为实现依据、有界推进、文档倒推代码核验和生产级实现约束。

## 新增能力

- 身份分流：支持按产品经理、项目经理、Go 全栈工程师、测试/验收人员等不同视角输出对应深度的文档。
- 五类标准交付文档：覆盖产品原型与交互需求文档、需求分析文档 PRD、技术方案/技术评审、接口文档、数据库表设计文档。
- AI 约束规则生成：强化批次门禁、链路契约、影响文件清单、证据标签和非本批次问题登记。
- 文档作为实现依据：开发、修复和评审必须优先追溯到已确认文档，缺少证据时标记 `仍未闭环`。
- 文档倒推代码核验：从交互文档、PRD、技术方案、接口文档和数据库设计反查代码是否真正贴合。
- `alignment` 校验模式：新增 `scripts/validate_project_delivery.py --mode alignment`。
- 运行证据闭环规则：缺少运行证据的矩阵行必须保持 `仍未闭环`，不能声称完成、验收通过或生产可用。
- 生产级实现门禁：拒绝单文件堆逻辑、前端假效果、mock-only、绕过模块边界和未测试却声称完成。

## 校验方式

可运行以下命令检查 Skill 结构、单元测试和文档倒推代码核验样例：

```bash
python scripts/validate_project_delivery.py --skill-root .
python tests/test_validate_project_delivery.py
python scripts/validate_project_delivery.py --doc artifacts/第9批-alignment最小样例.md --mode alignment
```

## 兼容性

- Skill 名称不变。
- 调用方式不变。
- 原有 PRD、prototype、technical、api、database、project-understanding、task-trace 校验模式继续可用。
- v1.3.0 已有的仓库工作流、OpenSpec / Loops、有界执行规则继续保留。

## 状态标签

所有交付、开发、修复、核验结论都应明确区分：

- `文档已确认`
- `代码已存在`
- `已测试通过`
- `仍未闭环`

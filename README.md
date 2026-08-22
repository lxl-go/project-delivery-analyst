# Project Delivery Analyst

版本：`v1.3.0`

这是一个面向 Codex 的项目交付主控 Skill。它覆盖项目理解、PRD 与设计、AI 工作流门禁、OpenSpec / Loops 路由、任务追溯、发布准备和合规校验。

## v1.3.0 更新内容

- 新增仓库原生工作流路由，支持批次门禁和链路契约。
- 新增 OpenSpec / Loops 引用，用于有界 AI 执行。
- 重写入口 Skill，使其从扁平清单升级为主控路由器。
- 重写 README，使其更适合作为发布版使用说明。

## 能做什么

- 将模糊想法、PRD、日志和二次开发仓库梳理成边界清晰的交付材料。
- 生成 PRD、技术方案、数据库设计、接口说明和前后端闭环文档。
- 将 AI 工作流纳入批次隔离、影响文件清单和证据标签。
- 在不扩大范围的前提下，输出任务追溯、发布说明和合规校验结果。

## 路由说明

- 新项目想法或范围不清：`references/project-startup.md`、`references/interview-questions.md`、`references/prd-branch-flow.md`
- 二次开发项目理解：`references/project-understanding.md`
- PRD 与交付文档：`references/prd-template.md`、`references/output-modes.md`、`references/doc-gen-rules.md`
- AI 工作流和门禁：`references/repository-workflow.md`、`references/ai-constraints.md`、`references/workflow.md`
- OpenSpec 和 Loops：`references/openspec-loops.md`
- 发布准备：`references/release-checklist.md`、`references/releases-v1.3.0.md`

## 目录结构

```text
project-delivery-analyst/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
├── scripts/
│   └── validate_project_delivery.py
└── tests/
```

## 校验

运行内置结构校验：

```bash
python scripts/validate_project_delivery.py --skill-root .
```

该脚本只做第一层结构筛查。正式发布或交付前，仍需要人工做语义复核。

## 发布说明

- `v1.3.0`：主控路由升级、AI 工作流路由、OpenSpec / Loops 支持、README 重写。
- `v1.2.0`：证据驱动的数据库建模工作流。

## 安装方式

将仓库克隆到你实际使用的 Codex skill 目录中。如 Codex 未自动识别变更，可重启 Codex。

```bash
git clone https://github.com/lxl-go/project-delivery-analyst.git ~/.codex/skills/project-delivery-analyst
```

PowerShell 示例：

```powershell
git clone https://github.com/lxl-go/project-delivery-analyst.git "$env:USERPROFILE\.codex\skills\project-delivery-analyst"
```

## 作者

原作者：李小龙 / lxl-go

协作改进：张浩宇 / haolihai-zhy

协作仓库：https://github.com/zhanghaoyu494-cell/project-delivery-analyst

如果你使用、修改或二次发布这个 Skill，请保留原作者信息、仓库来源和贡献者致谢。

## 许可证

Apache License 2.0

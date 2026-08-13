# Project Delivery Analyst

面向 Codex / AI 编程助手的项目交付分析 Skill，适合用来做需求梳理、PRD、技术方案、数据库设计、接口落地指导、AI 开发约束、任务追溯、上线前检查和合规校验。

## 能做什么

- 从项目想法、PRD、工单、日志、竞品材料中梳理需求。
- 分析二次开发项目，输出项目画像和可复用资源说明。
- 生成 PRD、技术方案、数据库设计、接口文档和前后端闭环说明。
- 生成 AI 开发约束规则、批次门禁、任务追溯文档和上线前检查清单。
- 对业务需求、混合需求、技术评审和交付文档做合规校验。

## 适用场景

当你希望 Codex 或其他 AI 编程助手处理下面这些任务时，可以使用这个 Skill：

- 梳理需求、写 PRD、出技术方案、做数据库设计。
- 做二次开发项目理解、项目画像、接口落地指导。
- 制定开发约束规则、修复门禁、批次隔离规则。
- 生成任务追溯、上线前检查、合规校验报告。

## 安装方式

个人级安装推荐克隆到 Codex 当前支持的用户 skills 目录：

```bash
git clone https://github.com/lxl-go/project-delivery-analyst.git ~/.agents/skills/project-delivery-analyst
```

Windows PowerShell 示例：

```powershell
git clone https://github.com/lxl-go/project-delivery-analyst.git "$env:USERPROFILE\.agents\skills\project-delivery-analyst"
```

仓库级使用时，也可以放到项目的 `.agents/skills/project-delivery-analyst/`。已有环境如果仍从 `~/.codex/skills/` 加载，本仓库也保持兼容，但新安装优先使用 `.agents/skills`。

Codex 通常会自动发现 skill 变更；如果没有显示，再重启 Codex。

## 目录结构

```text
project-delivery-analyst/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── ai-constraints.md
│   ├── prd-template.md
│   ├── tech-plan-template.md
│   └── ...
└── scripts/
    └── validate_project_delivery.py
```

## 校验

可以运行内置校验脚本做基础结构检查：

```bash
python scripts/validate_project_delivery.py --skill-root .
```

脚本只做初步结构筛查，正式交付前仍需要人工语义复核。

## 作者

Original author: 李小龙 / lxl-go

如果你使用、修改或二次发布这个 Skill，请保留原作者信息和本仓库来源。

## License

Apache License 2.0

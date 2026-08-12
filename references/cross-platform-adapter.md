# Cross-Platform Adapter

Use this reference when a user wants to install, migrate, or use this skill outside Codex.

## 1. Important Limit

This folder is a Codex skill. Other AI platforms may not support Codex's native skill discovery, `agents/openai.yaml`, or automatic reference routing.

When running outside Codex, adapt the skill into that platform's rule system. If the platform cannot persist rules, load the skill for the current conversation only.

## 2. Universal Loading Order

For any platform:

1. Read `SKILL.md`.
2. Read this file: `references/cross-platform-adapter.md`.
3. Read `references/workflow.md`.
4. For the specific task, read only the relevant reference files named by `SKILL.md`.
5. Follow the same evidence labels, gate rules, task trace rules, and stop conditions.

## 3. Universal Install Prompt

Use this prompt in other AI platforms:

```text
请解压并读取这个 project-delivery-analyst skill。
先读取 SKILL.md，再读取 references/cross-platform-adapter.md。
根据你当前平台的规则系统，把这个 skill 转换成可长期生效的项目规则。
如果当前平台不支持持久安装，请告诉我限制，并给出本会话可用的加载方式。
安装或适配后，所有项目需求、PRD、二次开发、功能修复、逻辑修复、接口落地指导、AI 约束规则和上线前纠偏任务，都必须按这个 skill 的流程执行。
```

## 4. Platform Mapping

### Codex

Use native skill format:

```text
~/.codex/skills/project-delivery-analyst/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

If the skill was copied while Codex was already running, open a new task or restart Codex if the new description is not visible.

### Claude Code

Claude Code does not natively install Codex skills as skills. Convert the rules into `CLAUDE.md`.

Recommended action:

- Put the full `SKILL.md` summary and the key rules from `references/workflow.md`, `references/project-startup.md`, `references/ai-constraints.md`, and `references/dev-and-fix-flows.md` into project-level `CLAUDE.md`.
- Keep the original `references/` folder in the project or a docs/rules directory.
- Add a line in `CLAUDE.md`: "When project-delivery-analyst references are available, read the relevant reference before acting."

### Cursor

Cursor does not natively install Codex skills as skills. Convert the rules into Cursor rules.

Recommended action:

```text
.cursor/rules/project-delivery-analyst.mdc
.cursor/rules/project-delivery-ai-constraints.mdc
.cursor/rules/project-delivery-dev-fix-gates.mdc
```

Use `SKILL.md` as the main router. Put the high-risk development and fix rules in always-on or project rules according to Cursor's current rule system.

### Windsurf

Windsurf does not natively install Codex skills as skills. Convert the core rules into:

```text
.windsurfrules
```

Keep detailed references in a visible folder such as `docs/ai-rules/project-delivery-analyst/`.

### Generic ChatGPT, Claude, Gemini, or Web AI

If the platform supports file upload or project knowledge:

- Upload the zip or the extracted `project-delivery-analyst/` folder.
- Ask it to read `SKILL.md` first.
- Ask it to use the universal install prompt above.

If the platform does not support persistent project knowledge, the skill is only available for the current conversation.

### Custom Agent Or Local AI

Map files as follows:

| Codex skill file | Generic agent role |
| --- | --- |
| `SKILL.md` | Main system/developer instruction or router |
| `references/workflow.md` | Workflow controller |
| `references/project-startup.md` | Startup classifier and gate rules |
| `references/ai-constraints.md` | Development guardrails |
| `references/dev-and-fix-flows.md` | Development/fix procedure |
| `references/interface-implementation-guide.md` | Interface implementation template |
| `references/task-trace-template.md` | Traceability artifact template |
| `references/release-checklist.md` | Release readiness checklist |

## 5. Reinstall Or Update Rules

- Codex: reinstall or copy the updated skill folder when moving to another machine or Codex environment.
- Claude Code, Cursor, Windsurf: update their rule files. This is not a native skill install.
- Web AI: re-upload or update project knowledge when starting a new workspace or conversation.
- Any platform that previously loaded an older version must replace it with the newer files; otherwise it will continue using old behavior.

## 6. Compatibility Self-Check

After adapting to another platform, ask the AI to answer:

```text
请确认你已经加载 project-delivery-analyst，并列出：
1. 当前平台是否支持持久规则；
2. 你把 SKILL.md 映射到了哪里；
3. 你把 references/ 映射到了哪里；
4. 开发/修复任务是否会强制输出门禁表、链路契约清单、影响文件清单；
5. 缺第三方资料、缺日志、缺数据库结构时是否会停止并询问我。
```

If it cannot answer these points clearly, treat the adaptation as `仍未闭环`.


# Task Trace Template

Use this reference for development and repair traceability. The trace directory must be human-readable and AI-readable.

## 1. Directory

Use:

```text
docs/task-trace/
```

Structure:

```text
docs/task-trace/
  README.md
  2026-08-10/
    task-001-xxx.md
    task-002-xxx.md
  2026-08-11/
    task-001-xxx.md
```

Do not use hidden directories for the primary trace record unless the user requests it.

## 2. Task File Template

```markdown
# [任务名称]

## 1. 任务目标

## 2. 当前批次

## 3. 允许修改范围

## 4. 禁止修改范围

## 5. 计划修改文件

| 文件 | 修改原因 | 解决的问题 | 状态标签 |
| --- | --- | --- | --- |

## 6. 解决方案

## 7. 前后端链路

## 8. 数据库、第三方、配置影响

## 9. 本地开发临时放宽项

## 10. 上线前必须纠正项

## 11. 自测命令和结果

## 12. 未覆盖风险

## 13. 非本批次发现问题登记
```

## 3. Update Rule

- Create or update a trace file before implementation planning becomes code modification.
- Complete the test and risk sections after verification.
- If no test was run, write `仍未闭环：未执行测试` instead of implying completion.
- Keep one trace file per development or repair task.


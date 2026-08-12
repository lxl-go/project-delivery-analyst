# Diagrams Template

All diagrams must be Mermaid code blocks.

## Required Diagrams

Use these when relevant:

- Mindmap: product function overview.
- Flowchart: user operation or business process.
- Sequence diagram: component or service interaction.
- Architecture diagram: system layers and dependencies.
- State diagram: orders, approvals, tickets, workflows.
- ER diagram: database entities, placed in `database.md` when possible.

## File Structure

````markdown
# [需求名称] 图表文档

## 图1：功能全貌思维导图

一句话说明。

```mermaid
mindmap
  root((产品名称))
```

## 图2：核心业务流程图

```mermaid
flowchart TD
    A([开始]) --> B[用户执行操作]
    B --> C{是否满足条件?}
    C -- 是 --> D[继续]
    C -- 否 --> E[提示原因]
    D --> F([结束])
    E --> F
```

## 图3：核心时序图

```mermaid
sequenceDiagram
    autonumber
    actor 用户
    participant 前端
    participant 服务端
    participant 数据库
    用户->>前端: 发起操作
    前端->>服务端: 提交请求
    服务端->>数据库: 保存数据
    数据库-->>服务端: 返回结果
    服务端-->>前端: 返回响应
    前端-->>用户: 展示结果
```

## 图4：技术架构图

```mermaid
flowchart TB
    subgraph 客户端
        WEB[Web/移动端]
    end
    subgraph 服务端
        API[接入层]
        SVC[业务服务]
        DB[(数据库)]
    end
    WEB --> API --> SVC --> DB
```
````

## Diagram Checks

- Each flowchart has start and end nodes.
- Decision nodes have at least two exits.
- Sequence diagrams use `autonumber`.
- Architecture diagrams group client, server, data, and external dependencies when applicable.
- Diagram names match terminology used in PRD and technical plan.


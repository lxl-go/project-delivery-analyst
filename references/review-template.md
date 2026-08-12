# Review Template

Use `review-1.md` for document-quality review and `review-2.md` for compliance and traceability review.

```markdown
# [需求名称] 第 N 轮自我评审报告

> 评审时间：YYYY-MM-DD HH:MM
> 评审轮次：第 N 轮
> 评审对象：

## 1. 评审总结

| 严重级别 | 问题数量 | 说明 |
| --- | --- | --- |
| 严重 | N | 影响完整性、准确性或合规性 |
| 建议 | N | 影响可读性、专业度或可测试性 |
| 优化 | N | 可选增强 |

整体结论：通过 / 需要修改后再评审

## 2. 问题明细

### 严重问题

#### S-1

- 位置：
- 描述：
- 影响：
- 建议方案 A：
- 建议方案 B：
- 用户决策：待确认

### 建议问题

#### W-1

- 位置：
- 描述：
- 建议：
- 用户决策：待确认

### 优化建议

#### O-1

- 位置：
- 描述：
- 建议：
- 用户决策：待确认

## 3. 各文件评审详情

### PRD
### diagrams
### tech-plan
### database
### business-requirements
### hybrid-requirements
### technical-review
### project rules
```

## Review Pass 1: Document Quality

- Clear business background.
- Target users and roles are specific.
- MVP and later iterations are separated.
- Requirements are testable.
- Diagrams match text.
- Technical plan includes choices, trade-offs, risks, and estimates.
- Database design covers core entities and indexes.

## Review Pass 2: Compliance And Traceability

- Pure business documents contain no technical implementation terms.
- Hybrid documents keep technical content in allowed sections.
- Technical review does not invent business requirements.
- Important decisions trace back to PRD, work orders, or user confirmation.
- Missing information is listed, not silently invented.
- Remediation list is concrete.


# Release Correction Checklist

Use this reference before claiming a development or fix task is release-ready.

## 1. Local Temporary Items

Check whether any local-only items remain:

- Mock data.
- Test configuration.
- Temporary switches.
- Temporary logs.
- Relaxed validation.
- Hard-coded URLs, tokens, roles, status values, or config.

If any remain, mark the task as `仍未闭环` for release readiness and tell the user what must be corrected.

## 2. Production Readiness

Check:

- Permission verification.
- Parameter legality checks.
- Transaction boundaries.
- Idempotency and duplicate-submit protection.
- Concurrency control.
- Error handling and rollback.
- Key business logs and exception logs.
- Pagination, filtering, sorting, indexes, cache, and batch query needs.
- Third-party production config, callback, signature, retry, compensation, and degradation.
- Chinese encoding.
- Large integer ID transfer safety.
- Real frontend/backend interface closure.

## 3. Output

Use this format:

```markdown
【上线前纠偏清单】
- 已满足：
- 仍未闭环：
- 需要人工提供：
- 建议上线前阻断项：
```


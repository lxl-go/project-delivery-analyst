# v2.0.0 Release Notes

## Summary

This release upgrades `project-delivery-analyst` from a delivery workflow router into a stricter project-document and implementation-alignment skill. It addresses persona-specific documents, standardized deliverables, AI execution gates, document-as-source-of-truth behavior, bounded task progress, and production-grade implementation checks.

## Added

- Persona routing for product managers, project managers, Go full-stack engineers, and testing or acceptance readers.
- Standardized output coverage for product prototype and interaction documents, PRD, technical review, API documents, and database table design.
- Stronger AI constraint generation with batch gates, chain contracts, affected-file lists, evidence labels, and out-of-batch issue registration.
- Document-to-code alignment workflow for checking whether implementation follows confirmed documents and whether the feature actually runs.
- `alignment` validation mode in `scripts/validate_project_delivery.py`.
- Runtime evidence closure rule: rows without runtime evidence must remain marked `仍未闭环`.
- Production-grade implementation gate against single-file fake implementation, frontend-only effects, mock-only delivery, architecture bypass, and unverified completion claims.

## Validation

Run the standard checks:

```bash
python scripts/validate_project_delivery.py --skill-root .
python tests/test_validate_project_delivery.py
python scripts/validate_project_delivery.py --doc artifacts/第9批-alignment最小样例.md --mode alignment
```

## Compatibility

- Skill name unchanged.
- Invocation unchanged.
- Existing PRD, prototype, technical, API, database, project-understanding, and task-trace modes remain available.
- Existing v1.3.0 repository workflow and OpenSpec / Loops references remain available.

## Status Labels

All delivery and alignment conclusions should distinguish:

- `文档已确认`
- `代码已存在`
- `已测试通过`
- `仍未闭环`

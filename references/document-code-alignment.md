# Document Code Alignment

Use this reference when the user asks whether code matches confirmed documents, whether a delivered function really works, or whether implementation should be driven strictly by PRD, interaction, API, database, or technical design documents.

## 1. Source Priority

Use this evidence order:

1. User-confirmed requirement or latest explicit instruction.
2. Confirmed project documents: interaction document, PRD, technical design/review, API document, database design, task trace.
3. Existing code, route, DTO, schema, config, migration, or tests.
4. Runtime evidence: logs, real request/response, build output, unit/integration tests, screenshots, database records.
5. Inference.

Items from inference must be marked `仍未闭环`. Do not promote inference into requirements, API fields, schema, middleware, third-party behavior, or acceptance evidence.

## 2. Alignment Matrix

When auditing code against documents, produce a matrix with these fields:

| Document requirement | Source document and section | Expected code location | Actual code evidence | Runtime evidence | Status label | Gap / action |
| --- | --- | --- | --- | --- | --- | --- |

Status labels:

- `文档已确认`: the requirement is present in a confirmed document or user instruction.
- `代码已存在`: route, method, DTO, schema, service, config, or test exists.
- `已测试通过`: a command, request, build, or live check proves behavior.
- `仍未闭环`: missing, untested, inferred, contradictory, or local-only.

## 3. Required Reverse Checks

For frontend/backend features, verify these links in order:

1. Page or user action from the interaction document.
2. PRD requirement ID or business rule.
3. Frontend route/page/component and event handler.
4. Frontend API wrapper method.
5. HTTP route or gateway endpoint.
6. Request DTO fields, types, required flags, and validation.
7. Response DTO fields and frontend rendering usage.
8. Backend controller/handler.
9. Service/domain method and business rule enforcement.
10. Repository/DAO and database tables.
11. Transaction, lock, idempotency, status flow, and concurrency handling.
12. Third-party API, middleware, cache, MQ, ES, object storage, or model provider usage.
13. Error handling, logging, trace ID, and security masking.
14. Tests or live verification.

If any required link is missing, stop claiming full closure and report the exact missing link.

## 4. Document Drift Handling

If code differs from documents:

- If the user gave a newer explicit requirement, mark the older document as needing synchronization.
- If documents conflict with each other, list the conflict and ask one focused question.
- If code implements behavior not found in documents, mark it as undocumented implementation and do not expand the requirement silently.
- If documents specify behavior but code lacks it, mark it as an implementation gap.
- If code is present but not runnable or not tested, mark it as `仍未闭环`.

## 5. Runtime Closure

Document/code alignment is not complete until there is runtime evidence appropriate to the change:

- Frontend: build plus route/page interaction check.
- Backend: targeted unit or integration test.
- API: real request with expected method, URL, headers, parameters, response, and error handling.
- Database: migration/schema check and data read/write evidence when relevant.
- Third-party: sandbox/live documented response or a clearly marked unverified dependency.

Build success alone does not prove business closure. Code existence alone does not prove runtime behavior.

## 6. Alignment Validation Mode

When a document is meant to be checked by `validate_project_delivery.py --mode alignment`, it must contain:

- A clear audit scope that limits the document-to-code check to the confirmed batch or feature.
- A source/evidence section using all four hard labels: `文档已确认`, `代码已存在`, `已测试通过`, `仍未闭环`.
- An alignment matrix with document requirement, source document and section, expected code location, actual code evidence, runtime evidence, status label, and gap/action.
- A reverse-chain checklist covering frontend entry, frontend API wrapper, backend route or gateway, request DTO, response DTO, service/domain/RPC, repository/DAO/database, transaction/lock/idempotency/status/concurrency, third-party or middleware dependencies, logging/trace/security, and tests or live verification.
- A runtime evidence section that names the exact command, request, log, database check, build, screenshot, or other proof used for closure.
- A gap/action section for every missing, inferred, unread, untested, or contradictory item.

Any matrix row that lacks runtime evidence must be marked `仍未闭环`. Do not mark a row as complete, production-ready, accepted, or fully closed when the runtime evidence column says no test was executed, no request was made, or the behavior was only inferred.

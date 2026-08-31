# Production Code Standards

Use this reference for development plans, code reviews, implementation audits, and fix verification when the user expects enterprise-grade, market-grade, or production-grade output.

## 1. Production-Ready Definition

A feature is production-ready only when it is implemented through the project's intended layers and has evidence for behavior, failure handling, and operational safety.

Minimum required dimensions:

- Requirement traceability.
- Module and service boundary compliance.
- Frontend/backend/API/database closure.
- Permission and ownership checks.
- Parameter validation.
- Transaction boundaries.
- Idempotency and duplicate-submit protection.
- Concurrency control.
- Status and lifecycle consistency.
- Error handling and user feedback.
- Business logs, trace IDs, and sensitive-data masking.
- Third-party timeout, retry, compensation, or degradation.
- Tests and runtime verification.

## 2. Module Boundary Gate

Do not mark a change production-ready when it:

- Implements an entire business flow in one oversized file when the project already has pages, services, controllers, domain services, repositories, RPC services, or adapters.
- Bypasses an existing module, microservice, RPC, gateway, repository, middleware, or shared API wrapper without documented reason.
- Places business rules in UI code when backend/domain enforcement is required.
- Places database logic in controllers or page handlers when the project has DAO/repository layers.
- Hard-codes config, URLs, providers, status values, prompts, or secrets instead of using existing config paths.
- Adds mock, sample, local-only, or temporary logic without labeling it as local temporary work and listing the release correction.
- Passes acceptance by changing display text while leaving real data, route, state, or persistence behavior broken.

If the repository has no established layering, propose a minimal layer structure before implementation and mark it as `待确认`.

## 3. Expected Layering For Go Full-Stack Work

Adapt to the existing repository, but when no stronger project pattern exists, use this default mental model:

| Layer | Responsibility |
| --- | --- |
| Frontend page/component | Render state, collect input, trigger events, show success/failure/empty/loading states |
| Frontend service/API wrapper | Centralize URL, method, headers, DTO typing, token handling, and response normalization |
| Gateway/controller/handler | Bind request, basic validation, auth context, trace ID, call service |
| Service/domain | Business rules, ownership checks, status transitions, transaction orchestration, idempotency decisions |
| Repository/DAO | Database queries, writes, indexes, optimistic lock fields, soft delete filters |
| Infrastructure adapter | Redis, MQ, ES, object storage, third-party APIs, model providers, SDK calls, retry/degrade behavior |
| Config layer | Environment, YAML/Nacos/Consul, feature flags, provider selection, secrets references |
| Test layer | Unit, integration, API, frontend build, contract checks, regression cases |

## 4. Implementation Plan Requirements

Before code modification, the plan must identify:

- Which layer each changed file belongs to.
- Why that layer owns the change.
- Which confirmed document or user requirement each change implements.
- Which existing route, DTO, service, table, config, or middleware is reused.
- Which new route, DTO, method, table, config, or adapter is added.
- Which production risks are deliberately out of scope and why.

Do not accept plans that only say "modify frontend" or "add backend logic" without layer ownership and evidence.

## 5. Review Questions

Before calling work complete, answer:

1. Can this behavior be traced to a confirmed document or user instruction?
2. Does the implementation follow the project's existing module and service boundaries?
3. Are business rules enforced server-side when data integrity or permissions matter?
4. Are request/response DTOs consistent across frontend, gateway, and service?
5. Are database writes transactional where multi-table consistency matters?
6. Is duplicate submit, retry, refresh, or concurrent update handled?
7. Are third-party failures, timeouts, retries, compensation, and degradation handled or marked `仍未闭环`?
8. Are logs useful for diagnosis without leaking sensitive data?
9. Were targeted tests, builds, or live requests run?
10. Are remaining gaps listed as risks instead of hidden behind "completed" wording?


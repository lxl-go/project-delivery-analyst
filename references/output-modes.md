# Output Modes

## Pure Business Requirement

Use when the user wants a business-facing requirements document for product, operations, testing, or acceptance.

Allowed:

- Business background, target users, role permissions, page interactions, functional requirements, business rules, data display rules, exports, user-visible states, acceptance criteria.

Forbidden:

- Database, table, field, index, cache, Redis, Kafka, MQ, Elasticsearch, WebSocket, HTTP, gRPC, API parameters, code, CI/CD, Docker, Kubernetes, DDD, framework names, deployment paths.

## Persona-Specific Output

Before producing a document, identify the target reader:

| Persona | Use when | Emphasis | Avoid |
| --- | --- | --- | --- |
| Product manager | PRD, requirement analysis, prototype, interaction, acceptance | Business background, target users, page flow, role permissions, functional requirements, business rules, acceptance criteria | Framework names, database fields, middleware, deployment details |
| Project manager | Project plan, delivery governance, schedule, risk, traceability | Scope, milestones, dependencies, owners, risks, blockers, acceptance materials, document synchronization | Low-level code detail unless it affects delivery risk |
| Go full-stack engineer | Technical design, implementation guide, API/database review, code audit | Go framework, frontend framework, middleware, third-party APIs, service boundaries, DTOs, tables, transactions, idempotency, logs, tests | Unverified business expansion and invented provider details |
| Testing/acceptance | Test plan, validation matrix, regression, compliance review | Scenario matrix, normal/boundary/exception/idempotency flows, evidence, uncovered risks | Implementation speculation without testable behavior |

If the user states an identity, use it. If the identity is inferred, state the inference and keep unknowns as `待确认`.

## Hybrid Requirement

Use when the user explicitly wants business requirements plus controlled technical acceptance content.

Allowed technical sections only:

- Non-functional indicators.
- Technical acceptance constraints.
- Work-order or task matrix.
- Service boundary constraints.
- Interface-level acceptance only when needed for verification, not implementation detail.

Mark uncertain metrics as "待确认"; do not invent QPS, P99, capacity, or cost numbers.

## Technical Design

Use for implementation planning. It may include architecture, module boundaries, API shape, data model, middleware, security, exceptions, performance, deployment, and risks.

Technical design may be created from a PRD, but it must not add new business requirements without marking them as assumptions or questions.

For Go full-stack engineer readers, include language, framework, middleware, third-party API, module ownership, service boundary, DTO, database, transaction, idempotency, logging, and verification sections when supported by documents or code evidence.

## Technical Review

Use for formal review. It must include requirement traceability:

- Each technical decision should cite a PRD section, work order, or user-confirmed requirement when available.
- Risks must include mitigation.
- Unknowns must be listed instead of silently filled in.

## Project Rules

Use to create reusable project constraints under `.dev-rules/rule/`.

Generate rules from provided project facts. Do not create team policy, architecture, security, or release constraints that have no source or explicit user confirmation.

When the user asks for AI constraints, development guardrails, batch rules, or anti-fake-fix rules, read [ai-constraints.md](ai-constraints.md). Prefer human-readable project rules plus task-trace guidance over generic coding style rules.

Rules must be derived from project facts, confirmed documents, or user confirmation. If the project is a microservice or layered application, include module-boundary and production-readiness rules from [production-code-standards.md](production-code-standards.md).

## Project Understanding

Use when the user is doing secondary development and may not understand the existing project. Read [project-understanding.md](project-understanding.md). The output must be read-only and evidence-labeled.

## Frontend Layout Description

Use when the user needs frontend page planning, competitor-inspired page structure, role-based screens, or end-specific UI layout.

Include:

- End and role.
- Page list.
- Navigation and entry points.
- Page layout.
- Buttons, forms, tables, states, and interactions.
- Data source for each page area.
- Empty, loading, error, and permission states.

## Frontend/Backend Closed Loop

Use when the user needs to understand how a function completes from frontend action to backend processing and back to frontend display.

Include:

- Frontend page and action.
- API method and route.
- Request/response DTOs.
- Backend service flow.
- Database and third-party effects.
- State transitions.
- Exceptions and frontend feedback.
- Acceptance checks.

## Interface Implementation Guide

Use when the user asks how to implement a feature or interface. Read [interface-implementation-guide.md](interface-implementation-guide.md). This artifact must describe code-level implementation order, exception handling, database work, third-party calls, performance, validation, logs, and frontend/backend closure.

## Task Trace

Use for every development or fix task. Read [task-trace-template.md](task-trace-template.md). The primary directory is `docs/task-trace/` so both the user and AI can inspect it.

## Compliance-Only

Use when the user asks to check existing documents.

Do not regenerate the document body. Produce only the report unless remediation is explicitly requested.

## Document/Code Alignment Audit

Use when the user asks whether code follows documents, whether a task was implemented according to PRD/API/database/technical design, or whether an existing implementation can run. Read [document-code-alignment.md](document-code-alignment.md).

The output must compare confirmed documents, code evidence, and runtime evidence. Do not mark an item complete unless runtime evidence exists.

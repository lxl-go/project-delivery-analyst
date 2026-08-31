# AI Constraints And Development Guardrails

Use this reference to generate project-specific AI constraints and to control development/fix tasks.

## 1. Goal

Prevent these failure modes:

- Unbounded scanning and unrelated repairs.
- Speculative root-cause guesses.
- Fixing whatever the scan finds instead of the assigned task.
- New errors caused by modifying already working logic.
- Fake fixes that only change appearance or mock data.
- Hard-coded URL, token, role, status, config, or third-party fields.
- Production-unready code that ignores permissions, validation, transactions, idempotency, concurrency, logs, errors, and performance.
- Single-file fake implementation that bypasses the project's module, service, microservice, API wrapper, controller, service, repository, adapter, or configuration boundaries.
- Invented third-party APIs, config, SDK usage, callbacks, signatures, schemas, or performance numbers.
- Frontend/backend mismatch, Chinese encoding pollution, large integer ID precision loss, and fake frontend implementation.
- Sensitive information leaking into logs, examples, task traces, screenshots, commands, or generated documents.

## 2. Core Hard Rules

- Focus on the current task only.
- Each batch solves one clear goal.
- Respect finalized documents. During development, follow finalized documents strictly. During repair, compare the new user requirement with finalized documents; if there is a difference, prioritize the new user requirement and apply the document synchronization rule.
- Before development or repair, state what will be changed.
- Explain why each location will be changed.
- Explain what problem each modification solves.
- Generate or update a solution document.
- Do not modify code without an affected-file list.
- Register out-of-scope issues only; do not repair them.
- Ask the user when third-party API docs, config, secrets, callbacks, signing rules, or SDK usage are missing.
- Do not fabricate third-party fields, schemas, configuration, callbacks, signatures, SDK behavior, or performance numbers.
- Do not present mock, sample, temporary, or local-only code as production-ready.
- Do not present one-file, architecture-bypassing, or module-bypassing code as production-ready when the project has established layers or services.
- Do not hard-code URLs, tokens, roles, status values, or config unless the project has an explicit existing rule.
- Consider permission, parameter validation, transactions, idempotency, concurrency, logs, exceptions, and performance.
- For frontend/backend work, verify page entry, API method, backend route, DTOs, database handling, and status flow.
- Protect large integer IDs from JavaScript precision loss; use strings when needed.
- Avoid Chinese garbling or encoding pollution in code and documents.
- Do not implement only frontend fake behavior; verify real interface closure.
- Do not move backend business rules into frontend-only checks when the rule affects permissions, ownership, money, state transitions, persistence, or external side effects.
- If tests were not run, do not say "completed"; mark the status as `仍未闭环`.
- Safe read-only inspection may continue while facts are being established, but it does not authorize modification or scope expansion.

## 3. Required Rule Dimensions

When generating project AI constraints, include only dimensions supported by project facts or user confirmation:

- Project type rules.
- Batch isolation rules.
- Readable scope rules.
- Modifiable scope rules.
- Forbidden scope.
- Verified-logic protection rules.
- Frontend/backend chain verification rules.
- Database-change rules.
- Status-flow rules.
- Log-investigation rules.
- Human confirmation before repair.
- Self-test and acceptance rules.
- Out-of-scope issue registration rules.
- Local-development relaxation and release correction rules.
- Module-boundary and production-readiness rules.
- Document-to-code traceability rules.

## 4. Security And Logging

- Never log passwords, tokens, session identifiers, signing secrets, private keys, payment data, or full sensitive request/response bodies.
- Mask personal or business-sensitive identifiers unless the project has an explicit audit requirement.
- Add logs only where they improve diagnosis, auditability, or state-transition visibility.
- Keep log level and volume appropriate for production.
- Do not expose secrets in examples, task traces, generated documents, test commands, or screenshots.

## 5. Code Quality Requirements

When implementation is allowed:

- Add logs to key business flows.
- Add logs to exception branches.
- Add necessary logs before and after third-party calls.
- Record key state transitions.
- Add concise comments for complex logic, idempotency, locks, transactions, money, permissions, or status decisions.
- Comments must explain why the logic exists, not restate what the code does.
- Do not add boilerplate logs, comments, locks, caches, or abstractions without a concrete need.

## 6. Anti Fake Implementation Gate

Before accepting implementation, check:

- Does every changed file belong to an intended project layer?
- Does the change reuse existing API wrappers, routes, services, repositories, middleware, config, and adapters where they exist?
- Is business logic enforced in the backend/domain layer when integrity or permissions matter?
- Are database operations isolated in the expected repository/DAO layer?
- Are third-party calls isolated behind adapters or service clients?
- Are config, provider choice, URLs, prompts, and secrets read from existing configuration paths instead of being hard-coded?
- Is the behavior proven by tests or real requests rather than static code existence?

If any answer is no, mark the item `仍未闭环` and describe the missing production step. Use [production-code-standards.md](production-code-standards.md) for the full review.

## 7. Local Vs Release

Local development may temporarily use mocks, test config, switches, logs, or relaxed validation for testing convenience. These must be marked as local temporary items.

Before release, remind the user to correct or confirm:

- Mocks.
- Hard-coded values.
- Temporary config.
- Third-party production config.
- Permission and validation completeness.
- Transaction, idempotency, and concurrency completeness.
- Log appropriateness.
- Production performance, pagination, indexes, cache, and capacity.
- Chinese encoding.
- Large integer ID transfer safety.

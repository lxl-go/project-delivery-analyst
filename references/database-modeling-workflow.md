# Evidence-Driven Database Modeling Workflow

Use this before producing `database.md`, DDL guidance, migration plans, or database-related implementation guidance.

Core rule: every table, field, index, enum value, nullable decision, redundant field, lock field, and idempotency field must have a source basis. If the basis is missing or inferred, mark it as `仍未闭环`; do not invent it.

## 1. Global Rules

- Do not start database design from imagined pages, DTOs, or generic CRUD tables.
- Use page fields, list filters, detail display fields, and DTO fields as reverse checks after business modeling, not as the first modeling basis.
- Allow controlled redundancy when it is justified by historical snapshots, query performance, cross-module decoupling, reports, or audit evidence.
- Do not force third normal form when the project context favors read performance, immutable business snapshots, or delivery compatibility.
- Do not produce DDL or modify code for database changes until scope, impact, rollback, and human confirmation are established.
- Label all conclusions with `文档已确认`, `代码已存在`, `已测试通过`, or `仍未闭环`.

## 2. 0-1 Project Modeling Flow

Use this order for new projects:

1. Confirm roles.
2. Confirm business facts that must be persisted long term.
3. Confirm business objects with independent lifecycles.
4. Confirm business actions, such as create, submit, review, pay, cancel, complete, refund, assign, archive.
5. Confirm state machines: states, triggers, actors, guard conditions, reversibility, abnormal paths.
6. Confirm business constraints: uniqueness, requiredness, transaction boundaries, concurrency risks, idempotency risks.
7. Confirm query, sorting, filtering, statistics, report, and audit scenarios.
8. Confirm data lifecycle: soft delete, retention, archiving, partitioning, and expected growth when known.
9. Derive logical entities, table relationships, candidate fields, field types, nullable rules, indexes, redundancy, lock fields, and idempotency fields.
10. Use pages, forms, list filters, detail displays, APIs, and DTOs to reverse-check missing fields or over-modeled fields.

Do not generate a final `database.md` until the requirement summary and core business flow are confirmed. If business facts, state machines, or query scenarios are incomplete, output questions and mark the affected tables or fields as `仍未闭环`.

## 3. 0-1 Decision Rules

| Decision | Rule |
| --- | --- |
| Add a table | A business object has an independent lifecycle, one-to-many details, many-to-many relation, status history, money flow, audit trail, snapshot, or large-growth boundary. |
| Add a field | The field maps to a business fact, action, state, query, audit need, compatibility need, or statistics need. |
| Choose a type | Use business meaning, range, precision, calculation needs, sorting needs, and project conventions. Do not choose by frontend control alone. |
| Amount fields | Use integer minor units or decimal according to project convention. Do not use floating point. |
| State fields | Derive only from confirmed state machines. Do not invent enum values. |
| Nullable fields | Use `NOT NULL` only when the value is required at creation and historical/migration data can guarantee it. |
| Indexes | Add only for confirmed unique constraints, joins, high-frequency filters, sorting, pagination, statistics, or lookup paths. |
| Redundant fields | Allow only for historical snapshots, query performance, cross-module decoupling, reports, or audit evidence. Explain the source and sync rule. |
| Optimistic lock | Add when multiple actors or processes can update the same business object and blind overwrite is unacceptable. |
| Idempotency field | Add for payment callbacks, refunds, order submission, repeated clicks, third-party notifications, retries, or compensation. |
| Log/flow table | Add when status, money, review, manual operation, or responsibility chain must be traceable. |

## 4. Secondary-Development Database Flow

Secondary development is compatibility-first. Do not redesign an ideal schema from scratch.

Required order:

1. Define the read-only evidence scope before inspection.
2. Identify existing database assets: tables, fields, indexes, migrations, ORM models, DAO/repository access, service usage, DTO references, page usage, reports, scheduled jobs, cache keys, import/export, and task-specific logs.
3. Establish existing table semantic boundaries: what each relevant table means and which features depend on it.
4. Confirm the new requirement difference: new business object, old rule change, old field semantic change, new detail records, state history, display/query-only change, or integration need.
5. Decide the least disruptive strategy: reuse existing table, add nullable field, add one-to-one extension table, add detail table, add flow/log table, add relation table, add snapshot table, or add async/compensation table.
6. Prove why any new table is necessary and why old tables or fields cannot safely carry the new business fact.
7. Analyze compatibility impact on old data, old APIs, old pages, reports, scheduled jobs, cache, import/export, migrations, and rollback.
8. Output a database change proposal with source basis, evidence state, migration plan, rollback plan, and human-confirmation items.

## 5. Secondary-Development Hard Rules

- Do not directly drop fields.
- Do not change an existing field's business meaning.
- Do not reuse an old field with a new semantic meaning.
- Prefer new nullable fields for additive scalar data.
- Use Go pointer fields only when the database column allows `NULL`.
- If business semantics change, use a new field, dual write, one-to-one extension table, or new business table.
- Deprecated fields require multi-version transition before physical deletion.
- Any existing schema change, including length expansion, comment changes, default changes, index changes, and nullable changes, requires impact analysis, rollback plan, and explicit human confirmation.
- New tables still require table name, field list, indexes, migration plan, rollback plan, and compatibility impact confirmation before DDL or code changes.

## 6. When A Secondary-Development Feature Needs A New Table

Create a new table only after evidence supports one of these cases:

| Case | Preferred table type |
| --- | --- |
| New core business object with independent lifecycle | Main business table |
| Original table must not be polluted or old field semantics would change | One-to-one extension table |
| One parent has multiple child records | Detail table |
| Payment, refund, balance, or status transitions must be traced | Flow table |
| Review, manual operation, or responsibility chain must be traced | Operation log table |
| Many-to-many binding | Relation table |
| Historical price, address, name, phone, or other immutable facts must be preserved | Snapshot table |
| Third-party callback, retry, compensation, or async process must be durable | Async/compensation table |

For each proposed new table, document:

- Which new business fact it stores.
- Which existing tables were evaluated for reuse.
- Why reuse is unsafe or insufficient.
- Which existing functions depend on the related old tables.
- Whether old data must be migrated or backfilled.
- Whether dual write, read fallback, or compatibility mapping is needed.
- Whether rollback can ignore, disable, or detach the new table.

## 7. Evidence Matrices

Use these matrices in database design outputs.

### Table Basis Matrix

| Table | New/reuse/extension | Source basis | Why existing structure is insufficient | Compatibility impact | Evidence state |
| --- | --- | --- | --- | --- | --- |

### Field Basis Matrix

| Table | Field | Source basis | Business use | Nullable | Redundant | Sync/migration rule | Evidence state |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Index Basis Matrix

| Table | Index | Fields | Unique | Query/constraint source | Evidence state |
| --- | --- | --- | --- | --- | --- |

### DDL Confirmation Matrix

| Change | Impact | Rollback plan | Requires human confirmation | Evidence state |
| --- | --- | --- | --- | --- |

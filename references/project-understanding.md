# Secondary-Development Project Understanding

Use this reference when the user may not understand an inherited project, or when a secondary-development task requires read-only analysis before planning.

## 1. Entry Rule

Do not start with a full project scan by default. First ask the user to explain the project. If their explanation is incomplete or project evidence is needed, perform a read-only project portrait using the smallest useful evidence set.

Before scanning, state:

- Allowed read scope.
- Forbidden modification scope.
- Core analysis target.
- Rule for unrelated findings: register only, do not repair.

Read-only analysis may resolve ambiguity, but it does not authorize file modification, refactoring, dependency installation, or unrelated issue repair.

## 2. Read-Only Analysis Scope

Analyze only the agreed project files. Prefer README, docs, package/module manifests, router files, API definitions, DTO/model files, database migrations, config examples, representative service/controller files, target frontend entries, and task-specific logs.

Do not modify files during project understanding.
Expand read scope only when the first evidence set cannot answer the current question. State the reason for expansion before reading more files.
For database-related secondary development, also map existing table semantics, field usage points, indexes, migration history, ORM models, DAO/repository access, DTO references, page usage, reports, scheduled jobs, cache keys, and import/export touchpoints inside the agreed scope.

## 3. Project Portrait Output

Produce a human-readable report with evidence labels:

- Project business description.
- README or project documentation summary.
- Main business workflow.
- Technology stack, framework, language, and runtime.
- Directory structure.
- Code layering.
- Code flow from entry to persistence.
- Code style and conventions.
- Existing ends, such as admin, user, driver, merchant, gateway, service, app, or mini program.
- Modules in each end.
- Existing feature interfaces in each module.
- Frontend page/button/API method to backend route mapping.
- Database tables, key fields, and state flows.
- Existing table semantic boundaries: what each relevant table currently means, which features depend on it, and which fields must not be reused with changed business meaning.
- Database compatibility risks for the current requirement, including old data, old APIs, old pages, reports, scheduled jobs, cache, import/export, and migration scripts.
- Existing exception-handling style.
- Reusable components, interfaces, utilities, services, and tables.
- Differences between the current requirement and existing implementation.
- Unknown or missing materials that require user input.
- Evidence state for material findings: `文档已确认`, `代码已存在`, `已测试通过`, or `仍未闭环`.

## 4. Understanding Check

After the portrait, summarize:

- What the project does.
- What the user is probably responsible for.
- Which modules and files are likely relevant.
- What can be reused.
- What is still not closed.

Ask the user to confirm before moving to PRD, implementation design, or code changes.

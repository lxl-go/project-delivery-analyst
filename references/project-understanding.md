# Secondary-Development Project Understanding

Use this reference when the user may not understand an inherited project, or when a secondary-development task requires read-only analysis before planning.

## 1. Entry Rule

Do not start with a full project scan by default. First ask the user to explain the project. If their explanation is incomplete, ask whether to perform a read-only project portrait.

Before scanning, state:

- Allowed read scope.
- Forbidden modification scope.
- Core analysis target.
- Rule for unrelated findings: register only, do not repair.

## 2. Read-Only Analysis Scope

Analyze only the agreed project files. Prefer README, docs, package/module manifests, router files, API definitions, DTO/model files, database migrations, config examples, and representative service/controller files.

Do not modify files during project understanding.

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
- Existing exception-handling style.
- Reusable components, interfaces, utilities, services, and tables.
- Differences between the current requirement and existing implementation.
- Unknown or missing materials that require user input.

## 4. Understanding Check

After the portrait, summarize:

- What the project does.
- What the user is probably responsible for.
- Which modules and files are likely relevant.
- What can be reused.
- What is still not closed.

Ask the user to confirm before moving to PRD, implementation design, or code changes.


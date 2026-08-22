# Repository Rulepack

Use this reference when the user asks to generate or standardize repository-native AI workflow rules, such as `AGENTS.md`, `aiDoc/`, `workflow/`, work items, OpenSpec change packages, test reports, release plans, learnings, or waivers.

This module is optional. Do not apply it to ordinary questions, single PRD drafts, or small fixes unless the user asks for a repository rulepack or project-level AI workflow files.

## 1. Purpose

The rulepack turns AI collaboration rules into repository files so future work has a stable source of truth. It should define what the AI reads, what it may change, how work is numbered, how changes are specified, how tests are recorded, and how release and learning materials are preserved.

Keep the generated rules project-specific and evidence-driven. If project facts are missing, write `待确认` instead of inventing framework, directory, API, deployment, security, or performance rules.

When backend implementation language is not specified by the project or user, default to Go.

## 2. When To Use

Use this module for requests like:

- Generate `AGENTS.md` for this repo.
- Build an `aiDoc/` and `workflow/` rule system.
- Create an AI development workflow with work items, OpenSpec, Loops, test reports, release plans, learnings, and waivers.
- Standardize AI rules for a Go backend project.
- Convert existing project rules into repository-native Markdown.

Do not use this module just because the task mentions AI. For ordinary AI constraints or batch gates, use `ai-constraints.md` and `repository-workflow.md` first.

## 3. Output Tree

For a full rulepack, produce or update this structure:

```text
AGENTS.md
aiDoc/
  README.md
  relations/
    repo-profile.md
    system-map.md
    development-workflow.md
    copyright-and-brand.md
  modules/
    backend-layering.md
    plugin-development.md
  frontend-backend/
    response-contract.md
    field-contract.md
    frontend-ui-rules.md
  examples/
    backend-example.md
    frontend-example.md
    plugin-example.md
  memory/
    long-term-memory.md
    business-requirements-memory.md
workflow/
  README.md
  standards/
    requirement-delivery.md
    framework.md
    rest-api.md
    tech-stack.md
    git.md
  work-items/
    active/
    done/
  openspec/
    changes/
      <WORK-ID>/
        proposal.md
        spec.md
        design.md
        tasks.md
        summary.md
  loops/
    README.md
  test-reports/
  release-plans/
  learnings/
  waivers/
```

Create only the files requested by the user when they ask for a partial rulepack.

## 4. AGENTS.md Content

`AGENTS.md` should be the repository rule entrypoint. Include:

- Project scope and default language.
- Required read order.
- Allowed and forbidden scan scope.
- Allowed and forbidden modification scope.
- Batch isolation rules.
- Evidence labels.
- Frontend/backend contract rules when applicable.
- Test and acceptance requirements.
- Release and push restrictions.
- Memory and learning rules.
- Copyright, brand, and third-party boundary rules when known.

Do not embed every detailed standard in `AGENTS.md`. Link to `aiDoc/` and `workflow/` files for details.

## 5. aiDoc Layer

Use `aiDoc/` for long-lived project context:

- `relations/`: project portrait, system map, development workflow, copyright and brand boundaries.
- `modules/`: backend layering, plugin rules, service boundaries, module-specific invariants.
- `frontend-backend/`: response shape, field naming, route/API parity, UI state and click verification rules.
- `examples/`: teaching examples that explain recommended code organization and common mistakes.
- `memory/`: durable project facts and business requirement memory.

Every project fact should be evidence-labeled. Mark guesses as `仍未闭环`.

## 6. workflow Layer

Use `workflow/` for work execution and traceability:

- `standards/`: project-level standards for requirements, framework, REST API, tech stack, and Git.
- `work-items/`: numbered `REQ`, `BUG`, and `CHORE` items.
- `openspec/changes/<WORK-ID>/`: one change package per work item.
- `loops/`: bounded execution prompts and loop rules.
- `test-reports/`: command-based verification records.
- `release-plans/`: release scope, rollback, and post-release checks.
- `learnings/`: reusable lessons from completed work.
- `waivers/`: documented exceptions and accepted risks.

Work item IDs should be stable and human-readable, such as `REQ-YYYY-001`, `BUG-YYYY-001`, or `CHORE-YYYY-001`.

## 7. OpenSpec Package

For each concrete work item, generate:

- `proposal.md`: goal, scope, non-goals, risks, affected areas.
- `spec.md`: acceptance criteria, API/data contracts, state changes, edge cases.
- `design.md`: implementation boundary, reliability, security, rollback, compatibility.
- `tasks.md`: ordered implementation and verification tasks.
- `summary.md`: short current-state summary for future AI runs.

OpenSpec files should not contain unsupported claims. Use `待确认` for missing business facts and `仍未闭环` for unverified technical facts.

## 8. Loops Rules

Loops should keep AI execution bounded:

- Read only the current work item, current OpenSpec stage, current task, and latest summary.
- Record each failed command with command, exit code, key output, and next action.
- Do not auto push, merge, release, delete data, or change production configuration.
- Default to no more than 3 retry loops. Use 5 as a hard ceiling only when the user explicitly confirms the risk and value.
- Stop when scope exceeds the current work item or required evidence is missing.

## 9. Acceptance Material

A completed rulepack should report:

- Files created or updated.
- Project facts used as evidence.
- Items marked `待确认` or `仍未闭环`.
- Validation commands that were run.
- Remaining risks and maintenance guidance.

Do not claim the rulepack is production-ready unless the repository-specific facts, tests, release rules, and owner review have been completed.

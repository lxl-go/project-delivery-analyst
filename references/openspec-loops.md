# OpenSpec + Loops

This reference captures the bounded execution loop used for AI workflow work.

## 1. OpenSpec change package

Use one change directory per work item. Keep only the current change context in:

- `proposal.md`
- `spec.md`
- `design.md`
- `tasks.md`
- `summary.md`

The files should describe the current work item, not a long narrative log.

## 2. Loops behavior

Loops should only:

- read the current OpenSpec stage
- read the latest short summary
- emit a short prompt for that stage
- run deterministic checks from the allowed set
- write a short summary of the outcome

Loops should not auto push, merge, or release.

## 3. Bounded execution

Keep the loop short and deterministic:

- default 3 iterations
- hard upper bound 5 iterations
- short context only
- failure stops the current loop and records the command, exit code, and next step

## 4. Why this helps

This pattern keeps AI work predictable, limits token growth, and makes each stage independently reviewable.

## 5. When to read

Read this file when the user asks about OpenSpec, Loops, stage prompts, bounded execution, or AI workflow sequencing.

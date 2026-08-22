# v1.3.0 Release Notes

## Summary

This release upgrades `project-delivery-analyst` into a main router skill with repository-native workflow support.

## Added

- Repository workflow routing for batch gates and chain contracts.
- OpenSpec / Loops references for bounded AI execution.
- Release-oriented README content.

## Compatibility

- Skill name unchanged.
- Invocation unchanged.
- Existing validation script retained.
- Existing delivery and compliance routes remain available.

## Why this is v1.3.0

This is a backward-compatible capability expansion. It adds routing and workflow modules without splitting the skill or breaking existing references. Reserve `v2.0.0` for a breaking restructure or a separate skill split.

## Validation

Run the standard structural check:

```bash
python scripts/validate_project_delivery.py --skill-root .
```

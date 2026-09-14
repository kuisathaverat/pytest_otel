---
applyTo: "**"
paths: "**"
globs: "**"
description: "DRY (Don't Repeat Yourself) design principle"
---

# DRY — Don't Repeat Yourself

Every piece of knowledge should have a single, unambiguous representation in the system.

## Guidelines
- Extract shared logic (budget checks, cost lookups, session-state queries) into a single
  function/module used by both the dispatcher and any agent profile that needs it
- Keep schema definitions (e.g. `ideas`, `idea_events`) in one place (`schema/`) and reference
  them, don't redefine the shape ad hoc in scripts or the canvas
- Prefer a single source of truth for config (e.g. `budget_config`) over copy-pasted constants
- Not a license to over-abstract: two similar-looking things that change for different reasons
  are not duplication (see KISS/YAGNI) — only unify what actually represents the same knowledge

## Anti-patterns to avoid
- Copy-pasting the same validation/budget-check logic into multiple agent profiles
- Hardcoding the same repo list or label set in more than one file

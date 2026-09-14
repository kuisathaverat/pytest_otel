---
applyTo: "**"
paths: "**"
globs: "**"
description: "SINE (Simple Is Not Easy) design principle"
---

# SINE — Simple Is Not Easy

Simplicity is a deliberate outcome of effort, not the default result of doing less work.

## Guidelines
- Writing the simple version usually takes *more* thought than writing the first thing that
  works — budget time for it, don't skip straight to the "good enough" version
- A simple public interface can (and often should) hide a more careful internal implementation;
  simplicity is about what the caller has to understand, not about avoiding all complexity
- Refactor toward simplicity after something works, don't assume the first draft is simple
  just because it was quick to write
- When reviewing your own or an agent-generated change, ask "is this the simplest correct
  version?" rather than "does this technically work?"

## Relationship to KISS
KISS says *aim* for simple; SINE is the reminder that getting there is real work — don't confuse
"I wrote less code" with "I wrote simpler code."

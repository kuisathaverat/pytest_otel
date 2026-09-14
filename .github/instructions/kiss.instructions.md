---
applyTo: "**"
paths: "**"
globs: "**"
description: "KISS (Keep It Simple, Stupid) design principle"
---

# KISS — Keep It Simple, Stupid

Prefer the simplest design that correctly solves the problem at hand.

## Guidelines
- Avoid clever, dense one-liners when a few clear lines would do
- Avoid speculative abstraction layers (interfaces, factories, plugins) for a single use case
- Prefer straightforward control flow over deep nesting or indirection
- If you can't explain the design in one sentence, it's probably not simple enough
- Optimize for the next reader, not for showing off

## Anti-patterns to avoid
- Building a generic framework to solve one concrete problem
- Adding configuration knobs nobody asked for
- Deep inheritance chains where composition would be clearer

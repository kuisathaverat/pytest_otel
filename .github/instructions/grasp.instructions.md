---
applyTo: "**"
paths: "**"
globs: "**"
description: "GRASP (General Responsibility Assignment Software Patterns) design principles"
---

# GRASP — General Responsibility Assignment Software Patterns

Guidance for assigning responsibilities to modules/classes in this codebase.

## Information Expert
Give a responsibility to the module that has the information needed to fulfill it — e.g. cost
roll-up belongs with the module that reads `assistant_usage_events`, not the canvas.

## Creator
The dispatcher creates idea-processing sessions because it holds the data (queued ideas, budget
state) needed to decide when and how to create them.

## Controller
The dispatcher is the single controller/entry point coordinating a pipeline run — UI (canvas)
and agent profiles never talk to each other directly.

## Low Coupling
Agent profiles should not depend on canvas internals or on each other; they only depend on the
shared schema and the dispatcher's invocation contract.

## High Cohesion
Keep each agent profile focused on one `idea_type`'s concerns; keep budget logic, schema, and
scheduling in their own dedicated modules.

## Polymorphism
Vary behavior by `idea_type` through interchangeable agent profiles (see SOLID/LSP), not through
conditional branching on type strings scattered across the codebase.

## Pure Fabrication
Introduce dedicated, non-domain modules (e.g. a budget-checker, a cost-estimator) when no single
domain object naturally owns that responsibility.

## Indirection
Route session lifecycle events through the dispatcher rather than having the canvas or agent
profiles reach into each other's state directly.

## Protected Variations
Isolate points likely to change (cost model, model-tier mapping, budget config) behind small,
stable interfaces so changes don't ripple through the dispatcher or agent profiles.

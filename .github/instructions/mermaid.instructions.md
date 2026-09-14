---
applyTo: "**/*.md"
paths: "**/*.md"
globs: "**/*.md"
description: "Mermaid diagram conventions for this repository's documentation"
---

# Mermaid Diagram Guidelines

## Choosing a diagram type
- **flowchart** — pipelines and data flow (e.g. idea lifecycle stages, dispatcher decision logic)
- **sequenceDiagram** — interactions over time between actors (e.g. canvas ↔ dispatcher ↔ session,
  scheduler wake-up → reconcile → spawn)
- **stateDiagram-v2** — lifecycle/status machines (e.g. `ideas.status` transitions:
  new → queued → in_progress → needs_review → done | budget_blocked)
- Avoid `graph`/`gantt`/`class` diagrams unless they are clearly the best fit — don't reach for a
  diagram type just because it's available

## Keeping diagrams accurate
- Every diagram in `docs/architecture.md` must reflect the current schema/state machine in
  `schema/` — update the diagram in the same change that alters the states, columns, or flow
- Do not let diagrams drift into aspirational/future design; if it's not implemented, mark it
  clearly (e.g. a note, not a solid arrow) or leave it out

## Complexity budget (KISS/SINE)
- If a diagram needs more than ~10-12 nodes/states to read clearly, split it into two focused
  diagrams (e.g. "idea lifecycle" and "budget enforcement") rather than one dense one
- Prefer short, verb-based edge labels over long descriptive sentences

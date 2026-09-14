---
applyTo: "**"
paths: "**"
globs: "**"
description: "YAGNI (You Aren't Gonna Need It) design principle"
---

# YAGNI — You Aren't Gonna Need It

Don't build functionality until it's actually needed.

## Guidelines
- Implement only what the current idea/stage requires — no "just in case" parameters, hooks,
  or extension points
- Prefer extending code later (when a real second use case appears) over generalizing early
- Delete unused code paths, feature flags, and config options rather than keeping them "for later"
- When in doubt, ship the narrow version and note the possible extension in a comment or issue,
  don't build it preemptively

## Anti-patterns to avoid
- Adding a plugin system before there is more than one plugin
- Designing for scale/load that doesn't exist yet
- Keeping dead code around because "we might need it"

---
applyTo: ".github/extensions/idea-board/**/*.{js,ts,jsx,tsx}"
paths: ".github/extensions/idea-board/**"
globs: ".github/extensions/idea-board/**/*.{js,ts,jsx,tsx}"
---

# JavaScript/TypeScript Guidelines (canvas extension)

## Formatting and Linting
- Formatted with `prettier`
- Linted with `eslint`
- Prefer TypeScript over plain JavaScript for new files

## Design
- The canvas is a pure read/write UI surface — no LLM calls happen inside canvas code
- Keep components small and stateless where possible; state lives in the synced data files,
  not in component memory
- Use `async`/`await` over raw promise chains
- Avoid global mutable state; pass data explicitly
- Never hardcode LLM prompt text (or agent instructions) as string literals in canvas code.
  Prompts, agents, and instructions are reusable AI Assets with exactly one owner: files under
  `.github/prompts/*.prompt.md`, `.github/agents/*.agent.md`, or `.github/instructions/*.instructions.md`.
  Canvas code must read those files at runtime (e.g. via `fs.readFile`) and pass their content
  through — never duplicate the text inline. This keeps manual usage (Copilot Chat, GitHub app)
  and automated usage (scheduled workflows, canvas buttons) in sync (DRY).

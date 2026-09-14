---
applyTo: ".github/workflows/**"
paths: ".github/workflows/**"
globs: ".github/workflows/**"
---

# GitHub Actions Guidelines

## Structure and Best Practices
- Use YAML syntax for GitHub Actions workflows
- Follow GitHub Actions best practices for workflow structure
- Use kebab-case for workflow file names
- Use kebab-case for job names
- Use kebab-case for step names
- Use kebab-case for action names
- Use kebab-case for variable names
- Use kebab-case for input names
- Use kebab-case for output names

## Security and Environment
- Use environment variables for sensitive data
- Use `secrets` for sensitive data
- Use environment variables to interpolate input and output values
- Follow security best practices for workflow permissions
- **Pin all GitHub Actions to SHA checksums** (not tags like `v1`, `v2`) to prevent supply chain attacks
- Use the `ratchet-lint` pre-commit hook to automatically pin actions (see Contributing.md)
- All actions will be automatically pinned on commit by the pre-commit hook

## Common Actions
- Use `ossf/scorecard` for security checks
- Use `actions/checkout` to check out the repository
- Use `actions/setup-python` for Python workflows
- Use `actions/setup-node` for Node.js workflows
- Use `actions/setup-go` for Go workflows
- Use `actions/github-script` to access the GitHub API
- Use `actions/github-script` to manipulate JSON and YAML data

## Workflow Organization
- Keep workflows focused and modular
- Use reusable workflows where appropriate
- Include proper error handling
- Use appropriate triggers for workflows
- Add meaningful names and descriptions

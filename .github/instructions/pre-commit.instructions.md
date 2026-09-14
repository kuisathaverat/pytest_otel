---
applyTo: "**"
paths: "**"
globs: "**"
---

# Pre-commit Validation Instructions

## Mandatory Pre-commit Checks

**CRITICAL REQUIREMENT**: Before committing or pushing ANY changes to this repository, you MUST run:

```bash
pre-commit run --all-files
```

This is not optional. All changes must pass pre-commit validation before being committed.

## What Pre-commit Checks

The pre-commit hooks in this repository validate:
- Code formatting and style consistency
- YAML file syntax and formatting
- JSON file syntax and formatting
- Python code quality (flake8, mypy, isort, black, etc.)
- Shell script quality (shellcheck)
- Markdown formatting
- Trailing whitespace removal
- End-of-file newline enforcement
- Security issues (bandit for Python)
- Spelling errors (codespell)
- File size limits
- Merge conflict markers
- Mixed line endings
- And many more checks

## Running Pre-commit

### First Time Setup

If pre-commit is not yet installed in the repository:

```bash
# Activate virtual environment
source .venv/bin/activate

# Install pre-commit hooks
pre-commit install

# Run all checks
pre-commit run --all-files
```

### Regular Usage

Before every commit and push:

```bash
# Run all pre-commit checks
pre-commit run --all-files
```

### Running Specific Hooks

To run only specific hooks:

```bash
# Run only YAML linting
pre-commit run yamllint --all-files

# Run only Python checks
pre-commit run flake8 --all-files
pre-commit run mypy --all-files
```

## Fixing Pre-commit Failures

When pre-commit reports failures:

1. **Read the error messages carefully** - they usually tell you exactly what's wrong
2. **Fix the issues** - don't just skip or ignore them
3. **Re-run pre-commit** - keep running until all checks pass
4. **Common fixes**:
   - Trailing whitespace: Remove spaces at end of lines
   - File endings: Ensure files end with a single newline
   - YAML formatting: Fix indentation and syntax
   - Python formatting: Use `black` to auto-format
   - Import sorting: Use `isort` to auto-sort imports

## Auto-fixing Issues

Some hooks can automatically fix issues:

```bash
# Many formatters auto-fix on commit
git add .
git commit -m "Your message"
# Pre-commit runs automatically and may auto-fix some issues

# Or run manually with auto-fix
pre-commit run --all-files
# Then stage the auto-fixed files
git add -u
```

## Bypassing Pre-commit (NOT RECOMMENDED)

**DO NOT bypass pre-commit checks unless you have a very good reason.**

Only in exceptional cases where you absolutely must skip checks:

```bash
git commit --no-verify -m "Emergency fix"
```

However, be aware that:
- CI/CD pipelines will still run these checks
- Your PR may be rejected if checks fail
- You may be asked to fix issues before merging

## Integration with Copilot Agents

When working as an AI coding agent:

1. **Always run pre-commit** after making any code changes
2. **Fix all reported issues** before considering the task complete
3. **Do not mark tasks as complete** if pre-commit checks fail
4. **Report pre-commit results** to the user if there are failures
5. **Never skip pre-commit** - it's a critical quality gate

## Workflow for Agents

```bash
# 1. Make code changes
# ... your code modifications ...

# 2. Run pre-commit checks
pre-commit run --all-files

# 3. If failures occur:
#    a. Read error messages
#    b. Fix the issues
#    c. Go back to step 2

# 4. Only when all checks pass:
#    a. Stage changes: git add .
#    b. Commit: git commit -m "your message"
#    c. Push: git push
```

## Common Pre-commit Failures and Solutions

| Error | Solution |
|-------|----------|
| Trailing whitespace | Remove spaces at end of lines |
| No newline at end of file | Add a newline at the end |
| YAML syntax error | Fix YAML indentation and structure |
| Flake8 errors | Fix Python style issues |
| Import sorting issues | Run `isort` to auto-sort |
| Black formatting | Run `black` to auto-format |
| Shellcheck warnings | Fix shell script issues |
| File too large | Remove or gitignore large files |
| Merge conflict markers | Resolve merge conflicts properly |

## Resources

- Pre-commit configuration: `.pre-commit-config.yaml`
- Contributing guide: `Contributing.md`
- Main instructions: `.github/instructions/`
- Project README: `README.md`

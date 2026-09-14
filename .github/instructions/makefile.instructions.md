---
applyTo: "Makefile,*.mk"
paths: "Makefile,*.mk"
globs: "Makefile,*.mk"
---

# Makefile Guidelines

## Indentation
- Use tabs for indentation (required by Make)
- Never use spaces for indentation in Makefiles

## Structure and Documentation
- Use the format `## @help:TARGET_NAME:TARGET_HELP` for target documentation
- Include the `common.mk` file for common targets
- Use `$(MAKE)` for recursive make calls
- Use proper variable definitions and references
- Add comments to explain complex targets
- Group related targets together
- Use `.PHONY` for targets that don't create files

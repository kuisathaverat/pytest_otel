---
applyTo: "*.yml,*.yaml"
paths: "*.yml,*.yaml"
globs: "*.yml,*.yaml"
---

# YAML Code Guidelines

## Indentation and Formatting
- Use 2 spaces for indentation
- Maximum line length: 120 characters
- YAML files must be valid and properly formatted
- Use consistent indentation throughout the file
- YAML should start with `---` to indicate the start of a document

## Tools and Validation
- Use `yamllint` to validate YAML files
- Use `ansible-lint` for Ansible playbooks and roles
- Use `prettier` for formatting YAML files
- YAML files should have yaml-language-server configured for syntax highlighting and validation

## Structure
- Use proper YAML syntax
- Maintain consistent key-value formatting
- Use quotes when necessary for string values
- Follow proper list and dictionary formatting

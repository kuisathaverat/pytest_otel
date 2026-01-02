# Documentation Principles - Copilot Instructions

Follow these documentation principles based on "Principles of Technical Documentation" from https://www.innoq.com/en/articles/2022/01/principles-of-technical-documentation/

## 1. Documentation as Code

**Principle**: Treat documentation like code.

**Guidelines**:
- Store documentation in version control alongside code
- Review documentation changes through pull requests
- Automate documentation builds and deployments
- Keep documentation close to the code it describes
- Use the same quality standards for docs as for code

**Structure Example**:
```
project/
├── src/
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── guides/
│   └── README.md
├── README.md
└── CONTRIBUTING.md
```

## 2. Write for Your Audience

**Principle**: Know your readers and adjust accordingly.

**Guidelines**:
- Identify who will read your documentation (developers, users, operators)
- Adjust technical depth accordingly
- Provide different documentation types for different audiences
- Use appropriate language and terminology
- Include examples relevant to your audience

**Example**:
```markdown
## For Developers

### Setting Up Development Environment

1. Clone the repository: `git clone ...`
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`

## For Users

### Installation

Install the package using pip:
```bash
pip install your-package
```
```

## 3. Keep It Current

**Principle**: Maintain documentation freshness.

**Guidelines**:
- Update documentation with code changes in the same PR
- Regular documentation reviews and updates
- Mark deprecated features clearly
- Remove outdated information
- Use automated checks for broken links and examples

**Practice**:
- Include documentation updates in your PR checklist
- Set up automated link checking in CI/CD
- Review and update docs quarterly

## 4. Structure and Organization

**Principle**: Organize documentation logically.

**Guidelines**:
- Start with a clear overview and purpose
- Use hierarchical structure
- Provide navigation aids (table of contents, cross-references)
- Group related information together
- Use consistent formatting and templates

**Template**:
```markdown
# Component Name

## Overview
Brief description of what this component does.

## Installation
How to install or set up the component.

## Quick Start
Minimal example to get started quickly.

## Usage
Detailed usage instructions with examples.

## API Reference
Detailed API documentation.

## Troubleshooting
Common issues and solutions.

## Contributing
How to contribute to this component.
```

## 5. Include Examples

**Principle**: Provide practical examples.

**Guidelines**:
- Show real-world usage scenarios
- Include both simple and complex examples
- Make examples runnable and testable
- Show common patterns and best practices
- Include expected output

**Example**:
```python
"""
Example: Processing user data

This example shows how to load and process user data:

```python
from your_package import process_users

# Load users from a file
users = load_users('users.json')

# Process with custom configuration
config = {'filter': 'active', 'sort': 'name'}
results = process_users(users, config)

# Expected output:
# [
#   {'name': 'Alice', 'status': 'processed'},
#   {'name': 'Bob', 'status': 'processed'}
# ]
```
"""
```

## 6. Explain the Why

**Principle**: Don't just describe what, explain why.

**Guidelines**:
- Explain design decisions and trade-offs
- Document the reasoning behind choices
- Provide context and background
- Explain when to use different approaches
- Include limitations and constraints

**Example**:
```python
class ConnectionPool:
    """
    Manages a pool of database connections.
    
    Why use a connection pool?
    - Reduces connection overhead (connections are expensive to create)
    - Limits concurrent connections (prevents overwhelming the database)
    - Improves performance through connection reuse
    
    Trade-offs:
    - Memory overhead: Maintains connections even when idle
    - Complexity: Requires proper connection lifecycle management
    
    When to use:
    - Applications with frequent database access
    - High-concurrency scenarios
    
    When not to use:
    - Simple scripts with infrequent database access
    - Single-threaded applications with sequential access
    """
```

## 7. Make It Discoverable

**Principle**: Ensure documentation is easy to find.

**Guidelines**:
- Use clear, descriptive titles
- Implement search functionality
- Provide good navigation
- Link related documentation
- Use consistent naming conventions

**Practice**:
- Include a comprehensive README.md in the root
- Use clear section headers
- Provide a table of contents for long documents
- Cross-reference related documentation

## 8. Use Diagrams and Visuals

**Principle**: Visualize complex concepts.

**Guidelines**:
- Architecture diagrams for system structure
- Sequence diagrams for workflows
- Flow charts for decision logic
- Screenshots for UI documentation
- Tables for comparing options

**Example**:
```markdown
## System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Client    │────▶│   API Layer  │────▶│   Database   │
└─────────────┘     └──────────────┘     └──────────────┘
       │                    │                     │
       │                    ▼                     │
       │            ┌──────────────┐              │
       └───────────▶│  Auth Service│◀─────────────┘
                    └──────────────┘
```
```

## Documentation Types

### API Documentation
- Document all public APIs
- Include parameters, return values, and exceptions
- Provide usage examples
- Document error conditions

### User Guides
- Step-by-step instructions
- Common use cases
- Screenshots where helpful
- Troubleshooting section

### Architecture Documentation
- System overview
- Component interactions
- Design decisions
- Technology choices

### Contributing Guidelines
- How to set up development environment
- Code style guidelines
- Testing requirements
- Pull request process

## Summary

When writing documentation:
1. **Treat as code**: Version control, review, automate
2. **Know your audience**: Adjust depth and language
3. **Keep current**: Update with code changes
4. **Organize logically**: Clear structure and navigation
5. **Include examples**: Real-world, runnable code
6. **Explain why**: Decisions, trade-offs, context
7. **Make discoverable**: Clear titles, good navigation
8. **Use visuals**: Diagrams, charts, screenshots

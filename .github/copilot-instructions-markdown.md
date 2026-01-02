# Markdown Document Guidelines - Copilot Instructions

Follow these markdown guidelines when writing documentation.

## Structure and Formatting

### Headers

Use headers to create clear document structure:

```markdown
# H1 - Document Title (use only once per document)

## H2 - Main Sections

### H3 - Subsections

#### H4 - Sub-subsections (use sparingly)
```

**Rules**:
- Only one H1 per document (the main title)
- Use hierarchical structure (don't skip levels)
- Use descriptive, clear header text
- Keep headers concise

### Emphasis

```markdown
*italic* or _italic_
**bold** or __bold__
***bold and italic***
~~strikethrough~~
`inline code`
```

### Lists

**Unordered lists**:
```markdown
- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
- Item 3
```

**Ordered lists**:
```markdown
1. First item
2. Second item
   1. Nested item 2.1
   2. Nested item 2.2
3. Third item
```

**Task lists**:
```markdown
- [x] Completed task
- [ ] Incomplete task
- [ ] Another task
```

### Links

```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title text")

# Reference-style links
[Link text][reference]

[reference]: https://example.com
```

**Best practices**:
- Use descriptive link text (avoid "click here")
- Use relative links for internal documentation
- Include link titles for additional context

### Images

```markdown
![Alt text](path/to/image.png)
![Alt text](path/to/image.png "Image title")

# Reference-style images
![Alt text][image-ref]

[image-ref]: path/to/image.png "Image title"
```

**Best practices**:
- Always provide meaningful alt text
- Use descriptive image titles
- Optimize image sizes for documentation

### Code Blocks

Use fenced code blocks with language specification:

````markdown
```python
def hello_world():
    print("Hello, World!")
```

```bash
pip install pytest-otel
```

```json
{
  "name": "example",
  "version": "1.0.0"
}
```
````

**Best practices**:
- Always specify the language for syntax highlighting
- Keep code blocks focused and concise
- Ensure code examples are correct and runnable
- Include comments for clarity when needed

### Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

# Alignment
Left-aligned | Center-aligned | Right-aligned
:------------|:--------------:|--------------:
Left         | Center         | Right
```

**Best practices**:
- Keep tables simple and readable
- Use alignment for better clarity
- Consider using lists for simple data

### Blockquotes

```markdown
> This is a blockquote.
> It can span multiple lines.
>
> > Nested blockquote
```

### Horizontal Rules

```markdown
---
***
___
```

## Best Practices

### 1. Consistency

- Use consistent formatting throughout the document
- Choose one style for emphasis (e.g., `*italic*` vs `_italic_`) and stick with it
- Use consistent header capitalization (Title Case or Sentence case)
- Maintain consistent spacing between sections

**Example**:
```markdown
# Good - Consistent

## Section One

Content here.

## Section Two

Content here.

# Bad - Inconsistent

## Section One
Content here.
## section two

Content here.
```

### 2. Readability

- Add blank lines between sections
- Use blank lines around code blocks and lists
- Keep lines under 120 characters when possible (for diffs)
- Use meaningful link text

**Example**:
```markdown
# Good - Readable

Here is some text explaining the concept.

```python
code_example()
```

Here is more explanation.

# Bad - Not readable

Here is some text explaining the concept.
```python
code_example()
```
Here is more explanation.
```

### 3. Accessibility

- Provide alt text for all images
- Use descriptive link text
- Maintain proper header hierarchy
- Use semantic markup (lists, emphasis, etc.)

**Example**:
```markdown
# Good - Accessible
![Screenshot of the user dashboard showing active users](dashboard.png)
Learn more in our [API documentation](api.md).

# Bad - Not accessible
![](dashboard.png)
Learn more [here](api.md).
```

### 4. Code Examples

- Always specify language for syntax highlighting
- Keep examples concise and focused
- Ensure code examples are correct and runnable
- Include output or expected results when relevant

**Example**:
````markdown
# Good - Complete example

```python
# Calculate sum of numbers
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(f"Total: {total}")
# Output: Total: 15
```

# Bad - Incomplete example

```
total = sum(numbers)
```
````

### 5. Links and References

- Use relative links for internal documentation
- Check that all links work
- Use reference-style links for repeated URLs
- Include link titles for additional context

**Example**:
```markdown
# Good - Relative links for internal docs
See the [installation guide](./docs/installation.md) for setup instructions.

# Good - Reference-style for repeated links
Check out [Python][python] and [Python documentation][python].

[python]: https://python.org "Python programming language"

# Bad - Absolute URLs for internal docs
See the [installation guide](https://github.com/user/repo/blob/main/docs/installation.md).
```

## Document Structure Template

Use this template for consistent documentation:

```markdown
# Document Title

Brief introduction explaining what this document covers.

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- [Section 3](#section-3)

## Section 1

Content for section 1...

### Subsection 1.1

Details...

## Section 2

Content for section 2...

## Section 3

Content for section 3...

## Additional Resources

- [External resource 1](https://example.com)
- [External resource 2](https://example.com)

## Related Documentation

- [Related doc 1](./related-doc-1.md)
- [Related doc 2](./related-doc-2.md)
```

## Markdown Linting

Configure markdown linting to maintain quality:

**Example `.markdownlint.json`**:
```json
{
  "default": true,
  "MD013": {
    "line_length": 120,
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
}
```

**Common rules**:
- `MD013`: Line length (configure to project standards)
- `MD033`: Allow inline HTML when needed
- `MD041`: First line doesn't have to be top-level header

## Summary

When writing markdown documentation:

1. **Use proper structure**: Clear headers, proper nesting
2. **Be consistent**: Formatting, spacing, style
3. **Prioritize readability**: Blank lines, line length, meaningful text
4. **Ensure accessibility**: Alt text, semantic markup, descriptive links
5. **Provide complete examples**: Language specification, runnable code, expected output
6. **Maintain links**: Relative for internal, check validity, use references
7. **Lint your markdown**: Use automated tools to maintain quality
8. **Follow project conventions**: Adapt to existing style in the repository

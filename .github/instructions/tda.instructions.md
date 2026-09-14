---
applyTo: "**"
paths: "**"
globs: "**"
description: "TDA (Tell, Don't Ask) design principle for better encapsulation"
---

# TDA (Tell, Don't Ask) Design Principle

The "Tell, Don't Ask" (TDA) principle is a fundamental object-oriented design guideline that promotes better encapsulation and more maintainable code.

## Core Principles

- Tell objects what to do, don't ask for their data and decide for them
- Encapsulate behavior with data
- Avoid getter/setter heavy designs that expose internal state
- Let objects make decisions about their own data
- Move behavior to where the data lives

## Why TDA Matters

- **Better Encapsulation**: Objects control their own state and behavior
- **Reduced Coupling**: Code doesn't depend on internal object structure
- **Easier Maintenance**: Changes to internal state don't ripple through the codebase
- **Clearer Responsibilities**: Each object is responsible for its own behavior

## Examples

### Bad (Ask Pattern)
```python
# Asking for data and making decisions outside the object
if user.get_age() >= 18:
    user.set_status("adult")
```

### Good (Tell Pattern)
```python
# Telling the object what to do
user.update_status_based_on_age()
```

### Bad (Ask Pattern)
```python
# External code decides based on object's data
if order.get_total() > 100:
    discount = order.get_total() * 0.1
    order.set_total(order.get_total() - discount)
```

### Good (Tell Pattern)
```python
# Object handles its own logic
order.apply_discount_if_eligible()
```

## Guidelines for Implementation

- When you find yourself getting data from an object just to make a decision, consider moving that decision into the object
- If a method only gets data and another method uses that data to modify the object, combine them into a single behavior-focused method
- Prefer methods that describe what should happen rather than methods that expose how it happens
- Design interfaces around behaviors, not data access

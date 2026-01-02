# GitHub Copilot Instructions

This file contains custom instructions for GitHub Copilot when working on this repository.

## Software Engineering Principles

Apply the following core software engineering principles when writing code:

### KISS - Keep It Simple, Stupid

**Principle**: Simplicity should be a key goal in design, and unnecessary complexity should be avoided.

**Guidelines**:
- Write code that is easy to understand and maintain
- Avoid over-engineering solutions
- Choose straightforward approaches over clever tricks
- Break complex problems into smaller, manageable pieces
- Prefer readable code over concise but cryptic code
- Use clear naming conventions that convey intent
- Minimize the number of moving parts in your solution

**Example**:
```python
# Good - Simple and clear
def calculate_total_price(items):
    return sum(item.price for item in items)

# Bad - Unnecessarily complex
def calculate_total_price(items):
    return functools.reduce(lambda acc, item: acc + item.price, items, 0)
```

### SOLID Principles

#### Single Responsibility Principle (SRP)
**Principle**: A class should have only one reason to change.

**Guidelines**:
- Each class should focus on doing one thing well
- If a class has multiple responsibilities, split it into separate classes
- Changes to one aspect shouldn't require modifying unrelated functionality

**Example**:
```python
# Good - Single responsibility
class UserRepository:
    def save_user(self, user):
        # Only handles database operations
        pass

class UserValidator:
    def validate_user(self, user):
        # Only handles validation
        pass
```

#### Open/Closed Principle (OCP)
**Principle**: Software entities should be open for extension but closed for modification.

**Guidelines**:
- Design systems that can be extended without modifying existing code
- Use inheritance, interfaces, and composition
- Avoid modifying existing classes when adding new features

**Example**:
```python
# Good - Open for extension
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        # Credit card logic
        pass
```

#### Liskov Substitution Principle (LSP)
**Principle**: Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.

**Guidelines**:
- Derived classes must be substitutable for their base classes
- Don't strengthen preconditions or weaken postconditions
- Preserve the expected behavior of the base class

**Example**:
```python
# Good - Proper substitution
class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

class Sparrow(Bird):
    def move(self):
        return "flying"

class Penguin(Bird):
    def move(self):
        return "walking"
```

#### Interface Segregation Principle (ISP)
**Principle**: Clients should not be forced to depend on interfaces they don't use.

**Guidelines**:
- Create specific, focused interfaces rather than large, general-purpose ones
- Split large interfaces into smaller, more specific ones
- Classes should only implement methods they actually need

**Example**:
```python
from typing import Protocol

# Good - Segregated interfaces
class Printable(Protocol):
    def print(self): ...

class Scannable(Protocol):
    def scan(self): ...

class Printer:
    def print(self):
        pass

class Scanner:
    def scan(self):
        pass
```

#### Dependency Inversion Principle (DIP)
**Principle**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Guidelines**:
- Depend on abstractions, not concrete implementations
- Use dependency injection
- Define interfaces/protocols for dependencies

**Example**:
```python
# Good - Depends on abstraction
class MessageSender(ABC):
    @abstractmethod
    def send(self, message):
        pass

class NotificationService:
    def __init__(self, sender: MessageSender):
        self.sender = sender
    
    def notify(self, message):
        self.sender.send(message)
```

### DRY - Don't Repeat Yourself

**Principle**: Every piece of knowledge should have a single, unambiguous representation within a system.

**Guidelines**:
- Avoid code duplication
- Extract common functionality into reusable functions or classes
- Use inheritance, composition, and mixins appropriately
- Create utility functions for repeated logic
- Don't duplicate business logic
- Be cautious: sometimes duplication is better than the wrong abstraction

**Example**:
```python
# Good - DRY
def validate_email(email):
    return "@" in email and "." in email

def register_user(email):
    if not validate_email(email):
        raise ValueError("Invalid email")
    # Registration logic

def update_user_email(user, email):
    if not validate_email(email):
        raise ValueError("Invalid email")
    # Update logic
```

### YAGNI - You Aren't Gonna Need It

**Principle**: Don't add functionality until it's necessary.

**Guidelines**:
- Implement features only when they're actually needed
- Avoid building "future-proof" systems with unused features
- Focus on current requirements, not hypothetical future needs
- Refactor when new requirements emerge, don't anticipate them
- Keep the codebase lean and maintainable

**Example**:
```python
# Good - Only what's needed now
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Bad - Anticipating future needs
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.address = None  # Not needed yet
        self.phone = None  # Not needed yet
        self.preferences = {}  # Not needed yet
```

### TDA - Tell, Don't Ask

**Principle**: Tell objects what to do, don't ask them for their state and make decisions based on that.

**Guidelines**:
- Encapsulate behavior within objects
- Minimize exposure of internal state
- Objects should make decisions based on their own data
- Avoid getter methods that expose internal state just for external decisions
- Push behavior into the object that owns the data

**Example**:
```python
# Good - Tell, Don't Ask
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def apply_discount(self):
        if len(self.items) > 5:
            return sum(item.price for item in self.items) * 0.9
        return sum(item.price for item in self.items)

cart = ShoppingCart()
total = cart.apply_discount()

# Bad - Ask, Then Tell
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def get_items(self):
        return self.items

cart = ShoppingCart()
if len(cart.get_items()) > 5:
    total = sum(item.price for item in cart.get_items()) * 0.9
else:
    total = sum(item.price for item in cart.get_items())
```

## Summary

Always apply these principles when writing code:
- **KISS**: Keep it simple and maintainable
- **SOLID**: Follow proper object-oriented design
- **DRY**: Avoid code duplication
- **YAGNI**: Only implement what's needed
- **TDA**: Encapsulate behavior with data

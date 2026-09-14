# Python Best Practices - Copilot Instructions

Follow these Python best practices when writing code for this repository.

## Code Style and Structure

### PEP 8 Compliance
- Follow PEP 8 style guide for Python code
- Use 4 spaces for indentation (never tabs)
- Limit lines to 79-120 characters (project-dependent)
- Use snake_case for functions and variables
- Use PascalCase for class names
- Use UPPER_CASE for constants

**Example**:
```python
# Good naming
class UserAccount:
    MAX_LOGIN_ATTEMPTS = 3
    
    def __init__(self, username):
        self.username = username
        self._login_attempts = 0
    
    def authenticate_user(self, password):
        pass
```

## Type Hints

Always use type hints for function signatures and class attributes:

```python
from typing import List, Dict, Optional, Union, Any

def process_users(users: List[str], config: Dict[str, Any]) -> List[Dict[str, str]]:
    """Process a list of users based on configuration."""
    results: List[Dict[str, str]] = []
    for user in users:
        results.append({"name": user, "status": "processed"})
    return results

class User:
    def __init__(self, name: str, age: int, email: Optional[str] = None) -> None:
        self.name: str = name
        self.age: int = age
        self.email: Optional[str] = email
```

## Docstrings

Use comprehensive docstrings following PEP 257:

```python
def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """
    Calculate basic statistics for a dataset.
    
    Args:
        data: A list of numerical values to analyze.
    
    Returns:
        A dictionary containing:
            - mean: The average of the values
            - median: The middle value
            - std_dev: The standard deviation
    
    Raises:
        ValueError: If the data list is empty.
    
    Example:
        >>> calculate_statistics([1, 2, 3, 4, 5])
        {'mean': 3.0, 'median': 3.0, 'std_dev': 1.41}
    """
    if not data:
        raise ValueError("Data list cannot be empty")
    
    # Implementation
    pass
```

## Error Handling

Use specific exceptions and proper error handling:

```python
# Good - Specific exceptions
def read_config(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        raise ValueError(f"Invalid configuration format") from e

# Bad - Bare except
def read_config(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return {}
```

## Context Managers

Use context managers for resource management:

```python
# Good - Automatic resource cleanup
with open('file.txt', 'r') as f:
    content = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def database_connection(db_url: str):
    conn = create_connection(db_url)
    try:
        yield conn
    finally:
        conn.close()

with database_connection('postgresql://...') as conn:
    conn.execute("SELECT * FROM users")
```

## List Comprehensions and Generators

Use comprehensions for concise, readable code:

```python
from typing import Generator

# Good - List comprehension
squared_evens = [x**2 for x in range(10) if x % 2 == 0]

# Good - Generator for large datasets
def process_large_file(filename: str) -> Generator[str, None, None]:
    with open(filename) as f:
        for line in f:
            yield process_line(line)

# Bad - Verbose loop
squared_evens = []
for x in range(10):
    if x % 2 == 0:
        squared_evens.append(x**2)
```

## Properties and Descriptors

Use properties for computed attributes:

```python
class Circle:
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def area(self) -> float:
        return 3.14159 * self._radius ** 2
```

## Dataclasses

Use dataclasses for simple data structures:

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    name: str
    email: str
    age: int
    roles: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")
```

## Testing Best Practices

Write comprehensive tests:

```python
import pytest
from typing import List

def test_user_creation():
    """Test that a user can be created with valid data."""
    user = User(name="John Doe", email="john@example.com", age=30)
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

def test_user_invalid_age():
    """Test that user creation fails with invalid age."""
    with pytest.raises(ValueError, match="Age cannot be negative"):
        User(name="John Doe", email="john@example.com", age=-5)

@pytest.fixture
def sample_users() -> List[User]:
    """Fixture providing sample users for testing."""
    return [
        User(name="Alice", email="alice@example.com", age=25),
        User(name="Bob", email="bob@example.com", age=30),
    ]

def test_process_users(sample_users):
    """Test user processing with fixture data."""
    results = process_users(sample_users)
    assert len(results) == 2
```

## Modern Python Features

Use modern Python features (Python 3.10+):

```python
# Pattern matching (Python 3.10+)
def process_command(command: Dict[str, Any]) -> str:
    match command:
        case {"action": "create", "resource": resource}:
            return f"Creating {resource}"
        case {"action": "delete", "resource": resource}:
            return f"Deleting {resource}"
        case _:
            return "Unknown command"

# Union types (Python 3.10+)
def process_value(value: int | str | None) -> str:
    if value is None:
        return "No value"
    return str(value)
```

## Logging

Use proper logging instead of print statements:

```python
import logging

logger = logging.getLogger(__name__)

def process_data(data: List[Dict[str, Any]]) -> None:
    logger.info(f"Processing {len(data)} records")
    
    for record in data:
        try:
            process_record(record)
            logger.debug(f"Processed record: {record['id']}")
        except Exception as e:
            logger.error(f"Failed to process record {record['id']}: {e}", exc_info=True)
    
    logger.info("Processing completed")
```

## Summary

Apply these Python best practices:
- Follow PEP 8 style guide
- Use type hints for all functions and classes
- Write comprehensive docstrings
- Handle errors with specific exceptions
- Use context managers for resources
- Prefer comprehensions over loops
- Use properties for computed attributes
- Use dataclasses for data structures
- Write tests with pytest
- Use modern Python features
- Use logging instead of print

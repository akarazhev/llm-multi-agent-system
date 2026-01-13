# Testing Guide

## Overview

The LLM Multi-Agent System includes a comprehensive test suite to ensure reliability and correctness of all components. Tests are organized in the `tests/` directory and cover agent functionality, file operations, response parsing, and edge cases.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── simple_test.py             # Simple workflow tests
├── test_agent.py              # Agent functionality tests
├── test_all_formats.py        # File format tests
├── test_file_writer.py        # File writer tests
├── test_full_response.py      # Full response tests
├── test_nested_blocks.py      # Nested block tests
├── test_no_backticks.py       # No backticks tests
└── test_no_duplicates.py      # Duplicate prevention tests
```

## Running Tests

### Run All Tests

```bash
# Using pytest (recommended)
python -m pytest tests/

# With verbose output
python -m pytest tests/ -v

# With coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test Files

```bash
# Run a single test file
python -m pytest tests/test_agent.py

# Run multiple specific files
python -m pytest tests/test_agent.py tests/test_file_writer.py
```

### Run Individual Tests

```bash
# Run as standalone scripts
python tests/simple_test.py
python tests/test_file_writer.py
python tests/test_all_formats.py
```

### Run Tests with Filters

```bash
# Run tests matching a pattern
python -m pytest tests/ -k "file_writer"

# Run tests by marker (if configured)
python -m pytest tests/ -m "unit"
```

## Test Categories

### 1. Agent Functionality Tests (`test_agent.py`)

Tests core agent behavior and workflow execution:
- Agent initialization
- Task execution
- Workflow coordination
- Error handling
- State management

**Run:**
```bash
python -m pytest tests/test_agent.py -v
```

### 2. File Writer Tests (`test_file_writer.py`)

Tests file writing utilities and operations:
- File creation
- Directory handling
- Content writing
- Format preservation
- Error recovery

**Run:**
```bash
python tests/test_file_writer.py
```

### 3. Format Handling Tests (`test_all_formats.py`)

Tests support for multiple file formats:
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Markdown (.md)
- YAML (.yaml)
- JSON (.json)
- And more...

**Run:**
```bash
python tests/test_all_formats.py
```

### 4. Response Parsing Tests (`test_full_response.py`)

Tests LLM response parsing and extraction:
- Code block extraction
- Metadata parsing
- Multi-file responses
- Format detection

**Run:**
```bash
python tests/test_full_response.py
```

### 5. Edge Case Tests

#### Nested Blocks (`test_nested_blocks.py`)
Tests handling of nested code structures:
- Nested functions
- Nested classes
- Complex indentation
- Multi-level nesting

**Run:**
```bash
python tests/test_nested_blocks.py
```

#### No Backticks (`test_no_backticks.py`)
Tests handling of responses without code fences:
- Plain text code
- Inline code
- Mixed formats

**Run:**
```bash
python tests/test_no_backticks.py
```

#### Duplicate Prevention (`test_no_duplicates.py`)
Tests prevention of duplicate file creation:
- Duplicate detection
- Overwrite protection
- Version management

**Run:**
```bash
python tests/test_no_duplicates.py
```

### 6. Simple Workflow Tests (`simple_test.py`)

End-to-end workflow tests:
- Complete workflow execution
- Agent coordination
- Output validation

**Run:**
```bash
python tests/simple_test.py
```

## Test Environment Setup

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Or install from requirements.txt
pip install -r requirements.txt
```

### Configuration

Tests use the same configuration as the main application but may override certain settings:

```python
# Example test configuration
TEST_CONFIG = {
    "cursor_workspace": "/tmp/test_workspace",
    "log_level": "DEBUG",
    "cursor_timeout": 60,
}
```

## Writing New Tests

### Test Template

```python
"""
Test module for [component name].
"""
import pytest
from src.component import ComponentClass


class TestComponent:
    """Test suite for ComponentClass."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.component = ComponentClass()
    
    def teardown_method(self):
        """Cleanup after tests."""
        pass
    
    def test_basic_functionality(self):
        """Test basic component functionality."""
        result = self.component.do_something()
        assert result is not None
        assert result.status == "success"
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            self.component.invalid_operation()
```

### Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Use descriptive test names
3. **Coverage**: Test both success and failure cases
4. **Fixtures**: Use setup/teardown for common setup
5. **Assertions**: Use specific assertions
6. **Documentation**: Add docstrings to test methods

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Test Coverage

### Generate Coverage Report

```bash
# HTML report
python -m pytest tests/ --cov=src --cov-report=html

# Terminal report
python -m pytest tests/ --cov=src --cov-report=term

# XML report (for CI)
python -m pytest tests/ --cov=src --cov-report=xml
```

### View Coverage

```bash
# Open HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Debugging Tests

### Run with Debug Output

```bash
# Show print statements
python -m pytest tests/ -s

# Show full traceback
python -m pytest tests/ --tb=long

# Stop on first failure
python -m pytest tests/ -x

# Enter debugger on failure
python -m pytest tests/ --pdb
```

### Using Python Debugger

```python
def test_something():
    import pdb; pdb.set_trace()  # Breakpoint
    result = function_to_test()
    assert result == expected
```

## Performance Testing

### Measure Test Execution Time

```bash
# Show slowest tests
python -m pytest tests/ --durations=10

# Profile test execution
python -m pytest tests/ --profile
```

## Common Issues

### Issue: Import Errors

**Solution**: Ensure PYTHONPATH includes project root:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m pytest tests/
```

### Issue: Test Fixtures Not Found

**Solution**: Check `conftest.py` or fixture definitions:
```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value"}
```

### Issue: Async Tests Failing

**Solution**: Install and configure pytest-asyncio:
```bash
pip install pytest-asyncio
```

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

## Test Maintenance

### Regular Tasks

1. **Update tests** when adding new features
2. **Remove obsolete tests** when deprecating features
3. **Refactor tests** to reduce duplication
4. **Review coverage** and add missing tests
5. **Update documentation** when test structure changes

### Code Review Checklist

- [ ] All new code has corresponding tests
- [ ] Tests pass locally
- [ ] Coverage hasn't decreased
- [ ] Tests are well-documented
- [ ] No flaky tests introduced
- [ ] Performance impact is acceptable

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

## Contributing Tests

When contributing tests:

1. Follow existing test structure
2. Use descriptive names
3. Add docstrings
4. Ensure tests are isolated
5. Update this documentation if needed
6. Run full test suite before submitting

---

For questions or issues with testing, please check the logs or open an issue on the project repository.

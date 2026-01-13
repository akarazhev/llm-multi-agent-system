# Test Suite

This directory contains all tests for the LLM Multi-Agent System.

## Quick Start

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_agent.py

# Run with verbose output
python -m pytest tests/ -v
```

## Test Files

- **`simple_test.py`** - Simple workflow tests
- **`test_agent.py`** - Agent functionality tests

## Documentation

For detailed testing information, see [TESTING.md](../docs/TESTING.md).

## Running Individual Tests

Each test file can be run independently:

```bash
python tests/simple_test.py
```

## Requirements

Install test dependencies:

```bash
pip install pytest pytest-cov pytest-asyncio
```

Or use the main requirements file:

```bash
pip install -r requirements.txt
```

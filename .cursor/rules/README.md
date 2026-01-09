# Project Rules & Best Practices

This directory contains all rules and best practices for the LLM Multi-Agent System project.

## Rules Structure

### Python
- **python-best-practices.mdc** - General Python practices, type hints, async/await, error handling

### FastAPI
- **fastapi-best-practices.mdc** - API design, validation, error handling, dependency injection

### LangChain & LangGraph
- **langchain-langgraph-best-practices.mdc** - Workflow design, agent architecture, state management

### Pydantic
- **pydantic-best-practices.mdc** - Model definition, validation, settings management

### Testing
- **testing-best-practices.mdc** - Pytest, async testing, mocking, fixtures

### Code Quality
- **code-quality-standards.mdc** - Black, Ruff, MyPy, pre-commit hooks

### Git
- **git-commit-standards.mdc** - Commit messages, branch naming, PR guidelines

### Architecture
- **architecture-standards.mdc** - Project structure, agent patterns, integration patterns

### Documentation
- **documentation-standards.mdc** - Docstrings, API docs, README guidelines

### Multi-Agent Collaboration
- **multi-agent-collaboration.mdc** - Protocol for multiple agents working together
- **MULTI_AGENT_COLLABORATION_USAGE.md** - Usage guide for collaboration

## Usage

These rules are automatically applied when working with the project through Cursor IDE. They help:

- Maintain code consistency
- Follow best practices
- Ensure code quality
- Simplify code review

## Updating Rules

When updating rules:
1. Update the corresponding file in `.cursor/rules/`
2. Ensure code examples are current
3. Update this README when adding new rules

## Links

- [Python PEP 8](https://pep8.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

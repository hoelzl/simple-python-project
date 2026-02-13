# Development Guidelines

## Test-Driven Development

- **Write tests first**: Before implementing a feature, write tests that define the expected behavior
- **Red-Green-Refactor**: Start with failing tests, make them pass, then refactor
- **Small iterations**: Write one test at a time, make it pass, then write the next

## Test Quality

- **Strong assertions**: Write specific assertions that verify exact expected behavior, not just "it doesn't crash"
- **Test public interfaces**: Don't test implementation details; test through the module/class public API
- **Maintain coverage**: Ensure test coverage remains high when adding new features
- **Independent tests**: Each test should be independent and not rely on other tests or shared mutable state
- **Descriptive names**: Test names should describe the behavior being tested

## Code Quality

- **Clean Code**: Write readable, self-documenting code with meaningful names
- **SOLID Principles**:
  - Single Responsibility: Each class/module should have one reason to change
  - Open/Closed: Open for extension, closed for modification
  - Liskov Substitution: Subtypes must be substitutable for their base types
  - Interface Segregation: Many specific interfaces are better than one general interface
  - Dependency Inversion: Depend on abstractions, not concretions
- **GRASP Patterns**: Apply General Responsibility Assignment principles for object-oriented design
- **Design Patterns**: Use appropriate patterns where they simplify the design, but avoid over-engineering

## Before Committing

Run all pre-commit checks:
```bash
uv run pre-commit run --all-files
```

Or install hooks to run automatically on every commit:
```bash
uv run pre-commit install
```

## Commands

| Command | Description |
|---------|-------------|
| `uv run pytest` | Run tests |
| `uv run tox` | Test against multiple Python versions |
| `uv run ruff check .` | Run linter |
| `uv run ruff format .` | Format code |
| `uv run mypy src/` | Run type checker |
| `uv run pre-commit run --all-files` | Run all pre-commit checks |

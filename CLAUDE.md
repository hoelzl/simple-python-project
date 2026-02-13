# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Copier template** for generating simple Python projects. It is NOT a Python project itself - it generates Python projects when users run `copier copy`.

## Template Structure

- `copier.yml` - Template configuration and user prompts
- `project/` - Template files that get copied to generated projects (via `_subdirectory` setting)
  - `src/{{project_package}}/` - Source code templates
  - `tests/` - Test templates
  - `pyproject.toml.jinja` - Project configuration template
- Files ending in `.jinja` use Jinja2 templating with standard Jinja2 delimiters (`{{ }}` for variables, `{% %}` for blocks)

## Testing the Template

Generate a test project and verify it works:

```shell
# Generate a project (from template root)
copier copy . ../test-output --force

# Test the generated project
cd ../test-output
uv sync --group dev
uv run pytest
```

## Template Variables

Key variables defined in `copier.yml`:
- `project_package` - Python package name (underscores)
- `project_dir` - Directory name (hyphens)
- `cli` - CLI framework choice: none/argparse/click/typer
- `default_dependencies` - Include attrs, cattrs, platformdirs

## Generated Project Commands

Projects generated from this template use:
- `uv run pytest` - Run tests (includes doctests via pytest.ini)
- `uv run tox` - Test against Python 3.11-3.14
- `bumpversion patch|minor|major` - Version management

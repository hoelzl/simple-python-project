# A Copier Template for Simple Python Projects

This is a [Copier](https://copier.readthedocs.io/) template to generate simple Python projects that use **uv** as the recommended package manager, with pip/setuptools as an alternative.

## Features

- Generate a locally installable package
- Configure pytest to run project tests and doctests
- Configure tox (with tox-uv) to test with multiple Python versions
- Configure bumpversion to manage project versions
- Optional CLI framework (none, argparse, click, or typer)
- Optional default dependencies (attrs, cattrs, platformdirs)

## Usage

### Using uv (Recommended)

```shell
# Install copier using uv
uv tool install copier

# Generate a new project
copier copy https://github.com/hoelzl/trivial_python_project my-new-project
```

### Using pip

```shell
# Install copier using pip
pip install copier

# Generate a new project
copier copy https://github.com/hoelzl/trivial_python_project my-new-project
```

Answer the questions about the project configuration and enjoy your awesome new project.

## Template Options

| Option | Description | Default |
|--------|-------------|---------|
| `project_package` | Python package name (use underscores) | `my_awesome_project` |
| `project_name` | Human-readable project name | Derived from package name |
| `project_dir` | Project directory name | Derived from package name |
| `executable_name` | CLI executable name | Same as project_dir |
| `author` | Author name | `Dr. Matthias Hölzl` |
| `email` | Author email | `tc@xantira.com` |
| `description` | Short project description | `An awesome project!` |
| `base_url` | Project repository URL | GitHub URL |
| `cli` | CLI framework (none/argparse/click/typer) | `none` |
| `default_dependencies` | Include attrs, cattrs, platformdirs | `false` |

## Updating Existing Projects

Copier supports updating projects when the template changes:

```shell
cd my-existing-project
copier update
```

This will apply template updates while preserving your local modifications.

## Configuration

Bumpversion is configured to *not* commit the updated files. This is the safer
option but slightly inconvenient. To enable automatic commits, change
`commit = False` to `commit = True` in `.bumpversion.cfg`.

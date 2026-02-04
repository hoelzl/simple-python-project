# Cookiecutter to Copier Migration Guide for Claude Code

This guide provides instructions for Claude Code to convert Cookiecutter project templates to Copier templates. Copier is a modern alternative that supports template updates, better conditional logic, and YAML-based configuration.

---

## Overview

### Key Differences

| Aspect | Cookiecutter | Copier |
|--------|-------------|--------|
| Config file | `cookiecutter.json` | `copier.yml` or `copier.yaml` |
| Template directory | `{{cookiecutter.var}}` | `{{var}}` (no namespace prefix) |
| File suffix | None (all files templated) | `.jinja` suffix for templated files |
| Variable access | `{{cookiecutter.var}}` | `{{var}}` |
| Settings prefix | N/A | Underscore prefix (`_tasks`, `_exclude`) |
| Hooks | `hooks/pre_gen_project.py` | `_tasks` in copier.yml |
| Template updates | Not supported | Built-in with `copier update` |
| Answers file | None | `.copier-answers.yml` (auto-generated) |

---

## Migration Steps

### Step 1: Analyze the Cookiecutter Template

First, examine the existing cookiecutter structure:

```bash
# List the template structure
find . -type f -name "*.json" -o -name "*.py" | head -20
cat cookiecutter.json
ls -la hooks/ 2>/dev/null || echo "No hooks directory"
```

Identify:
1. All variables in `cookiecutter.json`
2. Any hooks in `hooks/` directory
3. Conditional logic patterns in templates
4. Derived/computed variables

### Step 2: Create the Copier Configuration

Create `copier.yml` in the template root. This replaces `cookiecutter.json`.

#### Basic Variable Conversion

**Cookiecutter (`cookiecutter.json`):**
```json
{
    "project_name": "My Project",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_') }}",
    "author": "Your Name",
    "email": "your@email.com",
    "version": "0.1.0",
    "use_docker": "n"
}
```

**Copier (`copier.yml`):**
```yaml
# Questions (no underscore prefix)
project_name:
  type: str
  help: What is your project name?
  default: My Project

project_slug:
  type: str
  help: Project slug (used for package name)
  default: "{{ project_name | lower | replace(' ', '_') }}"

author:
  type: str
  help: Author name
  default: Your Name

email:
  type: str
  help: Author email
  default: your@email.com

version:
  type: str
  help: Initial version
  default: "0.1.0"

use_docker:
  type: bool
  help: Include Docker configuration?
  default: false
```

#### Variable Type Mapping

| Cookiecutter | Copier |
|--------------|--------|
| String value | `type: str` |
| `["option1", "option2"]` (list) | `type: str` with `choices:` |
| `"y"` / `"n"` | `type: bool` |
| Integer string | `type: int` |
| Nested dict | `type: yaml` or `type: json` |

#### Choice Variables

**Cookiecutter:**
```json
{
    "license": ["MIT", "BSD-3", "Apache-2.0", "Proprietary"]
}
```

**Copier:**
```yaml
license:
  type: str
  help: Choose a license
  choices:
    - MIT
    - BSD-3
    - Apache-2.0
    - Proprietary
  default: MIT
```

#### Computed/Derived Variables

Copier supports Jinja2 in default values. Use `[[ ]]` syntax for templated defaults (different from file templating which uses `{{ }}`).

**Copier:**
```yaml
project_name:
  type: str
  default: My Project

# Derived from project_name
project_slug:
  type: str
  default: "[[ project_name | lower | replace(' ', '_') | replace('-', '_') ]]"
  help: Python package name (auto-generated from project name)

# Module name derived from slug
module_name:
  type: str
  default: "[[ project_slug ]]"
```

Note: The `[[ ]]` syntax is used in `copier.yml` for templating within the config file itself. This is because Copier uses different delimiters to distinguish config-time templating from file-content templating.

### Step 3: Rename and Restructure Template Directory

#### Directory Renaming

**Cookiecutter structure:**
```
my-template/
├── cookiecutter.json
├── hooks/
│   ├── pre_gen_project.py
│   └── post_gen_project.py
└── {{cookiecutter.project_slug}}/
    ├── {{cookiecutter.module_name}}/
    │   └── __init__.py
    ├── setup.py
    └── README.md
```

**Copier structure:**
```
my-template/
├── copier.yml
├── {{project_slug}}/              # Remove 'cookiecutter.' prefix
│   ├── {{module_name}}/           # Remove 'cookiecutter.' prefix
│   │   └── __init__.py.jinja      # Add .jinja suffix to templated files
│   ├── setup.py.jinja
│   └── README.md.jinja
└── {{_copier_conf.answers_file}}.jinja  # Add answers file template
```

#### Commands for Renaming

```bash
# Rename directories - remove 'cookiecutter.' prefix
# Use a script or manual renaming as shell glob expansion varies

# Example: rename {{cookiecutter.project_slug}} to {{project_slug}}
find . -type d -name '*{{cookiecutter.*' | while read dir; do
    newname=$(echo "$dir" | sed 's/{{cookiecutter\./{{/g')
    mv "$dir" "$newname"
done
```

### Step 4: Update Template Files

#### Remove `cookiecutter.` Prefix from Variables

In all template files, replace `cookiecutter.` with nothing:

**Before (Cookiecutter):**
```python
# {{cookiecutter.project_slug}}/__init__.py
"""{{ cookiecutter.project_name }}."""

__version__ = "{{ cookiecutter.version }}"
__author__ = "{{ cookiecutter.author }}"
```

**After (Copier):**
```python
# {{project_slug}}/__init__.py.jinja
"""{{ project_name }}."""

__version__ = "{{ version }}"
__author__ = "{{ author }}"
```

#### Add `.jinja` Suffix to Templated Files

Files containing Jinja2 syntax need the `.jinja` suffix (Copier strips this during generation):

```bash
# Find files with Jinja syntax and rename them
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.cfg" -o -name "*.toml" -o -name "*.yml" -o -name "*.yaml" \) | while read file; do
    if grep -q '{{' "$file" || grep -q '{%' "$file"; then
        mv "$file" "${file}.jinja"
    fi
done
```

**Important:** Files without Jinja syntax should NOT have the `.jinja` suffix. They will be copied as-is.

#### Batch Variable Replacement

```bash
# Replace all occurrences of cookiecutter. prefix in files
find . -type f \( -name "*.jinja" -o -name "*.py" -o -name "*.md" \) -exec sed -i 's/cookiecutter\.//g' {} \;
```

### Step 5: Convert Hooks to Tasks

Copier uses `_tasks` instead of hook scripts.

#### Pre-generation Hooks

Copier doesn't have a direct equivalent of `pre_gen_project.py`. Instead:
- Use validators on questions
- Use `when` conditions on questions
- Use `_exclude` to conditionally exclude files

**Cookiecutter `hooks/pre_gen_project.py`:**
```python
import sys

project_slug = '{{ cookiecutter.project_slug }}'
if not project_slug.isidentifier():
    print(f"ERROR: {project_slug} is not a valid Python identifier!")
    sys.exit(1)
```

**Copier equivalent in `copier.yml`:**
```yaml
project_slug:
  type: str
  validator: "{% if not project_slug.isidentifier() %}Must be a valid Python identifier{% endif %}"
```

#### Post-generation Hooks

**Cookiecutter `hooks/post_gen_project.py`:**
```python
import os
import subprocess

# Initialize git
subprocess.run(["git", "init"])
subprocess.run(["git", "add", "."])

# Remove optional files
if '{{ cookiecutter.use_docker }}' != 'y':
    os.remove('Dockerfile')
    os.remove('docker-compose.yml')
```

**Copier equivalent in `copier.yml`:**
```yaml
use_docker:
  type: bool
  default: false

# Settings (underscore prefix)
_tasks:
  # Initialize git repository
  - command: git init
    when: "{{ _copier_conf.src_path }}"  # Always runs
  - command: git add .

# Conditional file exclusion (preferred over post-deletion)
_exclude:
  - "{% if not use_docker %}Dockerfile{% endif %}"
  - "{% if not use_docker %}docker-compose.yml{% endif %}"
```

### Step 6: Add the Answers File Template

Create `{{_copier_conf.answers_file}}.jinja` in the template root:

```yaml
# This file is auto-generated by Copier; do not edit manually.
# Changes to this file will be overwritten by `copier update`.
{{ _copier_answers | to_nice_yaml }}
```

This file stores answers for future updates.

### Step 7: Configure Template Settings

Add configuration options to `copier.yml`:

```yaml
# Template settings (all start with underscore)
_min_copier_version: "9.0.0"

_subdirectory: template  # If template files are in a subdirectory

_templates_suffix: .jinja  # Default, can be changed

_exclude:
  # Always exclude these
  - copier.yml
  - "*.pyc"
  - __pycache__
  - .git
  # Conditional exclusions
  - "{% if not use_docker %}Dockerfile{% endif %}"
  - "{% if not use_docker %}docker-compose.yml{% endif %}"

_skip_if_exists:
  # Don't overwrite these on update
  - ".env"
  - "*.local.*"

_tasks:
  - command: git init
    when: "{{ not _copier_conf.dst_path.joinpath('.git').exists() }}"
  - "pip install -e .[dev]"

_message_after_copy: |
  Your project "{{ project_name }}" has been created!
  
  Next steps:
    cd {{ project_slug }}
    git add .
    git commit -m "Initial commit"

_message_after_update: |
  Your project has been updated from the template.
  Please review changes and resolve any conflicts.
```

### Step 8: Handle Conditional Files and Directories

#### Method 1: Conditional File Names (Recommended)

Name files/directories with Jinja conditions:

```
{% if use_docker %}Dockerfile{% endif %}.jinja
{% if use_docker %}docker-compose.yml{% endif %}.jinja
{% if ci_system == 'github' %}.github{% endif %}/workflows/ci.yml.jinja
```

#### Method 2: Using `_exclude`

```yaml
_exclude:
  - "{% if not use_docker %}Dockerfile{% endif %}"
  - "{% if not use_docker %}docker-compose.yml{% endif %}"
  - "{% if ci_system != 'github' %}.github{% endif %}"
```

### Step 9: Test the Converted Template

```bash
# Install copier
pip install copier

# Test generation
copier copy /path/to/template /tmp/test-project

# Test with specific answers
copier copy --data project_name="Test" --data use_docker=true /path/to/template /tmp/test-project

# Test update functionality (requires git tags on template)
cd /tmp/test-project
copier update
```

---

## Complete Example Conversion

### Original Cookiecutter Template

**`cookiecutter.json`:**
```json
{
    "project_name": "My Python Project",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}",
    "project_dir": "{{ cookiecutter.project_slug }}",
    "author": "Author Name",
    "email": "author@example.com",
    "description": "A short description",
    "version": "0.1.0",
    "python_version": ["3.11", "3.12", "3.10"],
    "use_pytest": "y",
    "license": ["MIT", "BSD-3-Clause", "Apache-2.0"]
}
```

**Structure:**
```
trivial_python_project/
├── cookiecutter.json
├── hooks/
│   └── post_gen_project.py
└── {{cookiecutter.project_dir}}/
    ├── {{cookiecutter.project_slug}}/
    │   └── __init__.py
    ├── tests/
    │   └── __init__.py
    ├── pyproject.toml
    ├── README.md
    └── LICENSE
```

### Converted Copier Template

**`copier.yml`:**
```yaml
# Copier template configuration
# Converted from Cookiecutter

_min_copier_version: "9.0.0"

# Questions
project_name:
  type: str
  help: What is your project name?
  default: My Python Project

project_slug:
  type: str
  help: Project slug (Python package name)
  default: "[[ project_name | lower | replace(' ', '_') | replace('-', '_') ]]"
  validator: "{% if not project_slug.isidentifier() %}Must be a valid Python identifier{% endif %}"

project_dir:
  type: str
  help: Project directory name
  default: "[[ project_slug ]]"

author:
  type: str
  help: Author name
  default: Author Name

email:
  type: str
  help: Author email
  default: author@example.com

description:
  type: str
  help: Short project description
  default: A short description

version:
  type: str
  help: Initial version
  default: "0.1.0"

python_version:
  type: str
  help: Minimum Python version
  choices:
    - "3.12"
    - "3.11"
    - "3.10"
  default: "3.11"

use_pytest:
  type: bool
  help: Include pytest configuration?
  default: true

license:
  type: str
  help: Choose a license
  choices:
    - MIT
    - BSD-3-Clause
    - Apache-2.0
  default: MIT

# Settings
_exclude:
  - copier.yml
  - "*.pyc"
  - __pycache__
  - "{% if not use_pytest %}tests{% endif %}"
  - "{% if not use_pytest %}pytest.ini{% endif %}"

_skip_if_exists:
  - ".env"

_tasks:
  - command: git init
    when: "{{ not _copier_conf.dst_path.joinpath('.git').exists() }}"
  - git add .

_message_after_copy: |
  
  ✨ Project "{{ project_name }}" created successfully!
  
  Next steps:
    cd {{ project_dir }}
    python -m venv .venv
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
    pip install -e ".[dev]"
    git commit -m "Initial commit"
```

**Structure:**
```
trivial_python_project/
├── copier.yml
├── {{project_dir}}/
│   ├── {{project_slug}}/
│   │   └── __init__.py.jinja
│   ├── {% if use_pytest %}tests{% endif %}/
│   │   └── __init__.py
│   ├── pyproject.toml.jinja
│   ├── README.md.jinja
│   └── LICENSE.jinja
└── {{_copier_conf.answers_file}}.jinja
```

---

## Migration Checklist

Use this checklist when converting each template:

- [ ] **Analyze** the cookiecutter.json and document all variables
- [ ] **Create** copier.yml with all questions and proper types
- [ ] **Convert** choice lists to `choices:` with proper syntax  
- [ ] **Convert** y/n strings to `type: bool`
- [ ] **Add** `help:` text for each question
- [ ] **Add** `validator:` where input validation is needed
- [ ] **Rename** template directory (remove `{{cookiecutter.` prefix)
- [ ] **Rename** all subdirectories (remove `{{cookiecutter.` prefix)
- [ ] **Add** `.jinja` suffix to all files containing Jinja2 syntax
- [ ] **Replace** `cookiecutter.` prefix in all file contents
- [ ] **Convert** hooks to `_tasks` or `_exclude`
- [ ] **Add** `{{_copier_conf.answers_file}}.jinja` file
- [ ] **Configure** `_exclude` for conditional files
- [ ] **Configure** `_skip_if_exists` for user-customized files
- [ ] **Add** `_message_after_copy` with next steps
- [ ] **Test** template generation with `copier copy`
- [ ] **Test** with various answer combinations
- [ ] **Tag** the template repo for versioning (enables `copier update`)

---

## Copier-Specific Features to Consider Adding

After basic conversion, consider enhancing the template with Copier-specific features:

### Migrations

Allow existing projects to update when the template changes:

```yaml
_migrations:
  - version: "2.0.0"
    before:
      - rm -rf old_directory
    after:
      - echo "Migration to v2.0.0 complete"
```

### Multi-select Questions

```yaml
features:
  type: str
  multiselect: true
  choices:
    - Docker
    - CI/CD
    - Documentation
    - Pre-commit hooks
  default:
    - Pre-commit hooks
```

### Conditional Questions

```yaml
use_database:
  type: bool
  default: false

database_type:
  type: str
  when: "{{ use_database }}"
  choices:
    - PostgreSQL
    - MySQL
    - SQLite
```

### External Data

```yaml
_external_data:
  - source: https://api.github.com/gitignore/templates/Python
    dest: .gitignore.template
```

---

## Common Pitfalls

1. **Forgetting `.jinja` suffix**: Files without this suffix won't be templated
2. **Using `{{ }}` in copier.yml defaults**: Use `[[ ]]` for config-time templating
3. **Not escaping existing Jinja in target files**: If the generated project uses Jinja (e.g., Ansible), use `{% raw %}...{% endraw %}`
4. **Forgetting the answers file**: Always include `{{_copier_conf.answers_file}}.jinja`
5. **Invalid Python identifiers**: Add validators for package names
6. **Missing `_min_copier_version`**: Ensures users have compatible Copier version

---

## References

- [Copier Documentation](https://copier.readthedocs.io/)
- [Copier Configuration Reference](https://copier.readthedocs.io/en/stable/configuring/)
- [Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)

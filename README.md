# odoo-addons-path

Automatically detect and construct Odoo `addons_path` for various project layouts.

## Problem

Different Odoo project frameworks use different directory structures:
- Trobz, Camptocamp, Odoo.sh, Doodba each have unique layouts
- Manual configuration is error-prone and time-consuming
- Developers need consistent `addons_path` across team projects

## Solution

`odoo-addons-path` auto-detects your project layout and generates the correct configuration:

```bash
$ odoo-addons-path /home/project
/home/project/odoo/addons,/home/project/addons/repo1,/home/project/addons/repo2
```

## Installation

```bash
pip install odoo-addons-path
```

## Quick Start

### CLI Usage

```bash
# Auto-detect layout (detector runs)
odoo-addons-path /path/to/your/odoo/project

# With verbose output (categorized paths)
odoo-addons-path /path/to/project --verbose

# Project given + explicit dirs - detector runs, explicit dirs are added to its result
odoo-addons-path /path/to/project --addons-dir "./addons/*/18.0, ./custom"
odoo-addons-path /path/to/project --odoo-dir /opt/odoo

# No project given - detector SKIPPED (uses explicit paths only)
odoo-addons-path --odoo-dir /opt/odoo --addons-dir "./custom"

# Use environment variable with auto-detection
export CODEBASE=/home/project
odoo-addons-path
```

**Detection Behavior:** Layout detection runs only on a project path given explicitly, as an argument or through the `CODEBASE` environment variable. The current directory is never detected implicitly. Without a project path, the output is built only from `--addons-dir`/`--odoo-dir`. With neither a project path nor any explicit dir, the command prints an error and exits with status 1.

### Programmatic Usage

```python
from pathlib import Path
from odoo_addons_path import get_addons_path

# Auto-detect layout
paths = get_addons_path(Path("/path/to/project"))
print(paths)
# Output: /path/to/project/addons,/path/to/project/enterprise

# With options
paths = get_addons_path(
    codebase=Path("/home/project"),
    addons_dir=[Path("/home/project/custom")],
    verbose=True
)
```

## Supported Layouts

Auto-detects these Odoo project organizational patterns:

| Layout | Marker | Detection | Status |
|--------|--------|-----------|--------|
| **Trobz** | `.trobz/` directory | Explicit marker | ✓ Supported |
| **Camptocamp (C2C)** | Dockerfile with label | File content | ✓ Supported |
| **Odoo.sh** | 4-dir structure | Directory check | ✓ Supported |
| **Doodba** | `.copier-answers.yml` | YAML config | ✓ Supported |
| **Generic** | Any `__manifest__.py` | Recursive search | ✓ Fallback |

See `tests/data/` directory for layout examples.

## Features

- **Zero Configuration:** Works out-of-the-box for standard layouts
- **Multiple Interfaces:** CLI tool and Python library
- **Flexible Input:** Glob patterns, comma-separated paths, environment variables
- **Type Safe:** Full Python type hints
- **Well Tested:** 5 real-world layout patterns covered
- **Production Ready:** Used in multiple Odoo teams

## Documentation

- **[Project Overview & PDR](docs/project-overview-pdr.md)** - Vision, goals, and requirements
- **[System Architecture](docs/system-architecture.md)** - Design patterns and data flow
- **[Code Standards](docs/code-standards.md)** - Development guidelines and conventions
- **[Codebase Summary](docs/codebase-summary.md)** - Module structure and components
- **[Deployment Guide](docs/deployment-guide.md)** - Release and deployment procedures
- **[Contributing](CONTRIBUTING.md)** - How to contribute to the project

## Development

### Setup

```bash
uv sync
uv run pre-commit install
```

### Testing

```bash
# Single version
make test

# All supported versions (3.10-3.13)
tox

# Quality checks
make check
```

### Release

Releases are automated via semantic versioning on merge to main:

```bash
git commit -m "feat: add new feature"  # Creates MINOR version
git commit -m "fix: bug fix"           # Creates PATCH version
git commit -m "feat!: breaking change" # Creates MAJOR version
```

## Requirements

- Python 3.10+
- pyyaml
- typer >= 0.19.2

## Status

**v1.0.0** - Stable release (Nov 25, 2025)

See [CHANGELOG.md](CHANGELOG.md) for version history.

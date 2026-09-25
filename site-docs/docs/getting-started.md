# Getting Started

## Installation

```bash
# Recommended: install as a global tool
uv tool install odoo-addons-path

# Or with pip
pip install odoo-addons-path
```

## Basic Usage

Point it at your Odoo project root — it auto-detects the layout:

```bash
odoo-addons-path /path/to/your/odoo/project
```

**Output:**

```
/home/project/odoo/addons,/home/project/addons/repo1,/home/project/addons/repo2
```

## CLI Options

```bash
# Verbose output — shows categorized paths
odoo-addons-path /path/to/project --verbose

# Project given + explicit dirs — detector runs, explicit dirs are merged into its result
odoo-addons-path /path/to/project --addons-dir "./addons/*/18.0,./custom"
odoo-addons-path /path/to/project --odoo-dir /opt/odoo

# No project given — detector SKIPPED (uses explicit paths only)
odoo-addons-path --odoo-dir /opt/odoo --addons-dir "./custom"
```

!!! note "Detection Behavior"
    Layout detection runs only on a project path given explicitly — as the CLI argument or through the `CODEBASE` environment variable. The current directory is never detected implicitly.

    Without a project path, the output is built only from `--addons-dir`/`--odoo-dir`. With neither a project path nor any explicit dir, the command prints an error to stderr and exits with status 1.

## Environment Variable

```bash
export CODEBASE=/home/project
odoo-addons-path  # uses $CODEBASE automatically
```

## Python API

```python
from pathlib import Path
from odoo_addons_path import get_addons_path

# Auto-detect layout
paths = get_addons_path(Path("/path/to/project"))
print(paths)
# /path/to/project/addons,/path/to/project/enterprise

# With explicit options
paths = get_addons_path(
    codebase=Path("/home/project"),
    addons_dir=[Path("/home/project/custom")],
    verbose=True,
)

# codebase=None skips detection — only addons_dir/odoo_dir are used
paths = get_addons_path(
    codebase=None,
    odoo_dir=Path("/opt/odoo"),
    addons_dir=[Path("/home/project/custom")],
)
```

## Next Steps

- [Supported Layouts](supported-layouts.md) — see which project structures are auto-detected
- [API Reference](api-reference.md) — full CLI flags and Python API docs

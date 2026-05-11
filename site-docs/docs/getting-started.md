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

# Explicit addons dir — detector is SKIPPED
odoo-addons-path /path/to/project --addons-dir "./addons/*/18.0,./custom"

# Explicit Odoo dir — detector is SKIPPED
odoo-addons-path /path/to/project --odoo-dir /opt/odoo

# Both explicit paths
odoo-addons-path /path/to/project --odoo-dir /opt/odoo --addons-dir "./custom"
```

!!! note "Detector Skip Behavior"
    The layout detector is skipped when **any** explicit `--addons-dir` or `--odoo-dir` is provided.
    This ensures predictable, reproducible output when you specify paths manually.

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
```

## Next Steps

- [Supported Layouts](supported-layouts.md) — see which project structures are auto-detected
- [API Reference](api-reference.md) — full CLI flags and Python API docs

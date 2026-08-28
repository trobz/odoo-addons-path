---
name: odoo-addons-path
description: Construct Odoo addons-path for CLI. Use when running Odoo test instance, setting up --addons-path, or auto-detecting addon directories. Supports c2c, doodba, odoo.sh, trobz layouts. If user provides path, use directly; otherwise run odoo-addons-path to auto-detect.
---

# Odoo Addons Path

Auto-detect and construct `--addons-path` for Odoo CLI across different project layouts.

## Quick Start

```bash
# Auto-detect addons path in current directory
odoo-addons-path .

# Auto-detect with verbose output
odoo-addons-path --verbose /path/to/project

# Custom addon directory pattern
odoo-addons-path --addons-dir "./addons/*/18.0" /path/to/project
```

## Workflow: Constructing --addons-path

1. **User provides path** → Use directly as `--addons-path`
2. **User doesn't provide path** → Run auto-detection:
   ```bash
   odoo-addons-path /path/to/project
   ```
3. Use output for Odoo CLI: `odoo-v{major} --addons-path=$(odoo-addons-path .)`

## CLI Options

| Option | Description |
|--------|-------------|
| `CODEBASE` | Project path (positional arg, default: `.`) |
| `--addons-dir` | Custom addon dir patterns (globs, comma-separated) |
| `--odoo-dir` | Path to Odoo source code |
| `--verbose`, `-v` | Show detailed detection output |

## Usage Examples

```bash
# Basic detection
odoo-addons-path ~/code/odoo/project

# Multiple custom directories
odoo-addons-path --addons-dir "./external-src/,./custom/" ~/project

# Version-specific modules
odoo-addons-path --addons-dir "./repos/*/18.0" ~/project

# Use in Odoo command
odoo-v18 -d testdb --addons-path=$(odoo-addons-path .)
```

## Python API

```python
from pathlib import Path
from odoo_addons_path import get_addons_path

addons_path = get_addons_path(Path("/path/to/project"))
```

## Env Variable

Set `CODEBASE` env var as alternative to positional argument:
```bash
export CODEBASE=/path/to/project
odoo-addons-path
```

## Module Resolution

When a specific module is needed, resolve its location using pwd-first discovery:

1. **Check pwd for module directory** — look for `./{module_name}/` or `./{subdir}/{module_name}/` (one level of subdirectories)
2. **If found** → include the parent directory in `--addons-path`
3. **If NOT found** → ask the user via `AskUserQuestion`:
   > "Module '{name}' not found in current directory. Where is the folder containing this module?"
4. **Validate** that the user-provided path contains the module (i.e. `{path}/{module_name}/` exists)
5. **Return** the complete `--addons-path` including all discovered paths

**Example:**
```bash
# pwd contains ./my_module/ → resolved automatically
odoo-addons-path .
# Output includes . in --addons-path

# pwd contains ./third_party/my_module/ → resolved via one-level subdir scan
odoo-addons-path .
# Output includes ./third_party in --addons-path
```

## References

- [Supported Layouts](references/layouts.md) - c2c, doodba, odoo.sh, trobz patterns
- [GitHub Repository](https://github.com/trobz/odoo-addons-path)

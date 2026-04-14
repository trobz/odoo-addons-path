# API Reference

## CLI

```
odoo-addons-path [CODEBASE] [OPTIONS]
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `CODEBASE` | Path to the Odoo project root | `$CODEBASE` env var |

### Options

| Option | Type | Description |
|--------|------|-------------|
| `--addons-dir` | `TEXT` | Comma-separated glob patterns for addon directories. Skips detector. |
| `--odoo-dir` | `TEXT` | Path to Odoo source directory. Skips detector. |
| `--verbose` | flag | Show categorized path breakdown |
| `--help` | flag | Show help message |

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (no codebase provided, path not found, etc.) |

---

## Python API

### `get_addons_path`

```python
from odoo_addons_path import get_addons_path

result: str = get_addons_path(
    codebase: Path,
    addons_dir: list[Path] | None = None,
    odoo_dir: Path | None = None,
    verbose: bool = False,
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `codebase` | `Path` | Root directory of the Odoo project |
| `addons_dir` | `list[Path] \| None` | Explicit addon paths — skips detector |
| `odoo_dir` | `Path \| None` | Explicit Odoo source path — skips detector |
| `verbose` | `bool` | Print categorized paths to stdout |

**Returns:** Comma-separated string of addon paths, ready for `odoo.conf`.

**Example:**

```python
from pathlib import Path
from odoo_addons_path import get_addons_path

addons_path = get_addons_path(Path("/srv/odoo/project"))
# "/srv/odoo/project/odoo/addons,/srv/odoo/project/addons/mymodule"
```

---

## Source Modules

| Module | Purpose |
|--------|---------|
| `odoo_addons_path.cli` | Typer CLI entry point |
| `odoo_addons_path.main` | Core orchestration and path aggregation |
| `odoo_addons_path.detector` | Layout detectors (Chain of Responsibility) |
| `odoo_addons_path.__init__` | Public API — exports `get_addons_path` |

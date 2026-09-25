# API Reference

## CLI

```
odoo-addons-path [CODEBASE] [OPTIONS]
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `CODEBASE` | Path to the Odoo project whose layout should be detected. Optional — omit it (and `$CODEBASE`) to skip detection and use only `--addons-dir`/`--odoo-dir`. | `None`, or `$CODEBASE` env var |

### Options

| Option | Type | Description |
|--------|------|-------------|
| `--addons-dir` | `TEXT` | Comma-separated glob patterns for addon directories. Merged with the detected layout when `CODEBASE` is given; used alone otherwise. |
| `--odoo-dir` | `TEXT` | Path to Odoo source directory. Merged with the detected layout when `CODEBASE` is given; used alone otherwise. |
| `--verbose` | flag | Show categorized path breakdown |
| `--help` | flag | Show help message |

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (no `CODEBASE`, `--addons-dir`, or `--odoo-dir` given at all; path not found; etc.) |

---

## Python API

### `get_addons_path`

```python
from odoo_addons_path import get_addons_path

result: str = get_addons_path(
    codebase: Path | None,
    addons_dir: list[Path] | None = None,
    odoo_dir: Path | None = None,
    verbose: bool = False,
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `codebase` | `Path \| None` | Root directory of the Odoo project. Required (pass `None` explicitly to skip it) — `None` skips layout detection and builds the result from `addons_dir`/`odoo_dir` only. |
| `addons_dir` | `list[Path] \| None` | Explicit addon paths, merged with any detected layout |
| `odoo_dir` | `Path \| None` | Explicit Odoo source path, merged with any detected layout |
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

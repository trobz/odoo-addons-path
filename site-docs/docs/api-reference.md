# API Reference

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

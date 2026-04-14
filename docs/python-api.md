# Python API

`odoo-addons-path` exposes a public Python API for use in scripts, configuration generators, and CI tooling.

## Installation

```bash
pip install odoo-addons-path
# or
uv add odoo-addons-path
```

---

## Public Exports

```python
from odoo_addons_path import (
    get_addons_path,
    detect_codebase_layout,
    get_odoo_version,
    get_odoo_version_from_addons,
    get_odoo_version_from_release,
    check_version_consistency,
    app,  # Typer CLI app instance
)
```

---

## `get_addons_path()`

Main entry point. Returns a comma-separated string of absolute addon paths.

```python
from pathlib import Path
from odoo_addons_path import get_addons_path

result: str = get_addons_path(
    codebase: Path,
    addons_dir: list[Path] | None = None,
    odoo_dir: Path | None = None,
    verbose: bool = False,
    detected_paths: dict | None = None,
) -> str
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `codebase` | `Path` | Root of the Odoo project |
| `addons_dir` | `list[Path] \| None` | Explicit addon directories; skips auto-detection |
| `odoo_dir` | `Path \| None` | Explicit Odoo source directory; skips auto-detection |
| `verbose` | `bool` | Print categorised breakdown to stdout |
| `detected_paths` | `dict \| None` | Pre-computed detection result (avoids re-running detector) |

### Returns

A comma-separated string of absolute paths, e.g.:

```
/home/dev/project/odoo/addons,/home/dev/project/addons/custom
```

### Examples

```python
from pathlib import Path
from odoo_addons_path import get_addons_path

# Auto-detect layout
paths = get_addons_path(Path("/home/dev/myproject"))
print(paths)

# Explicit addon directory (skips detection)
paths = get_addons_path(
    Path("/home/dev/myproject"),
    addons_dir=[Path("/home/dev/myproject/custom")],
)

# Verbose — prints breakdown to stdout and returns the string
paths = get_addons_path(Path("/home/dev/myproject"), verbose=True)

# Reuse a previously computed detection result
from odoo_addons_path import detect_codebase_layout
detected = detect_codebase_layout(Path("/home/dev/myproject"))
paths = get_addons_path(Path("/home/dev/myproject"), detected_paths=detected)
```

---

## `detect_codebase_layout()`

Run the detector chain and return the detected layout paths. Useful when you need to inspect
the layout before computing the full path string.

```python
from pathlib import Path
from odoo_addons_path import detect_codebase_layout

layout: dict = detect_codebase_layout(
    codebase: Path,
    verbose: bool = False,
) -> dict
```

### Returns

A dict with some subset of these keys (depending on the detected layout):

```python
{
    "odoo_dir": [Path(...)],       # detected Odoo source directories
    "addons_dirs": [Path(...)],    # addon search root directories
    "addons_dir": [Path(...)],     # single addon directory (some layouts)
}
```

!!! warning "Exit on failure"
    If no layout is detected and the Generic fallback also finds no manifests,
    `detect_codebase_layout()` calls `sys.exit(1)`.

---

## `get_odoo_version()`

Detect the Odoo major version for a resolved addons path string.
Tries `odoo/release.py` first, falls back to manifest scanning.

```python
from odoo_addons_path import get_odoo_version

version: str | None = get_odoo_version(
    addons_path: str,
    odoo_dir: Path | None = None,
    detected_paths: dict | None = None,
) -> str | None
```

Returns `"18.0"`, `"17.0"`, etc., or `None` if no version can be determined.

---

## `get_odoo_version_from_release()`

Extract the Odoo version from `odoo/release.py` directly.

```python
from pathlib import Path
from odoo_addons_path import get_odoo_version_from_release

version: str | None = get_odoo_version_from_release(odoo_dir: Path) -> str | None
```

---

## `get_odoo_version_from_addons()`

Infer the Odoo version by scanning `__manifest__.py` files and returning
the most common major version (majority vote).

```python
from odoo_addons_path import get_odoo_version_from_addons

version: str | None = get_odoo_version_from_addons(addons_path: str) -> str | None
```

---

## `check_version_consistency()`

Detect version mismatches across all addons in a path string.
Returns a mapping of version → addon names. Empty dict means no issues found.

```python
from odoo_addons_path import check_version_consistency

result: dict[str, list[str]] = check_version_consistency(addons_path: str)

# Example result when mismatches exist:
# {
#     "17.0": ["addon_a", "addon_b"],
#     "18.0": ["addon_c"],
# }
```

---

## Complete Example

```python
from pathlib import Path
from odoo_addons_path import (
    get_addons_path,
    get_odoo_version,
    check_version_consistency,
)

project = Path("/home/dev/myproject")

# Resolve paths
addons_path = get_addons_path(project)
print(f"addons_path = {addons_path}")

# Detect version
version = get_odoo_version(addons_path)
print(f"Odoo version: {version}")

# Check for mismatches
mismatches = check_version_consistency(addons_path)
if mismatches:
    for ver, addons in mismatches.items():
        print(f"  {ver}: {', '.join(addons)}")
else:
    print("All addons consistent.")
```

# odoo-addons-path

A tool to auto-detect and construct Odoo `addons_path` for various project layouts.

## Install

```bash
pip install odoo-addons-path
```

## Quick start

### As a CLI tool

```bash
odoo-addons-path /path/to/your/odoo/project
```

**Note:** The path to the codebase can also be set via the `CODEBASE` environment variable.

### As a library

```python
from pathlib import Path
from odoo_addons_path import get_addons_path

addons_path = get_addons_path(Path("/path/to/your/odoo/project"))
print(addons_path)
```

## Codebase layouts supported

There are several out-of-the-box supported layouts:

- `c2c`
- `doodba`
- `odoo.sh`
- `trobz`

For more details on the layouts, please refer to the `tests/data/` directory.

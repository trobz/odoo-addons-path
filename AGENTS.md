# AGENTS.md

> Quick reference for AI coding agents.

## Project

- **Type**: CLI (Typer)
- **Language**: Python 3.10+
- **Package manager**: [uv](https://docs.astral.sh/uv/)

## Source Layout

```
src/odoo_addons_path/
├── __init__.py   — Public API (app, get_addons_path)
├── cli.py        — CLI interface (Typer)
├── main.py       — Core orchestration & path aggregation
└── detector.py   — Layout detection (Chain of Responsibility)
```

## Architecture

Detection: Chain of Responsibility — `TrobzDetector` → `C2CDetector` → `OdooShDetector` → `DoodbaDetector` → `GenericDetector` (fallback)

Detector is **skipped** when ANY explicit `--addons-dir` or `--odoo-dir` is provided.

## Public API

```python
from odoo_addons_path import get_addons_path
result = get_addons_path(codebase, addons_dir=None, odoo_dir=None, verbose=False)  # -> str
```

## Commands

Run `make help` for all commands. Key ones:

```
uv sync        # Install deps
make install   # Install deps + pre-commit hooks
make check     # Lint, format, type-check
make test      # Run pytest
tox            # Multi-Python testing (3.10–3.13)
```

## Key Files

- `Makefile` — Project commands
- `pyproject.toml` — Dependencies and build config
- `ruff.toml` — Linter/formatter rules
- `tests/` — Test suite (pytest)
- `tests/data/` — Real Odoo layout fixtures (`trobz`, `c2c`, `c2c-new`, `doodba`, `odoo-sh`, `repo-version-module`)

## Extending

To add a new layout detector: subclass `CodeBaseDetector` in `detector.py`, implement `detect()`, insert into the chain in `main.py::_detect_codebase_layout()`.

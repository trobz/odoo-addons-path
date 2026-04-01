# Contributing

## Setup

```bash
git clone https://github.com/trobz/odoo-addons-path
cd odoo-addons-path
uv sync
make install   # install deps + pre-commit hooks
```

## Development Commands

```bash
make check     # lint, format, type-check
make test      # run pytest
tox            # multi-Python testing (3.10–3.13)
```

## Adding a Layout Detector

1. Open `src/odoo_addons_path/detector.py`
2. Subclass `CodeBaseDetector` and implement `detect()`
3. Insert your detector into the chain in `main.py::_detect_codebase_layout()`
4. Add a fixture in `tests/data/` matching the new layout
5. Write tests covering detection and path output

```python
class MyLayoutDetector(CodeBaseDetector):
    def detect(self, codebase: Path) -> DetectionResult | None:
        marker = codebase / ".my-marker"
        if not marker.exists():
            return None
        # return paths...
```

## Commit Convention

Releases are automated via semantic versioning:

```bash
git commit -m "feat: add new layout detector"   # MINOR bump
git commit -m "fix: handle missing manifest"     # PATCH bump
git commit -m "feat!: change public API"         # MAJOR bump
```

## Running Tests

```bash
# Single Python version
make test

# All supported versions
tox
```

Tests use real-world fixtures in `tests/data/` — no mocks for filesystem layout detection.

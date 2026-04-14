# Supported Layouts

`odoo-addons-path` uses a **Chain of Responsibility** pattern — detectors run in order, first match wins.

## Detection Order

| Priority | Layout | Marker | Detection Method |
|----------|--------|--------|-----------------|
| 1 | **Trobz** | `.trobz/` directory | Explicit directory marker |
| 2 | **Camptocamp (C2C)** | `Dockerfile` with C2C label | File content scan |
| 3 | **Odoo.sh** | 4-directory structure | Directory presence check |
| 4 | **Doodba** | `.copier-answers.yml` | YAML config key |
| 5 | **Generic** | Any `__manifest__.py` | Recursive filesystem search |

## Layout Details

### Trobz

Identified by the presence of a `.trobz/` directory at the project root.

```
project/
├── .trobz/
├── odoo/
└── addons/
    ├── repo1/
    └── repo2/
```

### Camptocamp (C2C)

Identified by a `Dockerfile` containing a Camptocamp-specific label.

```
project/
├── Dockerfile        # contains C2C label
├── odoo/
└── addons/
```

Both classic (`c2c`) and new (`c2c-new`) layout variants are supported.

### Odoo.sh

Identified by the standard 4-directory structure used on the Odoo.sh platform.

```
project/
├── odoo/
├── enterprise/
├── design-themes/
└── src/
```

### Doodba

Identified by a `.copier-answers.yml` file with Doodba-specific configuration keys.

```
project/
├── .copier-answers.yml
├── odoo/
│   └── custom/
│       └── src/
└── ...
```

### Generic (Fallback)

When no known layout is detected, falls back to a recursive search for any directory containing `__manifest__.py` files.

```
project/
└── any-structure/
    └── my_module/
        └── __manifest__.py   # ← found by recursive search
```

## Version Detection

Starting from v1.2.0, the tool also detects Odoo version from module manifests and reports inconsistencies when `--verbose` is used.

## Test Fixtures

Real-world layout fixtures are available in `tests/data/` for reference:
`trobz`, `c2c`, `c2c-new`, `doodba`, `odoo-sh`, `repo-version-module`

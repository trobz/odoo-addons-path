# Supported Layouts

`odoo-addons-path` uses a **Chain of Responsibility** detector. Each detector checks for its
own marker and, if it does not match, passes control to the next one in line.

```
TrobzDetector → C2CDetector → OdooShDetector → DoodbaDetector → GenericDetector
```

---

## Detection Order

| Priority | Detector | Marker |
|----------|----------|--------|
| 1 | Trobz | `.trobz/` directory |
| 2 | Camptocamp (C2C) | `Dockerfile` with Camptocamp label |
| 3 | Odoo.sh | All four dirs present: `enterprise/`, `odoo/`, `themes/`, `user/` |
| 4 | Doodba | `.copier-answers.yml` with `doodba` in `_src_path` |
| 5 | Generic (fallback) | Any `__manifest__.py` found recursively |

---

## Trobz

**Marker:** `.trobz/` directory exists at the project root.

**Typical structure:**

```
project-root/
├── .trobz/
│   └── config.yml
├── addons/
│   └── custom-repo/
│       └── addon1/
├── odoo/
│   ├── addons/
│   └── odoo/addons/
└── project/
    └── addon4/
```

**Paths collected:**

- `odoo/addons/`
- `odoo/odoo/addons/`
- All subdirectories under `addons/` (one per addon repo)
- `project/`

---

## Camptocamp (C2C)

**Marker:** A `Dockerfile` containing `LABEL maintainer='Camptocamp'` or `maintainer="Camptocamp"`.

Two sub-variants are supported based on directory structure:

### Legacy C2C

Identified by the presence of `odoo/src/`:

```
project-root/
└── odoo/
    ├── Dockerfile
    ├── src/
    │   ├── addons/
    │   └── odoo/addons/
    ├── external-src/
    │   └── custom-repo/
    └── local-src/
```

### Modern C2C (c2c-new)

```
project-root/
├── Dockerfile
└── odoo/
    ├── addons/
    ├── dev-src/
    ├── external-src/
    │   └── custom-repo/
    └── paid-modules/
```

---

## Odoo.sh

**Marker:** All four directories must exist at the project root: `enterprise/`, `odoo/`, `themes/`, `user/`.

```
project-root/
├── enterprise/
├── odoo/
│   ├── addons/
│   └── odoo/addons/
├── themes/
└── user/
    └── local-src/
        └── addon5/
```

**Paths collected:**

- `odoo/addons/`
- `odoo/odoo/addons/`
- `enterprise/`
- `themes/`
- All subdirectories under `user/` (recursively)

---

## Doodba

**Marker:** `.copier-answers.yml` at the project root, containing `_src_path: doodba-copier-template`.

```
project-root/
├── .copier-answers.yml
└── odoo/
    └── custom/
        └── src/
            ├── private/
            ├── custom-repo/
            └── odoo/
                ├── addons/
                └── odoo/addons/
```

**Paths collected** from `odoo/custom/src/`:

- `odoo/addons/` and `odoo/odoo/addons/` (from the `odoo/` sub-source)
- All other subdirectories (excluding `odoo` and `private`)

---

## Generic (Fallback)

When no specific layout is detected, the Generic detector performs a recursive
search for `__manifest__.py` files and infers addon repository roots.

**Algorithm:**

1. Glob `**/__manifest__.py` from the project root
2. Exclude paths inside `setup/` directories
3. Exclude manifests nested more than one level inside another manifest's directory
4. Return the parent-of-parent directories as addon repository roots

This fallback works for any Odoo project that follows the standard module structure,
even if it does not match any of the named layouts above.

---

## Adding a Custom Detector

See [Architecture](system-architecture.md) for the extension guide — subclass `CodeBaseDetector`
and insert it into the chain in `main.py::_detect_codebase_layout()`.

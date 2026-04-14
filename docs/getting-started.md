# Getting Started

`odoo-addons-path` automatically detects your Odoo project layout and outputs the correct
`addons_path` string — ready to paste into your Odoo config.

---

## Installation

### Recommended: uv tool (isolated, globally available)

```bash
uv tool install odoo-addons-path
```

### pip

```bash
pip install odoo-addons-path
```

### Development install

```bash
git clone https://github.com/trobz/odoo-addons-path
cd odoo-addons-path
uv sync
```

---

## Requirements

| Requirement | Version |
|------------|---------|
| Python | 3.10 – 3.13 |
| pyyaml | any |
| typer | ≥ 0.19.2 |

---

## First Run

Point the tool at your Odoo project root:

```bash
odoo-addons-path /path/to/your/odoo/project
```

The tool will:

1. Detect your layout (Trobz, C2C, Odoo.sh, Doodba, or Generic)
2. Walk the directory tree to find all addon repositories
3. Print a comma-separated list of absolute paths

**Example output:**

```
/home/dev/project/odoo/addons,/home/dev/project/addons/custom-repo,/home/dev/project/project
```

Paste that directly into your `odoo.conf`:

```ini
[options]
addons_path = /home/dev/project/odoo/addons,/home/dev/project/addons/custom-repo,/home/dev/project/project
```

---

## Verbose Mode

Use `--verbose` / `-v` to see which layout was detected and how paths were categorised:

```bash
odoo-addons-path /path/to/project --verbose
```

---

## Environment Variable

If you always work in the same project, set `CODEBASE` to skip typing the path:

```bash
export CODEBASE=/home/dev/project
odoo-addons-path          # uses $CODEBASE automatically
```

---

## Next Steps

- [CLI Reference](cli-reference.md) — all options and flags
- [Python API](python-api.md) — use from your own scripts
- [Supported Layouts](supported-layouts.md) — how each layout is detected

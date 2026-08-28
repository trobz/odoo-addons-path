# Supported Project Layouts

`odoo-addons-path` auto-detects addon directories across these layouts:

## c2c (Camptocamp)

```
project/
├── odoo/
│   └── external-src/
│       ├── addon1/
│       └── addon2/
└── src/
    └── custom/
```

## doodba (Docker-based)

```
project/
├── odoo/
│   └── auto/
│       └── addons/
├── private/
│   └── addon1/
└── custom/
    └── src/
```

## odoo.sh

```
project/
├── odoo/
│   └── addons/
└── enterprise/
    └── addons/
```

## trobz

```
project/
├── addons/
│   ├── module1/
│   └── module2/
└── external/
    └── oca/
```

## Version-Based Repos

For multi-version repos (OCA-style):

```
repos/
├── sale-workflow/
│   ├── 16.0/
│   │   └── sale_custom/
│   └── 18.0/
│       └── sale_custom/
└── purchase-workflow/
    └── 18.0/
```

Detect with pattern:
```bash
odoo-addons-path --addons-dir "./repos/*/18.0" .
```

## Custom Detection

Override auto-detection with `--addons-dir`:
```bash
# Multiple custom paths
odoo-addons-path --addons-dir "./src/,./lib/,./custom/" .

# Glob patterns
odoo-addons-path --addons-dir "./addons/**/18.0" .
```

---
icon: lucide/book
description: Complete reference for every odoo-addons-path command, auto-generated from --help.
tags:
  - reference
  - cli
---

!!! info "Auto-generated"
    This page is regenerated from `odoo-addons-path --help` by `make cli-docs`.
    Do not edit by hand — your changes will be overwritten on the next build.

# `odoo-addons-path`

Return addons_path constructor

**Usage**:

```console
$ odoo-addons-path [OPTIONS] [codebase]
```

**Arguments**:

* `codebase`: Path to the Odoo project whose layout should be detected. Layout detection only runs when this is given explicitly (or via the CODEBASE environment variable); without it, only the explicit --addons-dir/--odoo-dir options are used.  \[env var: CODEBASE\]

**Options**:

* `-V, --version`: Display the odoo-addons-path version.
* `--addons-dir <str>`: Paths that are addon directories (contain Odoo modules) or paths that contain addon directories (repositories with multiple Odoo modules). Globs and comma-separated values are supported.
* `--odoo-dir <str>`: Path containing the Odoo source code.
* `-v, --verbose`
* `--check-versions`: Check for version discrepancies across addons and warn if multiple Odoo versions are found.
* `--format <text|json>`: Output format: &#x27;text&#x27; (default, comma-joined addons_path) or &#x27;json&#x27; (structured layout info).  \[default: text\]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

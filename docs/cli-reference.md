# CLI Reference

## Synopsis

```
odoo-addons-path [OPTIONS] [CODEBASE]
```

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `CODEBASE` | `$CODEBASE` env var, then `./` | Root directory of your Odoo project |

## Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--addons-dir` | | `TEXT` (repeatable) | Explicit addon directory paths. Accepts glob patterns and comma-separated values. Skips auto-detection. |
| `--odoo-dir` | | `TEXT` | Explicit path to the Odoo source directory. Skips auto-detection. |
| `--verbose` | `-v` | flag | Print categorised path breakdown in addition to the final result. |
| `--check-versions` | | flag | After path resolution, scan manifests and warn about version inconsistencies. |
| `--help` | | flag | Show help and exit. |

---

## Examples

### Auto-detect layout

```bash
odoo-addons-path /home/dev/myproject
```

### Verbose — see detected layout and path categories

```bash
odoo-addons-path /home/dev/myproject --verbose
```

### Provide addon directories explicitly (skips detection)

```bash
# Single directory
odoo-addons-path /home/dev/myproject --addons-dir ./addons/custom

# Glob pattern — expand all version-keyed sub-directories
odoo-addons-path /home/dev/myproject --addons-dir "./addons/*/18.0"

# Comma-separated list
odoo-addons-path /home/dev/myproject --addons-dir "./addons/repo1, ./addons/repo2"

# Repeatable flag
odoo-addons-path /home/dev/myproject --addons-dir ./addons/repo1 --addons-dir ./addons/repo2
```

### Provide Odoo source explicitly (skips detection)

```bash
odoo-addons-path /home/dev/myproject --odoo-dir /opt/odoo
```

### Both explicit — fully manual, no detection

```bash
odoo-addons-path /home/dev/myproject \
  --odoo-dir /opt/odoo \
  --addons-dir "./addons/custom, ./addons/enterprise"
```

### Check for version inconsistencies

```bash
odoo-addons-path /home/dev/myproject --check-versions
```

Exits with a warning if addons declare different Odoo major versions (e.g., mixing `17.0` and `18.0` modules).

### Use environment variable

```bash
export CODEBASE=/home/dev/myproject
odoo-addons-path              # equivalent to: odoo-addons-path /home/dev/myproject
odoo-addons-path --verbose    # with verbosity
```

---

## Detector Skip Behaviour

Auto-detection is **skipped** whenever any explicit path is provided:

| `--addons-dir` | `--odoo-dir` | Detection runs? |
|:--------------:|:------------:|:---------------:|
| — | — | Yes |
| provided | — | No |
| — | provided | No |
| provided | provided | No |

When detection is skipped, only the explicitly provided paths are used. This gives you full control without interference from the detector.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success — paths printed to stdout |
| `1` | Failure — invalid path, or no layout detected and no fallback found |

---

## Output Format

The command prints a single line to stdout: a comma-separated list of **absolute, resolved** paths with no trailing newline.

```
/abs/path/one,/abs/path/two,/abs/path/three
```

This format is directly compatible with the `addons_path` key in `odoo.conf`.

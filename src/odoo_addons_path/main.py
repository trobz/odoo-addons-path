import ast
import re
from collections import Counter
from pathlib import Path

import typer

from odoo_addons_path.detector import C2CDetector, DoodbaDetector, GenericDetector, OdooShDetector, TrobzDetector


def _add_to_path(path_list: list[str], dirs_to_add: list[Path], is_sorted: bool = False):
    if is_sorted:
        dirs_to_add = sorted(dirs_to_add, key=lambda p: p.name)
    for d in dirs_to_add:
        if d.is_dir():
            resolved_path = str(d.resolve())
            if resolved_path not in path_list:
                path_list.append(resolved_path)


def detect_codebase_layout(codebase: Path, verbose: bool = False) -> dict:
    trobz = TrobzDetector()
    c2c = C2CDetector()
    odoo_sh = OdooShDetector()
    doodba = DoodbaDetector()
    fallback = GenericDetector()
    trobz.set_next(c2c).set_next(odoo_sh).set_next(doodba).set_next(fallback)
    res = trobz.detect(codebase)
    if not res:
        typer.secho("No codebase layout detected", fg=typer.colors.RED)
        raise typer.Exit(1)
    detector_name, detected_paths = res
    if verbose:
        typer.echo(f"Codebase layout: {detector_name}")
    return detected_paths


def get_odoo_version_from_release(odoo_dir: Path) -> str | None:
    """Read the Odoo version (e.g. '18.0') from ``odoo/release.py``."""
    release_py = odoo_dir / "odoo" / "release.py"
    if not release_py.is_file():
        return None
    content = release_py.read_text()
    match = re.search(r"version_info\s*=\s*\((\d+),\s*(\d+)", content)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return None


def _extract_version_from_manifest(manifest_path: Path) -> str | None:
    """Extract the major version (e.g. '18.0') from a ``__manifest__.py`` file."""
    try:
        content = manifest_path.read_text()
        data = ast.literal_eval(content)
    except (OSError, ValueError, SyntaxError):
        return None
    version = data.get("version") if isinstance(data, dict) else None
    if not version or not isinstance(version, str):
        return None
    # Only accept full Odoo format: major.minor.patch.patch.patch (e.g. "18.0.1.0.0")
    match = re.match(r"(\d+\.\d+)\.\d+\.\d+\.\d+$", version)
    return match.group(1) if match else None


def get_odoo_version_from_addons(addons_path: str) -> str | None:
    """Infer Odoo version from the manifests found in an addons path string.

    Returns the most common major version (e.g. ``'18.0'``), or ``None`` if
    no version could be determined.
    """
    versions: list[str] = []
    for path_str in addons_path.split(","):
        path = Path(path_str)
        if not path.is_dir():
            continue
        for manifest in path.glob("*/__manifest__.py"):
            v = _extract_version_from_manifest(manifest)
            if v:
                versions.append(v)
    if not versions:
        return None
    counter = Counter(versions)
    return counter.most_common(1)[0][0]


def check_version_consistency(addons_path: str) -> dict[str, list[str]]:
    """Check for version discrepancies across all addons in the path.

    Returns a dict mapping each detected major version to the list of addon
    names using that version.  An empty dict means no versions were found.
    """
    version_addons: dict[str, list[str]] = {}
    for path_str in addons_path.split(","):
        path = Path(path_str)
        if not path.is_dir():
            continue
        for manifest in path.glob("*/__manifest__.py"):
            v = _extract_version_from_manifest(manifest)
            if v:
                version_addons.setdefault(v, []).append(manifest.parent.name)
    return version_addons


def get_odoo_version(
    addons_path: str,
    odoo_dir: Path | None = None,
    detected_paths: dict | None = None,
) -> str | None:
    """Return the Odoo major version (e.g. ``'18.0'``).

    Tries ``odoo/release.py`` first (from *odoo_dir* or the detected layout),
    then falls back to inferring the version from addon manifests.
    """
    # Try release.py from explicit odoo_dir
    if odoo_dir:
        version = get_odoo_version_from_release(odoo_dir)
        if version:
            return version

    # Try release.py from detected odoo_dir paths
    if detected_paths and detected_paths.get("odoo_dir"):
        for odoo_path in detected_paths["odoo_dir"]:
            # odoo_dir entries point to e.g. <root>/odoo/addons — walk up to find release.py
            candidate = odoo_path
            while candidate != candidate.parent:
                version = get_odoo_version_from_release(candidate)
                if version:
                    return version
                candidate = candidate.parent

    # Fallback: infer from addon manifests
    return get_odoo_version_from_addons(addons_path)


def _process_paths(
    all_paths: dict[str, list[str]],
    detected_paths: dict,
    addons_dir: list[Path] | None,
    odoo_dir: Path | None,
):
    if odoo_dir:
        _add_to_path(
            all_paths["odoo_dir"],
            [odoo_dir / "addons", odoo_dir / "odoo" / "addons"],
        )
    if detected_paths.get("odoo_dir"):
        _add_to_path(all_paths["odoo_dir"], detected_paths["odoo_dir"])

    all_addon_paths_to_process = (
        (addons_dir or []) + detected_paths.get("addons_dirs", []) + detected_paths.get("addons_dir", [])
    )

    result = []

    for p in all_addon_paths_to_process:
        if not p.is_dir():
            continue
        manifests = p.glob("**/__manifest__.py")
        for manifest in sorted(manifests):
            repo_path = manifest.parent.parent
            if repo_path not in result:
                result.append(repo_path)

    _add_to_path(
        all_paths["addon_repositories"],
        result,
        is_sorted=not bool(addons_dir),
    )


def get_addons_path(
    codebase: Path,
    addons_dir: list[Path] | None = None,
    odoo_dir: Path | None = None,
    verbose: bool = False,
    detected_paths: dict | None = None,
) -> str:
    all_paths: dict[str, list[str]] = {
        "odoo_dir": [],
        "addon_repositories": [],
    }

    # Skip detector only if both paths are None (no explicit paths provided)
    if detected_paths is None and not addons_dir and not odoo_dir:
        detected_paths = detect_codebase_layout(codebase, verbose)

    _process_paths(all_paths, detected_paths or {}, addons_dir, odoo_dir)

    result = [path for paths in all_paths.values() for path in paths]
    addons_path = ",".join(result)

    if verbose:
        version = get_odoo_version(addons_path, odoo_dir=odoo_dir, detected_paths=detected_paths)
        if version:
            typer.echo(f"Odoo version: {version}")
        for category, paths in all_paths.items():
            if paths:
                typer.echo(f"\n# {category}")
                for path in paths:
                    typer.echo(path)
        typer.echo("\n# addons_path")
        typer.echo(addons_path)

    return addons_path

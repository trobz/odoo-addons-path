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


def get_addons_path(
    codebase: Path,
    addons_dirs: list[Path] | None = None,
    addons_dir: list[Path] | None = None,
    odoo_dir: Path | None = None,
    verbose: bool = False,
) -> str:
    all_paths: dict[str, list[str]] = {
        "odoo_dir": [],
        "addon_repositories": [],
        "addon_directories": [],
        "themes": [],
    }

    detected_paths = {}
    if not addons_dirs and not addons_dir:
        trobz = TrobzDetector()
        c2c = C2CDetector()
        odoo_sh = OdooShDetector()
        doodba = DoodbaDetector()
        fallback = GenericDetector()

        trobz.set_next(c2c).set_next(odoo_sh).set_next(doodba).set_next(fallback)

        res = trobz.detect(codebase)
        if res:
            detector_name, detected_paths = res
            if verbose:
                typer.echo(f"Codebase layout: {detector_name}")
        else:
            detected_paths = {}

    if odoo_dir:
        _add_to_path(
            all_paths["odoo_dir"],
            [
                odoo_dir / "addons",
                odoo_dir / "odoo" / "addons",
            ],
        )
    else:
        _add_to_path(
            all_paths["odoo_dir"],
            detected_paths.get("odoo_dir", []),
        )

    _add_to_path(
        all_paths["addon_repositories"],
        addons_dirs or detected_paths.get("addons_dirs", []),
        is_sorted=True,
    )
    _add_to_path(
        all_paths["addon_directories"],
        addons_dir or detected_paths.get("addons_dir", []),
        is_sorted=True,
    )

    result = []
    for paths in all_paths.values():
        result.extend(paths)
    addons_path = ",".join(result)

    if verbose:
        for category, paths in all_paths.items():
            if paths:
                typer.echo(f"\n# {category}")
                for path in paths:
                    typer.echo(path)
        typer.echo("\n# addons_path")
        typer.echo(addons_path)

    return addons_path

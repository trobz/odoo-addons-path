from pathlib import Path
from typing import Optional

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
    addons_dirs: Optional[list[Path]] = None,
    addons_dir: Optional[list[Path]] = None,
    odoo_dir: Optional[Path] = None,
    cli: bool = False,
) -> list[str]:
    all_paths: dict[str, list[str]] = {
        "odoo_dir": [],
        "external_src": [],
        "local_src": [],
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
            if cli:
                typer.echo(f"Codebase layout: {detector_name}")
        else:
            detected_paths = {}

    _add_to_path(all_paths["odoo_dir"], [odoo_dir] if odoo_dir else detected_paths.get("odoo_dir", []))
    _add_to_path(
        all_paths["external_src"],
        addons_dirs or detected_paths.get("addons_dirs", []),
        is_sorted=True,
    )
    _add_to_path(
        all_paths["local_src"],
        addons_dir or detected_paths.get("addons_dir", []),
        is_sorted=True,
    )

    if cli:
        for category, paths in all_paths.items():
            if paths:
                typer.echo(f"\n# {category}")
                for path in paths:
                    typer.echo(path)

    result = []
    for paths in all_paths.values():
        result.extend(paths)
    return result

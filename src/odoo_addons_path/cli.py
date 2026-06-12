import glob
import json
from enum import Enum
from importlib.metadata import version
from pathlib import Path
from typing import Annotated

import typer

from .detector import C2CDetector, DoodbaDetector, GenericDetector, OdooShDetector, TrobzDetector
from .main import check_version_consistency, detect_codebase_layout, get_addons_path, get_odoo_version

_MULTI_VERSION_WARNING = "WARNING: Multiple Odoo versions detected in addons path!"


class OutputFormat(str, Enum):
    text = "text"
    json = "json"


def _parse_paths(values: list[str] | None) -> list[Path]:
    if not values:
        return []
    paths: list[Path] = []
    for value in values:
        for p_str in value.split(","):
            p_str = p_str.strip()
            if not p_str:
                continue
            p = Path(p_str).expanduser()
            if "*" in str(p) or "?" in str(p) or "[" in str(p):
                paths.extend(Path(g) for g in sorted(glob.glob(str(p), recursive=True)))
            else:
                paths.append(p)
    return paths


def _detect_layout_named(codebase: Path) -> tuple[str | None, dict | None]:
    trobz = TrobzDetector()
    c2c = C2CDetector()
    odoo_sh = OdooShDetector()
    doodba = DoodbaDetector()
    fallback = GenericDetector()
    trobz.set_next(c2c).set_next(odoo_sh).set_next(doodba).set_next(fallback)
    res = trobz.detect(codebase)
    if not res:
        return None, None
    return res


def _warn_version_discrepancies(addons_path: str) -> None:
    version_addons = check_version_consistency(addons_path)
    if len(version_addons) > 1:
        typer.secho(_MULTI_VERSION_WARNING, fg=typer.colors.YELLOW, err=True)
        for v, addons in sorted(version_addons.items()):
            typer.secho(f"  {v}: {', '.join(sorted(addons))}", fg=typer.colors.YELLOW, err=True)


def _emit_json(
    codebase: Path,
    addons_dir: list[Path],
    odoo_dir_path: Path | None,
    check_versions: bool,
) -> None:
    layout_name, detected_paths = _detect_layout_named(codebase)

    # Always call get_addons_path so explicit --addons-dir/--odoo-dir are included
    # even when no layout is detected; passing {} skips internal detection without
    # discarding the caller-supplied dirs.
    effective_detected = detected_paths if detected_paths is not None else {}
    addons_path = get_addons_path(
        codebase=codebase,
        addons_dir=addons_dir,
        odoo_dir=odoo_dir_path,
        verbose=False,
        detected_paths=effective_detected,
    )
    odoo_dir_list = [str(p) for p in effective_detected.get("odoo_dir", [])]

    version = get_odoo_version(addons_path, odoo_dir=odoo_dir_path, detected_paths=detected_paths)

    if check_versions:
        _warn_version_discrepancies(addons_path)

    typer.echo(
        json.dumps({
            "layout": layout_name,
            "odoo_dir": odoo_dir_list,
            "version": version,
            "addons_path": addons_path,
        })
    )


app = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(f"odoo-addons-path {version('odoo-addons-path')}")
        raise typer.Exit()


@app.command()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            is_eager=True,
            help="Display the odoo-addons-path version.",
        ),
    ] = False,
    codebase: Annotated[
        Path,
        typer.Argument(
            envvar="CODEBASE",
            help="Path to the Odoo project. Can also be set via the CODEBASE environment variable.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = Path("./"),
    addons_dir: Annotated[
        list[str] | None,
        typer.Option(
            help=(
                "Paths that are addon directories (contain Odoo modules) or "
                "paths that contain addon directories (repositories with multiple Odoo modules). "
                "Globs and comma-separated values are supported."
            ),
        ),
    ] = None,
    odoo_dir: Annotated[
        str | None,
        typer.Option(
            help="Path containing the Odoo source code.",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
        ),
    ] = False,
    check_versions: Annotated[
        bool,
        typer.Option(
            "--check-versions",
            help="Check for version discrepancies across addons and warn if multiple Odoo versions are found.",
        ),
    ] = False,
    output_format: Annotated[
        OutputFormat,
        typer.Option(
            "--format",
            help="Output format: 'text' (default, comma-joined addons_path) or 'json' (structured layout info).",
        ),
    ] = OutputFormat.text,
):
    """
    Return addons_path constructor
    """
    odoo_dir_path = None
    if odoo_dir:
        odoo_dir_path = Path(odoo_dir).expanduser()
        if not odoo_dir_path.exists():
            typer.secho(f"Odoo dir {odoo_dir} not found.", fg=typer.colors.RED)
            raise typer.Exit(1)

    paths = _parse_paths(addons_dir)

    if output_format == OutputFormat.json:
        _emit_json(codebase, paths, odoo_dir_path, check_versions)
        raise typer.Exit(0)

    # --format text (default): unchanged behavior
    detected_paths = detect_codebase_layout(codebase, verbose)

    addons_path = get_addons_path(
        codebase=codebase,
        addons_dir=paths,
        odoo_dir=odoo_dir_path,
        verbose=verbose,
        detected_paths=detected_paths,
    )

    if check_versions:
        _warn_version_discrepancies(addons_path)

    if not verbose:
        typer.echo(addons_path)

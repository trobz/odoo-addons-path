from pathlib import Path
from typing import Annotated

import typer

from .main import get_addons_path


def _parse_paths(value: str) -> list[Path]:
    if not value:
        return []
    paths = [Path(p.strip()) for p in value.split(",") if p.strip()]
    return paths


app = typer.Typer()


@app.command()
def main(
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
    addons_dirs: Annotated[
        str | None,
        typer.Option(
            help="Comma-separated directories that contain addon directories (repositories with multiple Odoo modules).",
        ),
    ] = None,
    addons_dir: Annotated[
        str | None,
        typer.Option(
            help="Comma-separated directories that are addon directories (contain Odoo modules).",
        ),
    ] = None,
    odoo_dir: Annotated[
        Path | None,
        typer.Option(
            help="The directory containing the Odoo source code.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
        ),
    ] = False,
):
    """
    Return addons_path constructor
    """
    parsed_addons_dirs = _parse_paths(addons_dirs) if addons_dirs else None
    parsed_addons_dir = _parse_paths(addons_dir) if addons_dir else None

    addons_path = get_addons_path(
        codebase=codebase,
        addons_dirs=parsed_addons_dirs,
        addons_dir=parsed_addons_dir,
        odoo_dir=odoo_dir,
        verbose=verbose,
    )

    if not verbose:
        typer.echo(addons_path)

from pathlib import Path
from typing import Annotated, Optional

import typer

from .main import get_addons_path

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
        Optional[list[Path]],
        typer.Option(
            help="A directory that contains addon directories.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = None,
    addons_dir: Annotated[
        Optional[list[Path]],
        typer.Option(
            help="A directory that is an addon directory.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = None,
    odoo_dir: Annotated[
        Optional[Path],
        typer.Option(
            help="The directory containing the Odoo source code.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = None,
):
    """
    Return addons_path constructor
    """
    get_addons_path(codebase=codebase, addons_dirs=addons_dirs, addons_dir=addons_dir, odoo_dir=odoo_dir, cli=True)

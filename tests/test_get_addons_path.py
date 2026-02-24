import shutil
from pathlib import Path

import pytest

from odoo_addons_path.main import detect_codebase_layout, get_addons_path, get_odoo_version_from_release


@pytest.fixture
def base_dir(tmp_path: Path) -> Path:
    d = tmp_path / "project"
    d.mkdir()
    return d


@pytest.mark.parametrize(
    "layout, expected_paths",
    [
        (
            "trobz",
            [
                "odoo/addons",
                "odoo/odoo/addons",
                "addons/custom-repo",
                "project",
            ],
        ),
        (
            "c2c",
            [
                "odoo/src/addons",
                "odoo/src/odoo/addons",
                "odoo/external-src/custom-repo",
                "odoo/local-src",
            ],
        ),
        (
            "c2c-new",
            [
                "odoo/addons",
                "odoo/external-src/custom-repo",
                "odoo/dev-src",
                "odoo/paid-modules",
            ],
        ),
        (
            "doodba",
            [
                "odoo/custom/src/odoo/addons",
                "odoo/custom/src/odoo/odoo/addons",
                "odoo/custom/src/custom-repo",
                "odoo/custom/src/private",
            ],
        ),
        (
            "odoo-sh",
            [
                "odoo/addons",
                "odoo/odoo/addons",
                "enterprise",
                "user/local-src",
                "themes",
            ],
        ),
    ],
)
def test_layouts(base_dir: Path, layout: str, expected_paths: list[str]):
    shutil.copytree(Path(__file__).parent / "data" / layout, base_dir, dirs_exist_ok=True)
    expected_paths = [str((base_dir / path).resolve()) for path in expected_paths]
    expected_addons_path = ",".join(expected_paths)

    result = get_addons_path(base_dir)

    assert result == expected_addons_path


@pytest.mark.parametrize("layout", ["trobz", "c2c", "doodba", "odoo-sh"])
def test_detect_codebase_layout(base_dir: Path, layout: str):
    shutil.copytree(Path(__file__).parent / "data" / layout, base_dir, dirs_exist_ok=True)

    result = detect_codebase_layout(base_dir)

    assert isinstance(result, dict)
    assert "odoo_dir" in result or "addons_dirs" in result or "addons_dir" in result


def test_get_odoo_version_from_release(tmp_path: Path):
    release_dir = tmp_path / "odoo"
    release_dir.mkdir()
    release_py = release_dir / "release.py"
    release_py.write_text("version_info = (18, 0, 0, 'final', 0)\nversion = '18.0'\n")

    result = get_odoo_version_from_release(tmp_path)

    assert result == "18.0"


def test_get_odoo_version_from_release_missing(tmp_path: Path):
    result = get_odoo_version_from_release(tmp_path)

    assert result is None


def test_get_odoo_version_from_release_no_version_info(tmp_path: Path):
    release_dir = tmp_path / "odoo"
    release_dir.mkdir()
    (release_dir / "release.py").write_text("# no version_info here\n")

    result = get_odoo_version_from_release(tmp_path)

    assert result is None


def test_get_addons_path_with_detected_paths(base_dir: Path):
    shutil.copytree(Path(__file__).parent / "data" / "trobz", base_dir, dirs_exist_ok=True)

    detected = detect_codebase_layout(base_dir)
    result_auto = get_addons_path(base_dir)
    result_predetected = get_addons_path(base_dir, detected_paths=detected)

    assert result_auto == result_predetected

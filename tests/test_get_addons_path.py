import shutil
from pathlib import Path

import pytest

from odoo_addons_path.main import (
    _extract_version_from_manifest,
    check_version_consistency,
    detect_codebase_layout,
    get_addons_path,
    get_odoo_version,
    get_odoo_version_from_addons,
    get_odoo_version_from_release,
)


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


class TestExtractVersionFromManifest:
    def test_standard_version(self, tmp_path: Path):
        manifest = tmp_path / "__manifest__.py"
        manifest.write_text('{"name": "Test", "version": "18.0.1.0.0"}')
        assert _extract_version_from_manifest(manifest) == "18.0"

    def test_short_version_ignored(self, tmp_path: Path):
        manifest = tmp_path / "__manifest__.py"
        manifest.write_text('{"name": "Test", "version": "17.0.1.0"}')
        assert _extract_version_from_manifest(manifest) is None

    def test_non_odoo_version_ignored(self, tmp_path: Path):
        manifest = tmp_path / "__manifest__.py"
        manifest.write_text('{"name": "Test", "version": "1.0"}')
        assert _extract_version_from_manifest(manifest) is None

    def test_no_version_key(self, tmp_path: Path):
        manifest = tmp_path / "__manifest__.py"
        manifest.write_text('{"name": "Test"}')
        assert _extract_version_from_manifest(manifest) is None

    def test_empty_file(self, tmp_path: Path):
        manifest = tmp_path / "__manifest__.py"
        manifest.write_text("")
        assert _extract_version_from_manifest(manifest) is None

    def test_invalid_syntax(self, tmp_path: Path):
        manifest = tmp_path / "__manifest__.py"
        manifest.write_text("{invalid")
        assert _extract_version_from_manifest(manifest) is None

    def test_missing_file(self, tmp_path: Path):
        manifest = tmp_path / "__manifest__.py"
        assert _extract_version_from_manifest(manifest) is None


class TestGetOdooVersionFromAddons:
    def test_single_version(self, tmp_path: Path):
        addon = tmp_path / "my_addon"
        addon.mkdir()
        (addon / "__manifest__.py").write_text('{"name": "A", "version": "18.0.1.0.0"}')
        assert get_odoo_version_from_addons(str(tmp_path)) == "18.0"

    def test_majority_version(self, tmp_path: Path):
        for i, ver in enumerate(["18.0.1.0.0", "18.0.2.0.0", "17.0.1.0.0"]):
            addon = tmp_path / f"addon{i}"
            addon.mkdir()
            (addon / "__manifest__.py").write_text(f'{{"name": "A{i}", "version": "{ver}"}}')
        assert get_odoo_version_from_addons(str(tmp_path)) == "18.0"

    def test_no_manifests(self, tmp_path: Path):
        assert get_odoo_version_from_addons(str(tmp_path)) is None

    def test_no_versions_in_manifests(self, tmp_path: Path):
        addon = tmp_path / "my_addon"
        addon.mkdir()
        (addon / "__manifest__.py").write_text('{"name": "A"}')
        assert get_odoo_version_from_addons(str(tmp_path)) is None


class TestCheckVersionConsistency:
    def test_consistent_versions(self, tmp_path: Path):
        for name in ["addon1", "addon2"]:
            addon = tmp_path / name
            addon.mkdir()
            (addon / "__manifest__.py").write_text(f'{{"name": "{name}", "version": "18.0.1.0.0"}}')
        result = check_version_consistency(str(tmp_path))
        assert sorted(result["18.0"]) == ["addon1", "addon2"]
        assert len(result) == 1

    def test_mixed_versions(self, tmp_path: Path):
        for name, ver in [("addon_a", "18.0.1.0.0"), ("addon_b", "17.0.1.0.0")]:
            addon = tmp_path / name
            addon.mkdir()
            (addon / "__manifest__.py").write_text(f'{{"name": "{name}", "version": "{ver}"}}')
        result = check_version_consistency(str(tmp_path))
        assert len(result) == 2
        assert "addon_a" in result["18.0"]
        assert "addon_b" in result["17.0"]

    def test_multiple_paths(self, tmp_path: Path):
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()
        addon1 = dir1 / "addon1"
        addon1.mkdir()
        (addon1 / "__manifest__.py").write_text('{"name": "A1", "version": "18.0.1.0.0"}')
        addon2 = dir2 / "addon2"
        addon2.mkdir()
        (addon2 / "__manifest__.py").write_text('{"name": "A2", "version": "17.0.1.0.0"}')
        result = check_version_consistency(f"{dir1},{dir2}")
        assert len(result) == 2

    def test_empty_path(self, tmp_path: Path):
        assert check_version_consistency(str(tmp_path)) == {}


class TestGetOdooVersion:
    def test_prefers_release_over_manifests(self, tmp_path: Path):
        # Set up release.py saying 18.0
        release_dir = tmp_path / "odoo"
        release_dir.mkdir()
        (release_dir / "release.py").write_text("version_info = (18, 0, 0, 'final', 0)")
        # Set up addon saying 17.0
        addon = tmp_path / "addon1"
        addon.mkdir()
        (addon / "__manifest__.py").write_text('{"name": "A", "version": "17.0.1.0.0"}')

        result = get_odoo_version(str(tmp_path), odoo_dir=tmp_path)
        assert result == "18.0"

    def test_falls_back_to_manifests(self, tmp_path: Path):
        addon = tmp_path / "addon1"
        addon.mkdir()
        (addon / "__manifest__.py").write_text('{"name": "A", "version": "16.0.1.0.0"}')

        result = get_odoo_version(str(tmp_path))
        assert result == "16.0"

    def test_no_version_found(self, tmp_path: Path):
        result = get_odoo_version(str(tmp_path))
        assert result is None

    def test_from_detected_paths(self, tmp_path: Path):
        # Simulate detected odoo_dir pointing to <root>/odoo/addons
        odoo_root = tmp_path / "odoo"
        odoo_root.mkdir()
        odoo_pkg = odoo_root / "odoo"
        odoo_pkg.mkdir()
        (odoo_pkg / "release.py").write_text("version_info = (17, 0, 0, 'final', 0)")
        addons_dir = odoo_root / "addons"
        addons_dir.mkdir()

        detected_paths = {"odoo_dir": [addons_dir]}
        result = get_odoo_version("", detected_paths=detected_paths)
        assert result == "17.0"

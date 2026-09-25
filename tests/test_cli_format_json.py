"""Tests for odoo-addons-path --format json CLI option."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from odoo_addons_path.cli import app

runner = CliRunner()


def test_no_codebase_argument_skips_detection(tmp_path):
    """Running with only explicit dirs from the tool's own repo must not
    sweep tests/data fixtures: without a codebase argument, no layout
    detection runs at all."""
    (tmp_path / "odoo" / "addons").mkdir(parents=True)
    (tmp_path / "addons").mkdir()
    result = runner.invoke(
        app,
        ["--odoo-dir", str(tmp_path / "odoo"), "--addons-dir", str(tmp_path / "addons")],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "tests/data" not in result.output
    assert str(tmp_path / "odoo" / "addons") in result.output


@pytest.mark.parametrize("args", [[], ["--format", "json"]])
def test_no_input_at_all_errors(args, monkeypatch):
    """Without a codebase, CODEBASE env var, --addons-dir or --odoo-dir,
    the CLI must fail loudly instead of printing an empty addons path."""
    monkeypatch.delenv("CODEBASE", raising=False)
    result = runner.invoke(app, args)

    assert result.exit_code == 1
    assert "CODEBASE" in result.output


DATA = Path(__file__).parent / "data"


def test_format_json_trobz_layout():
    result = runner.invoke(app, [str(DATA / "trobz"), "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["layout"] == "Trobz"
    assert isinstance(data["odoo_dir"], list)
    assert len(data["odoo_dir"]) > 0
    assert isinstance(data["addons_path"], str)
    assert data["addons_path"] != ""
    # version may be None (empty manifests) but key must exist
    assert "version" in data
    assert data["odoo_edition"] == "CE"


def test_format_json_addons_path_equals_text_output():
    result_json = runner.invoke(app, [str(DATA / "trobz"), "--format", "json"])
    result_text = runner.invoke(app, [str(DATA / "trobz"), "--format", "text"])
    assert result_json.exit_code == 0
    assert result_text.exit_code == 0
    data = json.loads(result_json.stdout)
    assert data["addons_path"] == result_text.stdout.strip()


def test_format_json_fallback_layout(tmp_path):
    # A directory with manifests but no recognized layout marker → fallback
    module_dir = tmp_path / "my_module"
    module_dir.mkdir()
    (module_dir / "__manifest__.py").write_text("{'name': 'my_module'}")

    result = runner.invoke(app, [str(tmp_path), "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["layout"] == "fallback"
    assert data["odoo_dir"] == []


def test_format_json_no_layout_exits_zero(tmp_path):
    # A directory with no manifests → no layout detected
    result_json = runner.invoke(app, [str(tmp_path), "--format", "json"])
    assert result_json.exit_code == 0
    data = json.loads(result_json.stdout)
    assert data["layout"] is None
    assert data["odoo_dir"] == []
    assert data["addons_path"] == ""


def test_format_text_no_layout_exits_one(tmp_path):
    # --format text keeps the hard exit-1 behavior
    result_text = runner.invoke(app, [str(tmp_path), "--format", "text"])
    assert result_text.exit_code == 1


def test_format_default_no_format_flag_exits_one(tmp_path):
    # default (no --format) keeps the hard exit-1 behavior
    result = runner.invoke(app, [str(tmp_path)])
    assert result.exit_code == 1


def test_format_json_version_null_when_unresolvable(tmp_path):
    # Manifests with no version → version is null
    module_dir = tmp_path / "my_module"
    module_dir.mkdir()
    (module_dir / "__manifest__.py").write_text("{'name': 'my_module'}")

    result = runner.invoke(app, [str(tmp_path), "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["version"] is None


def test_format_json_check_versions_warnings_on_stderr(tmp_path):
    # --check-versions warnings must not bleed into JSON stdout
    # Create two modules with different versions
    for mod, ver in [("mod_a", "17.0.1.0.0"), ("mod_b", "18.0.1.0.0")]:
        d = tmp_path / mod
        d.mkdir()
        (d / "__manifest__.py").write_text(f"{{'name': '{mod}', 'version': '{ver}'}}")

    venv_bin = Path(sys.executable).parent / "odoo-addons-path"
    proc = subprocess.run(  # noqa: S603
        [str(venv_bin), str(tmp_path), "--format", "json", "--check-versions"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    # stdout must be valid JSON
    data = json.loads(proc.stdout)
    assert "layout" in data
    # warnings land on stderr, not stdout
    assert "WARNING" in proc.stderr


def test_format_text_default_byte_identical(tmp_path):
    # --format text output must be identical to no-flag output (when layout exists)
    module_dir = tmp_path / "my_module"
    module_dir.mkdir()
    (module_dir / "__manifest__.py").write_text("{'name': 'my_module'}")

    result_text = runner.invoke(app, [str(tmp_path), "--format", "text"])
    result_default = runner.invoke(app, [str(tmp_path)])
    assert result_text.exit_code == result_default.exit_code
    assert result_text.stdout == result_default.stdout


def test_format_json_addons_dir_on_undetected_layout(tmp_path):
    # Explicit --addons-dir must be reflected in addons_path even when no layout is detected
    empty_codebase = tmp_path / "empty"
    empty_codebase.mkdir()

    addons = tmp_path / "my_addons"
    addons.mkdir()
    module = addons / "my_module"
    module.mkdir()
    (module / "__manifest__.py").write_text("{'name': 'my_module', 'version': '17.0.1.0.0'}")

    result = runner.invoke(
        app,
        [str(empty_codebase), "--format", "json", "--addons-dir", str(addons)],
    )
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["layout"] is None
    # addons_path must not be empty — the explicit addons_dir must be included
    assert data["addons_path"] != ""


def test_format_json_odoo_dir_on_undetected_layout(tmp_path):
    # Explicit --odoo-dir must contribute to addons_path even when no layout is detected
    empty_codebase = tmp_path / "empty"
    empty_codebase.mkdir()

    # Simulate an Odoo source tree with an addons directory
    odoo_root = tmp_path / "odoo_src"
    odoo_addons = odoo_root / "addons"
    odoo_addons.mkdir(parents=True)
    module = odoo_addons / "base"
    module.mkdir()
    (module / "__manifest__.py").write_text("{'name': 'base', 'version': '17.0.1.0.0'}")

    result = runner.invoke(
        app,
        [str(empty_codebase), "--format", "json", "--odoo-dir", str(odoo_root)],
    )
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["layout"] is None
    # addons_path must contain the odoo addons path
    assert str(odoo_addons.resolve()) in data["addons_path"]


@pytest.mark.parametrize("fmt", ["text", "json"])
def test_verbose_notes_skipped_detection_without_codebase(tmp_path, monkeypatch, fmt):
    # --verbose explains on stderr why no layout was detected; stdout stays clean
    monkeypatch.delenv("CODEBASE", raising=False)
    (tmp_path / "odoo" / "addons").mkdir(parents=True)

    result = runner.invoke(app, ["-v", "--format", fmt, "--odoo-dir", str(tmp_path / "odoo")])
    assert result.exit_code == 0
    assert "layout detection skipped" in result.stderr
    assert "layout detection skipped" not in result.stdout
    if fmt == "json":
        assert json.loads(result.stdout)["layout"] is None


def test_verbose_no_note_with_codebase():
    result = runner.invoke(app, ["-v", str(DATA / "trobz")])
    assert result.exit_code == 0
    assert "layout detection skipped" not in result.stderr


def test_format_json_explicit_odoo_dir_without_codebase(tmp_path, monkeypatch):
    # Explicit --odoo-dir must be reported in "odoo_dir", not only in addons_path
    monkeypatch.delenv("CODEBASE", raising=False)
    odoo_addons = tmp_path / "odoo_src" / "addons"
    odoo_addons.mkdir(parents=True)

    result = runner.invoke(app, ["--format", "json", "--odoo-dir", str(tmp_path / "odoo_src")])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["layout"] is None
    assert data["odoo_dir"] == [str(odoo_addons.resolve())]
    assert str(odoo_addons.resolve()) in data["addons_path"]


def test_format_json_explicit_odoo_dir_with_detected_layout(tmp_path):
    # Explicit --odoo-dir comes first, followed by the detected layout's odoo dirs
    odoo_addons = tmp_path / "odoo_src" / "addons"
    odoo_addons.mkdir(parents=True)

    result = runner.invoke(
        app,
        [str(DATA / "trobz"), "--format", "json", "--odoo-dir", str(tmp_path / "odoo_src")],
    )
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["layout"] == "Trobz"
    assert data["odoo_dir"][0] == str(odoo_addons.resolve())
    assert len(data["odoo_dir"]) > 1
    for d in data["odoo_dir"]:
        assert d in data["addons_path"].split(",")

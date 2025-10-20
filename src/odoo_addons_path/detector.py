import glob
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import yaml


class CodeBaseDetector(ABC):
    _next_detector: Optional["CodeBaseDetector"] = None

    def set_next(self, detector: "CodeBaseDetector") -> "CodeBaseDetector":
        self._next_detector = detector
        return detector

    @abstractmethod
    def detect(self, codebase: Path) -> Optional[tuple[str, dict[str, Any]]]:
        if self._next_detector:
            return self._next_detector.detect(codebase)
        return None


class TrobzDetector(CodeBaseDetector):
    def detect(self, codebase: Path) -> Optional[tuple[str, dict[str, Any]]]:
        if (codebase / ".trobz").is_dir():
            addons_dirs = []
            for item in (codebase / "addons").iterdir():
                if item.is_dir():
                    addons_dirs.append(item)
            return (
                "Trobz",
                {
                    "addons_dirs": addons_dirs,
                    "addons_dir": [codebase / "project"],
                    "odoo_dir": [
                        codebase / "odoo/addons",
                        codebase / "odoo/odoo/addons",
                    ],
                },
            )
        return super().detect(codebase)


class DoodbaDetector(CodeBaseDetector):
    """
    root/
    ├── odoo/         # Odoo Enterprise
    │   └── custom/
        │   └── src/
        │       └── odoo/
        │       └── private/
        │       └── submodule/

    """

    def detect(self, codebase: Path) -> Optional[tuple[str, dict[str, Any]]]:
        copier_answers_file = codebase / ".copier-answers.yml"
        if not copier_answers_file.is_file():
            return super().detect(codebase)
        with open(copier_answers_file) as f:
            try:
                answers = yaml.safe_load(f)
                if "doodba" in answers.get("_src_path", ""):
                    addons_dirs = []
                    path = codebase / "odoo" / "custom" / "src"
                    if path.is_dir():
                        for item in path.iterdir():
                            if item.is_dir() and item.name not in ("odoo", "private"):
                                addons_dirs.append(item)
                        return (
                            "Doodba",
                            {
                                "addons_dirs": addons_dirs,
                                "addons_dir": [codebase / "odoo/custom/src/private"],
                                "odoo_dir": [
                                    codebase / "odoo/custom/src/odoo/addons",
                                    codebase / "odoo/custom/src/odoo/odoo/addons",
                                ],
                            },
                        )
            except yaml.YAMLError:
                pass
        return super().detect(codebase)


class C2CDetector(CodeBaseDetector):
    def detect(self, codebase: Path) -> Optional[tuple[str, dict[str, Any]]]:
        docker_file = codebase / "odoo" / "Dockerfile"
        if not docker_file.is_file():
            return super().detect(codebase)
        with open(docker_file) as f:
            if "odoo-image" in f.read():
                addons_dirs = []
                for item in (codebase / "odoo/external-src").iterdir():
                    if item.is_dir():
                        addons_dirs.append(item)
                return (
                    "Camptocamp",
                    {
                        "addons_dirs": addons_dirs,
                        "addons_dir": [codebase / "odoo/local-src"],
                        "odoo_dir": [
                            codebase / "odoo/src/addons",
                            codebase / "odoo/src/odoo/addons",
                        ],
                    },
                )
        return super().detect(codebase)


class OdooShDetector(CodeBaseDetector):
    """
    Follow Odoo.sh mode
    src/
    ├── enterprise/         # Odoo Enterprise
    ├── odoo/               # Odoo core
    └── themes/
    ├── user/               # user's submodule
    │   └── OCA/
    """

    def detect(self, codebase: Path) -> Optional[tuple[str, dict[str, Any]]]:
        if (
            (codebase / "enterprise").is_dir()
            and (codebase / "odoo").is_dir()
            and (codebase / "themes").is_dir()
            and (codebase / "user").is_dir()
        ):
            addons_dirs = [codebase / "enterprise", codebase / "themes"]
            for item in (codebase / "user").iterdir():
                if item.is_dir():
                    addons_dirs.append(item)
            return (
                "odoo.sh",
                {
                    "addons_dirs": addons_dirs,
                    "addons_dir": [codebase / "project"],
                    "odoo_dir": [
                        codebase / "odoo/addons",
                        codebase / "odoo/odoo/addons",
                    ],
                },
            )
        return super().detect(codebase)


class GenericDetector(CodeBaseDetector):
    """
    A fallback detector that looks for any folder that contains __manifest__.py
    """

    def detect(self, codebase: Path) -> Optional[tuple[str, dict[str, Any]]]:
        manifest_files = glob.glob(str(codebase / "**" / "__manifest__.py"), recursive=True)
        if not manifest_files:
            return super().detect(codebase)

        addons_dirs = set()
        for manifest_file in manifest_files:
            addons_dirs.add(Path(manifest_file).parent.parent)

        return "fallback", {"addons_dirs": list(addons_dirs)}

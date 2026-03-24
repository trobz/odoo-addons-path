from .cli import app
from .main import (
    check_version_consistency,
    detect_codebase_layout,
    get_addons_path,
    get_odoo_version,
    get_odoo_version_from_addons,
    get_odoo_version_from_release,
)

__all__ = [
    "app",
    "check_version_consistency",
    "detect_codebase_layout",
    "get_addons_path",
    "get_odoo_version",
    "get_odoo_version_from_addons",
    "get_odoo_version_from_release",
]

from .cli import app
from .main import detect_codebase_layout, get_addons_path, get_odoo_version_from_release

__all__ = ["app", "detect_codebase_layout", "get_addons_path", "get_odoo_version_from_release"]

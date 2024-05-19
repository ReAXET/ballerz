"""General utilities for the backend."""
from __future__ import annotations

import platform
import re
import sys
import unicodedata
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from typing import TYPE_CHECKING, Any


from loguru import logger



if TYPE_CHECKING:
    from types import ModuleType


__all__ = (
    "check_email",
    "slugify",
    "module_to_os_path",
    "import_string",
)


def check_email(email: str) -> str:
    """Check if an email is valid."""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email")
    return email.lower()


def slugify(value: str, allow_unicode: bool = False, seperator: str | None = None) -> str:
    """Convert a string to a slug."""
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).lower()
    if seperator is not None:
        return re.sub(r"[-\s]+", "-", value).strip("-_").replace("-", seperator)
    return re.sub(r"[-\s]+", "-", value).strip("-_")



def module_to_os_path(dotted_path: str = "backend") -> str:
    """Convert a module path to an OS path."""
    src = find_spec(dotted_path)
    if src is None:
        msg = "Couldn't find the path for %s"
        raise TypeError(msg, dotted_path)
    path_separator = "\\" if platform.system() == "Windows" else "/"
    return Path(str(src.origin).removesuffix(f"{path_separator}__init__.py"))


def import_string(dotted_path: str) -> Any:
    """Import a module path."""
    def _is_loaded(module: ModuleType | None) -> bool:
        spec = getattr(module, "__spec__", None)
        initializing = getattr(spec, "_initializing", False)
        return bool(module and spec and not initializing)
    
    def _cached_import(module_path: str, class_name: str) -> Any:
        module = sys.modules.get(module_path)
        if not _is_loaded(module):
            module = import_module(module_path)
        return getattr(module, class_name)
    
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as e:
        logger.error("Invalid import string: %s", e)
        raise

    try:
        return _cached_import(module_path, class_name)
    except (AttributeError, ModuleNotFoundError) as e:
        logger.error("Could not import %s: %s", dotted_path, e)
        raise



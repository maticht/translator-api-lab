from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def _default_runtime_root() -> Path:
    if os.getenv("VERCEL"):
        # Vercel functions expose only /tmp as writable storage.
        return Path("/tmp/ru-en-translation-service")
    return PROJECT_ROOT / ".runtime"


RUNTIME_ROOT = Path(os.getenv("LT_RUNTIME_ROOT", _default_runtime_root())).resolve()
ARGOS_ROOT = RUNTIME_ROOT / "argos"
XDG_DATA_HOME = ARGOS_ROOT / "xdg-data"
XDG_CACHE_HOME = ARGOS_ROOT / "xdg-cache"
XDG_CONFIG_HOME = ARGOS_ROOT / "xdg-config"
ARGOS_PACKAGES_DIR = ARGOS_ROOT / "packages"

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


def configure_runtime_environment() -> None:
    os.environ.setdefault("XDG_DATA_HOME", str(XDG_DATA_HOME))
    os.environ.setdefault("XDG_CACHE_HOME", str(XDG_CACHE_HOME))
    os.environ.setdefault("XDG_CONFIG_HOME", str(XDG_CONFIG_HOME))
    os.environ.setdefault("ARGOS_PACKAGES_DIR", str(ARGOS_PACKAGES_DIR))

    for path in (
        RUNTIME_ROOT,
        ARGOS_ROOT,
        XDG_DATA_HOME,
        XDG_CACHE_HOME,
        XDG_CONFIG_HOME,
        ARGOS_PACKAGES_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)


configure_runtime_environment()

from libretranslate.app import create_app
from libretranslate.main import get_parser


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False

    return default


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def build_service_args():
    args = get_parser().parse_args([])

    args.host = os.getenv("LT_SERVICE_HOST", os.getenv("LT_HOST", "0.0.0.0"))
    args.port = int(os.getenv("PORT", os.getenv("LT_SERVICE_PORT", str(args.port))))
    args.load_only = _split_csv(
        os.getenv("LT_SERVICE_LOAD_ONLY", os.getenv("LT_LOAD_ONLY", "en,ru"))
    ) or ["en", "ru"]
    args.disable_web_ui = _env_bool("LT_DISABLE_WEB_UI", True)
    args.disable_files_translation = _env_bool(
        "LT_DISABLE_FILES_TRANSLATION", True
    )
    if isinstance(args.translation_cache, str):
        args.translation_cache = _split_csv(args.translation_cache)

    if args.url_prefix and not args.url_prefix.startswith("/"):
        args.url_prefix = "/" + args.url_prefix

    return args


def create_service_app(args=None):
    service_args = args or build_service_args()
    return create_app(service_args)

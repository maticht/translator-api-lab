from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from service_config import ARGOS_PACKAGES_DIR, RUNTIME_ROOT, build_service_args
from libretranslate.init import check_and_install_models


def main() -> None:
    args = build_service_args()
    print(f"Preparing translation runtime in {RUNTIME_ROOT}")
    print(f"Installing Argos packages into {ARGOS_PACKAGES_DIR}")
    print(f"Loading only languages: {','.join(args.load_only)}")
    check_and_install_models(force=True, load_only_lang_codes=args.load_only)


if __name__ == "__main__":
    main()

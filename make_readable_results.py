"""Deprecated location. The implementation now lives in scripts/make_readable_results.py.

This thin shim keeps the old command `python make_readable_results.py` working. Prefer:

    python scripts/make_readable_results.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

from make_readable_results import main  # noqa: E402

if __name__ == "__main__":
    main()

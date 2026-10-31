"""Pytest configuration and shared test fixtures."""

import sys
from pathlib import Path

# Add src directory to path for imports
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

"""Integration tests for the GraphLab CLI."""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SRC_DIR = REPO_ROOT / "src"


def run_cli(*args):
    """Run the CLI via subprocess and return (returncode, stdout, stderr)."""
    env = os.environ.copy()
    src_str = str(SRC_DIR)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{src_str}{os.pathsep}{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = src_str

    cmd = [sys.executable, "-m", "graphlab.cli", *args]
    res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
    return res.returncode, res.stdout, res.stderr


def test_cli_small_dag():
    code, stdout, stderr = run_cli(str(DATA_DIR / "small-dag.csv"))
    assert code == 0
    assert stderr == ""
    assert "Vertices: 9" in stdout
    assert "Edges: 9" in stdout
    assert "  watch" in stdout
    assert "  undershorts -> pants" in stdout
    assert "  socks -> shoes" in stdout


def test_cli_cs_curriculum():
    code, stdout, stderr = run_cli(str(DATA_DIR / "cs-curriculum.csv"))
    assert code == 0
    assert stderr == ""
    assert "Vertices: 19" in stdout
    assert "Edges: 23" in stdout
    assert "  Algorithms" in stdout
    assert "  Data Structures -> Algorithms" in stdout


def test_cli_build_with_cycle():
    code, stdout, stderr = run_cli(str(DATA_DIR / "build-with-cycle.csv"))
    assert code == 0
    assert stderr == ""
    assert "Vertices: 11" in stdout
    assert "Edges: 13" in stdout
    assert "  metrics -> metrics" in stdout
    assert "  auth -> session" in stdout


def test_cli_missing_argument():
    code, stdout, stderr = run_cli()
    assert code == 2
    assert "Error:" in stderr


def test_cli_file_not_found(tmp_path):
    missing_file = tmp_path / "does_not_exist.csv"
    code, stdout, stderr = run_cli(str(missing_file))
    assert code == 2
    assert "Error:" in stderr
    assert "File not found" in stderr


def test_cli_empty_file(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    code, stdout, stderr = run_cli(str(empty))
    assert code == 1
    assert "Error:" in stderr
    assert "empty" in stderr.lower()


def test_cli_malformed_csv_missing_source(tmp_path):
    malformed = tmp_path / "malformed.csv"
    malformed.write_text("source,target\n,target_only\n", encoding="utf-8")
    code, stdout, stderr = run_cli(str(malformed))
    assert code == 1
    assert "Error:" in stderr
    assert "missing source" in stderr.lower()


def test_cli_module_execution_via_package():
    """Verify python -m graphlab works cleanly via __main__.py."""
    env = os.environ.copy()
    src_str = str(SRC_DIR)
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{src_str}{os.pathsep}{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = src_str

    cmd = [sys.executable, "-m", "graphlab", str(DATA_DIR / "small-dag.csv")]
    res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
    assert res.returncode == 0
    assert "Vertices: 9" in res.stdout

"""Unit tests for CSVLoader and CSV parsing edge cases."""

import pytest
from pathlib import Path
from graphlab.loader import CSVLoader
from graphlab.errors import DataValidationError, FileAccessError

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


def test_load_small_dag():
    graph = CSVLoader.load_from_path(DATA_DIR / "small-dag.csv")
    assert graph.vertex_count() == 9
    assert graph.edge_count() == 9
    assert "watch" in graph.get_vertices()
    assert ("undershorts", "pants") in graph.get_edges()


def test_load_cs_curriculum_deduplication():
    graph = CSVLoader.load_from_path(DATA_DIR / "cs-curriculum.csv")
    assert graph.vertex_count() == 19
    assert graph.edge_count() == 23
    assert ("Data Structures", "Algorithms") in graph.get_edges()
    # Check deduplication occurred
    assert len([e for e in graph.get_edges() if e == ("Data Structures", "Algorithms")]) == 1


def test_load_build_with_cycle_and_self_loop():
    graph = CSVLoader.load_from_path(DATA_DIR / "build-with-cycle.csv")
    assert graph.vertex_count() == 11
    assert graph.edge_count() == 13
    assert ("metrics", "metrics") in graph.get_edges()


def test_file_not_found(tmp_path):
    missing = tmp_path / "nonexistent.csv"
    with pytest.raises(FileAccessError):
        CSVLoader.load_from_path(missing)


def test_empty_file_error(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(DataValidationError):
        CSVLoader.load_from_path(empty)


def test_invalid_header_error(tmp_path):
    bad_header = tmp_path / "bad_header.csv"
    bad_header.write_text("foo,bar\na,b\n", encoding="utf-8")
    with pytest.raises(DataValidationError):
        CSVLoader.load_from_path(bad_header)


def test_missing_source_rejected(tmp_path):
    missing_src = tmp_path / "missing_src.csv"
    missing_src.write_text("source,target\n,destination\n", encoding="utf-8")
    with pytest.raises(DataValidationError):
        CSVLoader.load_from_path(missing_src)


def test_invalid_column_count_rejected(tmp_path):
    invalid_cols = tmp_path / "invalid_cols.csv"
    invalid_cols.write_text("source,target\na,b,c\n", encoding="utf-8")
    with pytest.raises(DataValidationError):
        CSVLoader.load_from_path(invalid_cols)


def test_whitespace_trimmed_and_bom_support(tmp_path):
    bom_file = tmp_path / "bom.csv"
    # Write actual UTF-8 BOM bytes \xef\xbb\xbf
    bom_file.write_bytes(b"\xef\xbb\xbfsource,target\n  Alpha  ,  Beta  \nGamma,\n")
    graph = CSVLoader.load_from_path(bom_file)
    assert graph.vertex_count() == 3
    assert graph.edge_count() == 1
    assert graph.get_vertices() == ["Alpha", "Beta", "Gamma"]
    assert graph.get_edges() == [("Alpha", "Beta")]

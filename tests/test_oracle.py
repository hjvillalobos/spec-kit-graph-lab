"""Oracle tests using NetworkX to verify custom graph correctness."""

import pytest
import csv
from pathlib import Path
import networkx as nx
from graphlab.loader import CSVLoader

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


def load_networkx_graph(path: Path) -> nx.DiGraph:
    """Helper to parse the CSV into a NetworkX DiGraph according to spec rules."""
    G = nx.DiGraph()
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row or not any(row):
                continue
            src = row[0].strip()
            dst = row[1].strip() if len(row) > 1 else ""
            if src:
                G.add_node(src)
            if dst:
                G.add_node(dst)
                G.add_edge(src, dst)
    return G


@pytest.mark.parametrize("filename", ["small-dag.csv", "cs-curriculum.csv", "build-with-cycle.csv"])
def test_oracle_matches_networkx(filename):
    file_path = DATA_DIR / filename
    custom_graph = CSVLoader.load_from_path(file_path)
    nx_graph = load_networkx_graph(file_path)

    # 1. Verify vertex sets match exactly
    assert set(custom_graph.get_vertices()) == set(nx_graph.nodes())
    assert custom_graph.vertex_count() == nx_graph.number_of_nodes()

    # 2. Verify edge sets match exactly
    assert set(custom_graph.get_edges()) == set(nx_graph.edges())
    assert custom_graph.edge_count() == nx_graph.number_of_edges()

    # 3. Verify ordering is lexicographical
    assert custom_graph.get_vertices() == sorted(list(nx_graph.nodes()))
    assert custom_graph.get_edges() == sorted(list(nx_graph.edges()))

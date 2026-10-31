"""Unit tests for topological sorting and cycle diagnosis algorithms."""

import pytest
from graphlab.core import DirectedGraph
from graphlab.algo import TopologicalSorter, CycleDiagnosis
from graphlab.errors import CycleDetectedError


def test_sort_empty_graph():
    graph = DirectedGraph()
    sorter = TopologicalSorter()
    assert sorter.sort(graph) == []


def test_sort_linear_dag():
    graph = DirectedGraph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    sorter = TopologicalSorter()
    assert sorter.sort(graph) == ["A", "B", "C"]


def test_sort_deterministic_tie_break():
    graph = DirectedGraph()
    # Both B and A point to C. A < B lexicographically.
    graph.add_edge("B", "C")
    graph.add_edge("A", "C")
    sorter = TopologicalSorter()
    assert sorter.sort(graph) == ["A", "B", "C"]


def test_sort_with_isolated_vertex():
    graph = DirectedGraph()
    graph.add_edge("B", "C")
    graph.add_vertex("A")  # In-degree 0, A < B
    graph.add_vertex("Z")  # In-degree 0, Z > B
    sorter = TopologicalSorter()
    # A (0), B (0), Z (0) initially ready:
    # A is popped, then B is popped (freeing C), C < Z so C is popped, then Z is popped
    assert sorter.sort(graph) == ["A", "B", "C", "Z"]


def test_cycle_self_loop():
    graph = DirectedGraph()
    graph.add_edge("loop", "loop")
    sorter = TopologicalSorter()
    with pytest.raises(CycleDetectedError) as exc_info:
        sorter.sort(graph)
    diag = exc_info.value.diagnosis
    assert isinstance(diag, CycleDiagnosis)
    assert "loop" in diag.cycle_vertices
    assert diag.blocked_vertices == set()
    assert ["loop", "loop"] in diag.cycle_paths


def test_cycle_indirect_with_blocked_nodes():
    graph = DirectedGraph()
    # Independent roots
    graph.add_edge("start", "cycle1")
    # Cycle: cycle1 -> cycle2 -> cycle1
    graph.add_edge("cycle1", "cycle2")
    graph.add_edge("cycle2", "cycle1")
    # Blocked nodes depending on cycle
    graph.add_edge("cycle2", "blocked1")
    graph.add_edge("blocked1", "blocked2")

    sorter = TopologicalSorter()
    with pytest.raises(CycleDetectedError) as exc_info:
        sorter.sort(graph)

    diag = exc_info.value.diagnosis
    assert diag.cycle_vertices == {"cycle1", "cycle2"}
    assert diag.blocked_vertices == {"blocked1", "blocked2"}
    assert any("cycle1" in path and "cycle2" in path for path in diag.cycle_paths)


def test_cycle_diagnosis_formatting():
    diag = CycleDiagnosis(
        cycle_paths=[["auth", "session", "user-profile", "auth"], ["metrics", "metrics"]],
        cycle_vertices={"auth", "session", "user-profile", "metrics"},
        blocked_vertices={"api", "web"},
    )
    report = diag.format_report()
    assert "Cycles detected:" in report
    assert "auth -> session -> user-profile -> auth" in report
    assert "metrics -> metrics" in report
    assert "Blocked vertices (not in cycle):" in report
    assert "  - api" in report
    assert "  - web" in report

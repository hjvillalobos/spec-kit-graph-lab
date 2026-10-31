"""Unit tests for DirectedGraph core in-memory operations."""

import pytest
from graphlab.core import DirectedGraph


def test_empty_graph():
    graph = DirectedGraph()
    assert graph.vertex_count() == 0
    assert graph.edge_count() == 0
    assert graph.get_vertices() == []
    assert graph.get_edges() == []


def test_add_vertex_idempotent():
    graph = DirectedGraph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("A")  # idempotent
    assert graph.vertex_count() == 2
    assert graph.get_vertices() == ["A", "B"]
    assert graph.edge_count() == 0


def test_add_edge_and_deduplication():
    graph = DirectedGraph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "B")  # duplicate edge
    assert graph.vertex_count() == 2
    assert graph.edge_count() == 1
    assert graph.get_vertices() == ["A", "B"]
    assert graph.get_edges() == [("A", "B")]


def test_self_loop():
    graph = DirectedGraph()
    graph.add_edge("metrics", "metrics")
    assert graph.vertex_count() == 1
    assert graph.edge_count() == 1
    assert graph.get_vertices() == ["metrics"]
    assert graph.get_edges() == [("metrics", "metrics")]


def test_isolated_vertex_addition():
    graph = DirectedGraph()
    graph.add_edge("pants", "shoes")
    graph.add_vertex("watch")  # isolated vertex
    assert graph.vertex_count() == 3
    assert graph.edge_count() == 1
    assert graph.get_vertices() == ["pants", "shoes", "watch"]
    assert graph.get_edges() == [("pants", "shoes")]


def test_deterministic_lexicographical_sorting():
    graph = DirectedGraph()
    graph.add_edge("zebra", "apple")
    graph.add_edge("banana", "cat")
    graph.add_vertex("mango")
    assert graph.get_vertices() == ["apple", "banana", "cat", "mango", "zebra"]
    assert graph.get_edges() == [("banana", "cat"), ("zebra", "apple")]


def test_empty_vertex_name_rejected():
    graph = DirectedGraph()
    with pytest.raises(ValueError):
        graph.add_vertex("")
    with pytest.raises(ValueError):
        graph.add_edge("", "A")
    with pytest.raises(ValueError):
        graph.add_edge("A", "")

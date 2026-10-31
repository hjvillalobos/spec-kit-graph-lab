"""Core DirectedGraph data structure for GraphLab.

Implemented using native Python collections without external graph libraries.
"""

from typing import List, Tuple, Set, Dict


class DirectedGraph:
    """Represents an unweighted directed graph with optional self-loops and isolated vertices."""

    def __init__(self) -> None:
        self._vertices: Set[str] = set()
        self._adjacency: Dict[str, Set[str]] = {}

    def add_vertex(self, vertex: str) -> None:
        """Register a vertex in the graph.

        Raises ValueError if vertex is empty.
        """
        if not vertex:
            raise ValueError("Vertex identifier cannot be empty.")
        self._vertices.add(vertex)
        if vertex not in self._adjacency:
            self._adjacency[vertex] = set()

    def add_edge(self, source: str, target: str) -> None:
        """Add a directed edge from source to target.

        Registers both source and target if not already present.
        Deduplicates parallel edges idempotently.
        Supports self-loops (source == target).
        """
        if not source or not target:
            raise ValueError("Edge endpoints cannot be empty.")
        self.add_vertex(source)
        self.add_vertex(target)
        self._adjacency[source].add(target)

    def vertex_count(self) -> int:
        """Return total number of unique vertices."""
        return len(self._vertices)

    def edge_count(self) -> int:
        """Return total number of unique directed edges."""
        return sum(len(targets) for targets in self._adjacency.values())

    def get_vertices(self) -> List[str]:
        """Return all unique vertices sorted in ascending lexicographical order."""
        return sorted(list(self._vertices))

    def get_edges(self) -> List[Tuple[str, str]]:
        """Return all unique directed edges sorted in ascending lexicographical order."""
        edges: List[Tuple[str, str]] = []
        for src in self._vertices:
            for dst in self._adjacency.get(src, set()):
                edges.append((src, dst))
        return sorted(edges)

    def get_successors(self, vertex: str) -> Set[str]:
        """Return a copy of the outgoing neighbors set for the given vertex."""
        return set(self._adjacency.get(vertex, set()))

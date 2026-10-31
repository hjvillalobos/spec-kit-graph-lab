"""Topological sorting and cycle diagnosis algorithms for GraphLab.

Implemented using Kahn's algorithm (with min-heap) and Tarjan's SCC analysis.
Strictly zero external graph libraries in production.
"""

import heapq
from typing import List, Set, Dict, Optional
from graphlab.core import DirectedGraph
from graphlab.errors import CycleDetectedError


class CycleDiagnosis:
    """Detailed diagnosis of cycles and blocked downstream nodes."""

    def __init__(
        self,
        cycle_paths: List[List[str]],
        cycle_vertices: Set[str],
        blocked_vertices: Set[str],
    ) -> None:
        self.cycle_paths = cycle_paths
        self.cycle_vertices = cycle_vertices
        self.blocked_vertices = blocked_vertices

    def format_report(self) -> str:
        """Format the diagnosis into a human-readable diagnostic report for stderr."""
        lines = [
            "Error: Graph contains cycle(s). Topological ordering is not possible.",
            "Cycles detected:",
        ]
        if self.cycle_paths:
            for path in self.cycle_paths:
                lines.append(f"  - {' -> '.join(path)}")
        else:
            for v in sorted(self.cycle_vertices):
                lines.append(f"  - {v} (participating in cycle)")

        if self.blocked_vertices:
            lines.append("Blocked vertices (not in cycle):")
            for v in sorted(self.blocked_vertices):
                lines.append(f"  - {v}")

        return "\n".join(lines)


class TopologicalSorter:
    """Computes deterministic topological orders for DAGs or diagnoses cycles."""

    @classmethod
    def sort(cls, graph: DirectedGraph) -> List[str]:
        """Compute and return a deterministic topological sort of the graph.

        Uses Kahn's algorithm with a min-heap priority queue for deterministic
        lexicographical tie-breaking.
        Raises CycleDetectedError if the graph contains cycles.
        """
        all_vertices = graph.get_vertices()
        if not all_vertices:
            return []

        # 1. Compute in-degree for all vertices
        in_degree: Dict[str, int] = {v: 0 for v in all_vertices}
        for u in all_vertices:
            for v in graph.get_successors(u):
                in_degree[v] += 1

        # 2. Min-heap of all vertices with in-degree 0
        heap: List[str] = [v for v, deg in in_degree.items() if deg == 0]
        heapq.heapify(heap)

        order: List[str] = []

        # 3. Process vertices layer by layer
        while heap:
            u = heapq.heappop(heap)
            order.append(u)
            for v in sorted(graph.get_successors(u)):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    heapq.heappush(heap, v)

        # 4. Check if all vertices were scheduled
        if len(order) == len(all_vertices):
            return order

        # 5. Graph contains cycles. Perform cycle diagnosis on unscheduled vertices
        diagnosis = cls._diagnose_cycles(graph, order)
        raise CycleDetectedError(diagnosis.format_report(), diagnosis=diagnosis)

    @classmethod
    def _diagnose_cycles(cls, graph: DirectedGraph, scheduled: List[str]) -> CycleDiagnosis:
        """Identify actual cycle paths vs blocked downstream vertices."""
        unscheduled: Set[str] = set(graph.get_vertices()) - set(scheduled)

        # Induced subgraph on unscheduled nodes
        adj_u: Dict[str, Set[str]] = {
            u: (graph.get_successors(u) & unscheduled) for u in unscheduled
        }

        # Tarjan's Strongly Connected Components algorithm
        index = 0
        indices: Dict[str, int] = {}
        lowlink: Dict[str, int] = {}
        on_stack: Dict[str, bool] = {}
        stack: List[str] = []
        sccs: List[List[str]] = []

        def strongconnect(v: str) -> None:
            nonlocal index
            indices[v] = index
            lowlink[v] = index
            index += 1
            stack.append(v)
            on_stack[v] = True

            for w in sorted(adj_u.get(v, set())):
                if w not in indices:
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif on_stack.get(w, False):
                    lowlink[v] = min(lowlink[v], indices[w])

            if lowlink[v] == indices[v]:
                scc: List[str] = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == v:
                        break
                sccs.append(scc)

        for node in sorted(unscheduled):
            if node not in indices:
                strongconnect(node)

        cycle_vertices: Set[str] = set()
        blocked_vertices: Set[str] = set()
        cycle_paths: List[List[str]] = []

        for scc in sccs:
            if len(scc) > 1:
                # Cycle component
                cycle_vertices.update(scc)
                path = cls._find_cycle_path(scc, adj_u)
                cycle_paths.append(path)
            else:
                node = scc[0]
                if node in adj_u.get(node, set()):
                    # Self-loop
                    cycle_vertices.add(node)
                    cycle_paths.append([node, node])
                else:
                    # Blocked vertex (has in-degree > 0 from cycle, but no loop)
                    blocked_vertices.add(node)

        # Sort cycle paths deterministically by starting node
        cycle_paths.sort(key=lambda p: (len(p), p[0] if p else ""))

        return CycleDiagnosis(
            cycle_paths=cycle_paths,
            cycle_vertices=cycle_vertices,
            blocked_vertices=blocked_vertices,
        )

    @classmethod
    def _find_cycle_path(cls, scc: List[str], adj: Dict[str, Set[str]]) -> List[str]:
        """Find an elementary directed cycle within an SCC."""
        scc_set = set(scc)
        for start in sorted(scc):
            def dfs(curr: str, path: List[str]) -> Optional[List[str]]:
                for nxt in sorted(adj.get(curr, set())):
                    if nxt not in scc_set:
                        continue
                    if nxt == start and len(path) >= 1:
                        return path + [start]
                    if nxt not in path:
                        res = dfs(nxt, path + [nxt])
                        if res is not None:
                            return res
                return None

            result = dfs(start, [start])
            if result:
                return result

        # Fallback to circular representation
        sorted_scc = sorted(scc)
        return sorted_scc + [sorted_scc[0]]

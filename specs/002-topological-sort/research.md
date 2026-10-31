# Research & Design Decisions: Topological Sorting and Cycle Diagnosis

**Feature Branch**: `002-topological-sort`
**Date**: 2026-10-31

## 1. Topological Sorting Algorithm Choice

### Decision
Use **Kahn's Algorithm with a Min-Heap (Priority Queue)** from Python's standard library `heapq`.

### Rationale
- **Deterministic Tie-Breaking**:
  - In a dependency graph, multiple vertices often have in-degree 0 simultaneously (e.g., initial courses in a curriculum or garments with no prerequisites).
  - Using a min-heap guarantees that whenever a choice exists, the lexicographically smallest vertex is selected next in $O(\log V)$ time.
- **In-Memory Compatibility**:
  - The in-memory adjacency list from Feature 1 (`dict[str, set[str]]` and `set[str]`) supports computing initial in-degrees in $O(V + E)$ time without modifying Feature 1's core structure.
- **Cycle Detection Guarantee**:
  - If the output list length is strictly less than the total vertex count, a cycle is guaranteed to exist.
- **Complexity**:
  - Time: $O(V \log V + E)$, well below the 100ms requirement for thousands of vertices.
  - Space: $O(V)$ auxiliary memory for in-degree counts and heap.

### Alternatives Considered and Rejected
1. **DFS-based Topological Sort (Post-Order Reversal)**:
   - *Rejected*: While $O(V + E)$, enforcing a deterministic tie-break with DFS requires sorting neighbors at every node and can produce non-intuitive scheduling (it traverses deep into one branch before visiting independent roots). Kahn's algorithm processes dependencies layer-by-layer (BFS-like), which is the natural mental model for build systems and academic schedules.
2. **Third-Party Libraries (`graphlib.TopologicalSorter`, `networkx.topological_sort`)**:
   - *Rejected for production*: Strictly prohibited by Constitution Principle II. Used solely in tests as verification oracles.

---

## 2. Cycle Diagnosis: Cycle Vertices vs. Blocked Vertices

### Decision
When Kahn's algorithm terminates with unscheduled vertices $U = V \setminus \text{scheduled}$, isolate the actual cycles and distinguish them from blocked downstream vertices using **Strongly Connected Components (SCC)**:
1. Induced subgraph on $U$: Consider only edges $(u, v)$ where both $u \in U$ and $v \in U$.
2. Compute SCCs on this induced subgraph using Tarjan's algorithm.
3. Classify components:
   - **Cycle Components**: Any SCC containing $\ge 2$ vertices, or a single vertex with a self-loop $(u, u)$.
   - **Blocked Vertices**: Any vertex in $U$ belonging to a trivial SCC of size 1 with no self-loop. These vertices cannot be scheduled because they depend on upstream cycle nodes, but they are not themselves part of any circular loop (e.g., `api` and `web` in `build-with-cycle.csv`).
4. Reconstruct representative cycle paths using DFS within each cycle SCC for crystal-clear reporting (e.g., `auth -> session -> user-profile -> auth` and `metrics -> metrics`).

---

## 3. CLI Interface Contract

### Decision
- Command: `py -m graphlab <path_to_csv> --sort`
- Exit Code:
  - `0`: DAG sorted successfully.
  - `1`: Graph contains cycles (or data validation error).
  - `2`: File not found / CLI argument error.
- Output Streams:
  - `stdout`: Deterministic topological order when successful.
  - `stderr`: Structured cycle diagnostics when cyclic.

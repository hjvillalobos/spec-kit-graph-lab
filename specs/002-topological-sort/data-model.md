# Data Model: Topological Sorting and Cycle Diagnosis

**Feature Branch**: `002-topological-sort`
**Date**: 2026-10-31

## Entities & Interfaces

### 1. `CycleDiagnosis`

Container entity holding the diagnostic breakdown when a graph contains cycles.

#### Attributes
- `cycle_paths: List[List[str]]`:
  - List of detected directed cycle sequences, e.g. `[['auth', 'session', 'user-profile', 'auth'], ['metrics', 'metrics']]`.
- `cycle_vertices: Set[str]`:
  - Set of all vertices that participate directly in at least one cycle.
- `blocked_vertices: Set[str]`:
  - Set of vertices that cannot be processed due to upstream dependencies on cycles, but do NOT participate in any cycle themselves.

#### Methods
- `format_report() -> str`:
  - Returns a formatted string for `stderr` detailing detected cycles and blocked vertices.

---

### 2. `TopologicalSorter`

Engine responsible for sorting DAGs or diagnosing cycles using custom in-house algorithms.

#### Methods
- `sort(graph: DirectedGraph) -> List[str]`:
  - Runs Kahn's algorithm with a min-heap priority queue.
  - Returns the deterministic topological sort list if graph is a DAG.
  - Raises `CycleDetectedError(diagnosis)` if the graph contains cycles.

---

### 3. Error Classes

- `CycleDetectedError(GraphLabError)`:
  - Raised when a topological order cannot be computed due to cycles.
  - Contains `diagnosis: CycleDiagnosis`.
  - Default `exit_code: int = 1`.

# Data Model: Directed Graph Loading and Inspection

**Feature Branch**: `001-directed-graphs`
**Date**: 2026-10-30

## Entities & Data Structures

### 1. `DirectedGraph`

Core in-memory entity representing an unweighted directed graph with optional self-loops and isolated vertices.

#### Attributes
- `_vertices: set[str]`
  - Set of all registered vertex identifiers.
  - Invariant: Contains no empty strings; all names trimmed of outer whitespace.
- `_adjacency: dict[str, set[str]]`
  - Mapping from a source vertex `u` to a set of destination vertices `{v_1, v_2, ...}` representing directed edges `u -> v_i`.
  - Invariant: For every key `u` and every element `v` in `_adjacency[u]`, both `u in _vertices` and `v in _vertices` hold true.

#### Methods & Invariants
- `add_vertex(v: str) -> None`:
  - Registers `v` in `_vertices` and initializes `_adjacency[v] = set()` if not already present.
  - Idempotent: Calling `add_vertex` on an existing vertex does not modify existing outgoing edges.
  - Precondition: `v` is a non-empty string.
- `add_edge(u: str, v: str) -> None`:
  - Ensures both `u` and `v` are registered in `_vertices`.
  - Inserts `v` into `_adjacency[u]`.
  - Idempotent: Duplicate insertions do not create parallel edges. Self-loops (`u == v`) are allowed and stored as `u in _adjacency[u]`.
- `vertex_count() -> int`:
  - Returns `len(_vertices)`.
- `edge_count() -> int`:
  - Returns $\sum_{u} \text{len}(\_adjacency[u])$.
- `get_vertices() -> list[str]`:
  - Returns `sorted(list(_vertices))` in ascending lexicographical order.
- `get_edges() -> list[tuple[str, str]]`:
  - Returns `sorted([(u, v) for u in _vertices for v in _adjacency.get(u, set())])` in ascending lexicographical order.

---

### 2. `CSVLoader`

Parser entity responsible for validating CSV file structure and populating a `DirectedGraph`.

#### Responsibilities
- Open file using `utf-8-sig`.
- Read and validate header: must contain `source` and `target` in the first non-empty line.
- For each row:
  - If empty: skip.
  - If length $\neq 2$: raise `DataValidationError("Row has invalid number of columns")`.
  - Strip outer whitespace: `src = row[0].strip()`, `dst = row[1].strip()`.
  - If `src == ""` and `dst != ""`: raise `DataValidationError("Missing source vertex in row")`.
  - If `src != ""` and `dst == ""`: call `graph.add_vertex(src)` (isolated vertex).
  - If `src != ""` and `dst != ""`: call `graph.add_edge(src, dst)`.
- Returns populated `DirectedGraph`.

---

### 3. Error Classes

- `GraphLabError(Exception)`: Base application error.
  - `exit_code: int`
- `DataValidationError(GraphLabError)`: Raised on malformed rows, invalid headers, or empty files.
  - `exit_code: int = 1`
- `FileAccessError(GraphLabError)`: Raised when the specified input file does not exist or cannot be read.
  - `exit_code: int = 2`

# Research & Design Decisions: Directed Graph Loading and Inspection

**Feature Branch**: `001-directed-graphs`
**Date**: 2026-10-30

## 1. Graph In-Memory Representation

### Decision
Represent the directed graph using an **Adjacency List** backed by native Python standard library types:
- `vertices: set[str]` to store the unique vertex identifiers.
- `adjacency: dict[str, set[str]]` where keys are source vertices and values are sets of target vertices.

### Rationale
- **Time Complexity**:
  - Adding a vertex: $O(1)$ average time.
  - Adding a directed edge: $O(1)$ average time.
  - Checking edge existence `(u, v)`: $O(1)$ average time.
  - Deduplication: Handled naturally and idempotently in $O(1)$ using sets.
  - Self-loops: `u` pointing to `u` is stored cleanly as `u in adjacency[u]`.
  - Iterating outgoing edges: $O(\text{out-degree}(u))$.
- **Space Complexity**:
  - $O(V + E)$ space, which is optimal for sparse graphs (real dependency networks like course curricula or package builds have $E \ll V^2$).
- **Evolution toward Feature 2**:
  - Computing in-degrees for Kahn's topological sort requires scanning edges in $O(V + E)$ or maintaining an `in_degree` map, perfectly supported by this representation without rewrites.

### Alternatives Considered and Rejected
1. **Adjacency Matrix (`list[list[int]]` or 2D boolean array)**:
   - *Rejected*: Requires pre-allocating or continually resizing an $O(V^2)$ grid. For 1000 packages with 2000 dependencies, a matrix allocates $1,000,000$ cells where 99.8% are empty. Finding neighbors requires $O(V)$ operations instead of $O(\text{degree})$.
2. **Edge List (`list[tuple[str, str]]`)**:
   - *Rejected*: Finding outgoing edges or checking if an edge exists takes $O(E)$ linear search. Deduplicating edges takes $O(E)$ per insertion without auxiliary sets.
3. **Graph Libraries (`networkx`, `graphlib`, `igraph`)**:
   - *Rejected for production*: Constitution Principle II strictly prohibits third-party or standard graph modules in production code. (Permitted only in tests as an oracle).

---

## 2. CSV Ingestion & Encoding Strategy

### Decision
- Use Python's built-in `csv.reader`.
- Open files with encoding `utf-8-sig` to automatically and transparently handle both standard UTF-8 and UTF-8 with Byte Order Mark (BOM).
- Trim outer whitespace on each token (`strip()`), while preserving internal casing (case-sensitive).
- Validation:
  - Header validation: First non-empty row must contain exactly two columns matching `source` and `target` (case-insensitive and trimmed). If mismatched, abort with code 1.
  - Data rows:
    - Empty lines: Ignored silently.
    - Columns $\neq 2$: Reject with code 1 and descriptive error in `stderr`.
    - Single-ended row `vertice,`: Treated as an isolated vertex declaration. Add `vertice` to `vertices`; do not add edges.
    - Single-ended row `,destino` (missing source): Reject as malformed with code 1 in `stderr`.
    - Normal row `source,target`: Add both to `vertices`, add directed edge `source -> target` to `adjacency`.

### Rationale
- Robust handling of real-world CSV artifacts without external parsing libraries.
- Explicit compliance with clarified requirements (FR-006, FR-007, FR-010, FR-011).

---

## 3. Deterministic Presentation & CLI Protocol

### Decision
- Built-in `sys.argv` / `argparse` with standard streams:
  - Positional argument: `path` to CSV file.
  - `stdout`: Deterministic, sorted output combining summary counts, vertices, and edges.
  - `stderr`: Informative diagnostic messages on failure.
  - Exit codes:
    - `0`: Success.
    - `1`: Validation/data error (empty file, invalid header, malformed row `,target`, extra columns).
    - `2`: File/system error (file not found, permission denied, missing CLI arguments).

### Output Format Schema
```text
Vertices: <count>
Edges: <count>

Vertices:
  <v_1>
  <v_2>
  ...

Edges:
  <source_1> -> <target_1>
  <source_2> -> <target_2>
  ...
```
Sorted lexicographically (ascending) to guarantee reproducible output across runs and operating systems.

---

## 4. Test Oracle Strategy

### Decision
Use `pytest` for unit and acceptance tests, and integrate `networkx` strictly within test files (`tests/`) as a verification oracle:
- In test fixtures, parse the test CSVs using both our custom `DirectedGraph` implementation and `networkx.DiGraph`.
- Assert that `set(graph.get_vertices()) == set(nx_graph.nodes())`.
- Assert that `set(graph.get_edges()) == set(nx_graph.edges())`.
- Assert that vertex count and edge count strictly match.

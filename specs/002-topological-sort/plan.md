# Implementation Plan: Topological Sorting and Cycle Diagnosis

**Branch**: `002-topological-sort` | **Date**: 2026-10-31 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-topological-sort/spec.md`

## Summary

Extend GraphLab with deterministic topological sorting and precise cycle diagnosis. Topological sorting uses Kahn's algorithm with a min-heap priority queue ($O(V \log V + E)$ time). When cycles exist, an in-house Tarjan's Strongly Connected Components (SCC) analysis isolates true directed cycle components from downstream blocked vertices. The CLI integrates a `--sort` option that preserves existing Feature 1 inspection behavior while providing structured output and diagnostics.

## Technical Context

**Language/Version**: Python 3.11+ (running on Python 3.14 via `py` launcher).

**Primary Dependencies**: Python Standard Library only (`heapq`, `collections`, `sys`, `typing`). Zero external production dependencies.

**Storage**: In-memory adjacency list from Feature 1.

**Testing**: `pytest` and `networkx` as verification oracle (`networkx.topological_sort`, `networkx.is_directed_acyclic_graph`, `networkx.simple_cycles`).

**Target Platform**: Cross-platform CLI.

**Project Type**: Standalone CLI / Modular Python package (`graphlab`).

**Performance Goals**: <50ms for DAG sorting and cycle analysis on realistic datasets.

**Constraints**: Zero production graph libraries (Constitution Principle II). Deterministic tie-breaking via min-heap. Exact cycle vs blocked classification.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (Python 3.11+ & CLI)**: PASS. Uses standard library and CLI flags.
- **Principle II (In-House Graph & Algorithms)**: PASS. Kahn's algorithm and Tarjan's SCC implemented in-house. Zero graph libraries in production.
- **Principle III (Testing & Oracles)**: PASS. Verified against `networkx.topological_sort` and `simple_cycles`.
- **Principle IV (Deterministic Output & Error Handling)**: PASS. Min-heap guarantees deterministic sorting. Exit code 1 on cycles.
- **Principle V (Spec-Code Agreement)**: PASS. Synchronized with `spec.md`.
- **Principle VI (Branch Flow & Phase Commits)**: PASS. Developing on `002-topological-sort`.

## Project Structure

### Documentation (this feature)

```text
specs/002-topological-sort/
├── spec.md              # Feature specification with clarifications
├── plan.md              # Implementation plan
├── research.md          # Kahn's algorithm, min-heap, Tarjan's SCC cycle isolation
├── data-model.md        # CycleDiagnosis, TopologicalSorter, CycleDetectedError
├── quickstart.md        # Execution guide
├── contracts/
│   └── cli-contract.md  # CLI contract with --sort flag
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Modifications

```text
src/
└── graphlab/
    ├── __init__.py      # Export TopologicalSorter, CycleDiagnosis, CycleDetectedError
    ├── core.py          # Existing DirectedGraph (unchanged or extended with helper if needed)
    ├── algo.py          # TopologicalSorter and Tarjan SCC cycle diagnosis
    ├── errors.py        # Add CycleDetectedError
    └── cli.py           # Add --sort argument parsing and cycle report presentation

tests/
├── test_algo.py         # Unit tests for TopologicalSorter (Kahn + cycle diagnosis)
├── test_cli.py          # Extended CLI integration tests with --sort
└── test_oracle.py       # Extended oracle tests against networkx.topological_sort
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| :--- | :--- | :--- |
| *None* | Compliant with all constitutional principles. | N/A |

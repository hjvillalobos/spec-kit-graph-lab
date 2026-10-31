# Implementation Plan: Directed Graph Loading and Inspection

**Branch**: `001-directed-graphs` | **Date**: 2026-10-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-directed-graphs/spec.md`

## Summary

Implement a lightweight, standalone Python 3.11+ CLI application to load, validate, and inspect directed unweighted graphs from CSV files. The graph is stored in-memory using an adjacency list (`dict[str, set[str]]` and `set[str]`) developed entirely in-house without third-party graph libraries in production. The CLI provides deterministic, lexicographically sorted summaries, vertex listings, and edge listings to `stdout`, and handles file and formatting errors via `stderr` with non-zero exit codes.

## Technical Context

**Language/Version**: Python 3.11+ (verified running on Python 3.14 via `py` launcher).

**Primary Dependencies**: Python Standard Library only (`csv`, `sys`, `pathlib`, `typing`). No external production dependencies.

**Storage**: In-memory data structures loaded on-demand from file system CSV files.

**Testing**: `pytest` for test execution and discovery; `networkx` strictly in `tests/` as a verification oracle.

**Target Platform**: Cross-platform CLI (Windows, macOS, Linux).

**Project Type**: Standalone CLI / Modular Python package (`graphlab`).

**Performance Goals**: Sub-second execution (<100ms) for graphs with thousands of vertices and edges.

**Constraints**: Zero external graph libraries in production code (Constitution Principle II). Deterministic lexicographical sorting on output (Constitution Principle IV). Clean error exit codes without raw exception tracebacks.

**Scale/Scope**: Dependency graphs ranging from small debugging sets (~10 nodes) to realistic academic curricula and software build dependency trees (~100–10,000 nodes).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (Python 3.11+ & CLI Architecture)**: PASS. Pure Python 3.11+ package structure with standard streams (`stdin`/args, `stdout`, `stderr`) and clean exit codes.
- **Principle II (In-House Graph Implementation & Zero Production Libraries)**: PASS. Custom `DirectedGraph` class backed by standard `set` and `dict`. Zero graph libraries in production.
- **Principle III (Exhaustive Testing & Verification Oracles)**: PASS. Every acceptance scenario will have corresponding automated tests in `tests/`, verified against `networkx` oracle tests.
- **Principle IV (Deterministic Output & Explicit Error Handling)**: PASS. All vertex and edge outputs are explicitly sorted. Exit codes 1 and 2 map directly to validation and file access errors.
- **Principle V (Strict Spec-Code Agreement)**: PASS. The plan strictly adheres to the clarified requirements in `spec.md`.
- **Principle VI (Branch Flow & Phase Commits)**: PASS. Work proceeds on `001-directed-graphs` with dedicated commits per phase.

## Project Structure

### Documentation (this feature)

```text
specs/001-directed-graphs/
├── spec.md              # Feature specification with clarifications
├── plan.md              # This file (implementation plan)
├── research.md          # In-memory graph choices, CSV handling, oracle strategy
├── data-model.md        # DirectedGraph, CSVLoader, error definitions
├── quickstart.md        # End-to-end run and test instructions
├── contracts/
│   └── cli-contract.md  # CLI command, arguments, exit codes, stream schemas
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
src/
└── graphlab/
    ├── __init__.py      # Package export
    ├── core.py          # DirectedGraph entity and in-memory operations
    ├── loader.py        # CSVLoader and CSV validation logic
    ├── errors.py        # Domain exceptions (DataValidationError, FileAccessError)
    └── cli.py           # CLI argument parsing, presentation, and exit code handling

tests/
├── conftest.py          # Shared fixtures, test dataset paths, oracle helpers
├── test_core.py         # Unit tests for DirectedGraph
├── test_loader.py       # Unit tests for CSVLoader and edge case handling
├── test_cli.py          # End-to-end subprocess CLI tests on sample files
└── test_oracle.py       # Verification oracle tests comparing with networkx
```

**Structure Decision**: Single project layout with clean separation between core data structures (`src/graphlab/core.py`), parser/validation (`src/graphlab/loader.py`), and CLI presentation (`src/graphlab/cli.py`). Tests mirror the structure with dedicated oracle tests.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| :--- | :--- | :--- |
| *None* | No constitutional violations identified. Standard library only. | N/A |

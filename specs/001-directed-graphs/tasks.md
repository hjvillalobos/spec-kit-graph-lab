# Tasks: Directed Graph Loading and Inspection

**Input**: Design documents from `/specs/001-directed-graphs/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/cli-contract.md`, `quickstart.md`).

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/cli-contract.md`.

**Organization**: Tasks are grouped by user story to enable independent implementation and test verification for each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies).
- **[Story]**: User story mapping (`[US1]`, `[US2]`, `[US3]`).
- Exact file paths are specified for every task.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Package layout initialization and core error definitions.

- [ ] T001 Create project directories `src/graphlab` and `tests` per implementation plan
- [ ] T002 [P] Create package initializer and export symbols in `src/graphlab/__init__.py`
- [ ] T003 [P] Implement domain exception classes (`GraphLabError`, `DataValidationError`, `FileAccessError`) in `src/graphlab/errors.py`

---

## Phase 2: Foundational (Core In-Memory Graph)

**Purpose**: In-memory graph data structure without external graph libraries (blocking prerequisite for all stories).

- [ ] T004 Write unit tests for `DirectedGraph` core operations in `tests/test_core.py` covering vertex addition, edge deduplication, self-loops, counts, and sorted getters
- [ ] T005 Implement `DirectedGraph` class in `src/graphlab/core.py` using `set[str]` and `dict[str, set[str]]` with $O(V+E)$ space and $O(1)$ edge operations

**Checkpoint**: Core graph structure ready and tested. User story tasks can now proceed.

---

## Phase 3: User Story 1 - Carga y Consulta de Resumen Estructural (Priority: P1) [MVP]

**Goal**: Load CSV dependency files into `DirectedGraph` and report exact vertex and edge counts.

**Independent Test**: Load `small-dag.csv` (9 vertices, 9 edges), `cs-curriculum.csv` (19 vertices, 23 edges), and `build-with-cycle.csv` (11 vertices, 13 edges) and verify counts.

### Tests for User Story 1

- [ ] T006 [P] [US1] Write unit tests for CSV ingestion and validation in `tests/test_loader.py` covering header checks, isolated vertex `watch,`, deduplicated edges in `cs-curriculum.csv`, and self-loops in `build-with-cycle.csv`
- [ ] T007 [P] [US1] Write verification oracle tests in `tests/test_oracle.py` comparing `DirectedGraph` vertex and edge counts against `networkx.DiGraph` on all sample datasets in `data/`

### Implementation for User Story 1

- [ ] T008 [US1] Implement `CSVLoader` in `src/graphlab/loader.py` with `utf-8-sig` encoding, header validation (`source,target`), whitespace trimming, isolated vertex handling (`u,`), and edge insertion

**Checkpoint**: User Story 1 is functional and verifiable against the `networkx` test oracle.

---

## Phase 4: User Story 2 - Inspección Detallada de Vértices y Aristas (Priority: P1)

**Goal**: Present deterministic, lexicographically sorted listings of all vertices and directed edges in `stdout`.

**Independent Test**: Execute CLI on `small-dag.csv`, `cs-curriculum.csv`, and `build-with-cycle.csv` and verify exact sorted outputs and 0 exit codes.

### Tests for User Story 2

- [ ] T009 [P] [US2] Write CLI integration tests in `tests/test_cli.py` asserting sorted stdout format (`Vertices: N`, `Edges: M`, vertex list, edge list) on sample files

### Implementation for User Story 2

- [ ] T010 [US2] Implement CLI argument parsing, runner function, and formatted stdout presentation in `src/graphlab/cli.py`

**Checkpoint**: User Stories 1 and 2 deliver the complete MVP workflow.

---

## Phase 5: User Story 3 - Robustez de Entrada y Diagnóstico de Anomalías (Priority: P2)

**Goal**: Safely handle real-world CSV anomalies, reject malformed input (missing file, empty file, invalid header, `,target` row) with clean `stderr` messages and non-zero exit codes.

**Independent Test**: Invoke CLI on missing files (exit code 2) and malformed CSVs (exit code 1) and confirm error messages in `stderr` without tracebacks.

### Tests for User Story 3

- [ ] T011 [P] [US3] Write negative scenario integration tests in `tests/test_cli.py` for non-existent files (code 2), empty files (code 1), invalid headers (code 1), and missing source `,target` (code 1)

### Implementation for User Story 3

- [ ] T012 [US3] Implement error trapping and exit code mapping in `src/graphlab/cli.py` ensuring exceptions produce clean messages in `stderr` without tracebacks

**Checkpoint**: All user stories complete with positive and negative testing.

---

## Phase 6: Polish & Verification

**Purpose**: Cross-cutting validation, documentation alignment, and execution checks.

- [ ] T013 [P] Execute CLI manually against `data/small-dag.csv`, `data/cs-curriculum.csv`, and `data/build-with-cycle.csv` verifying against `quickstart.md`
- [ ] T014 Run complete test suite via `pytest` ensuring 100% test pass rate across unit, integration, and oracle test suites

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1; blocks all User Stories.
- **Phase 3 (User Story 1)**: Depends on Phase 2; establishes loader and oracle tests.
- **Phase 4 (User Story 2)**: Depends on Phase 3; adds CLI presentation.
- **Phase 5 (User Story 3)**: Depends on Phase 4; hardens error handling and exit codes.
- **Phase 6 (Polish)**: Depends on all User Stories complete.

### Parallel Opportunities
- T002, T003 can run in parallel in Phase 1.
- T006, T007 can run in parallel in Phase 3.
- T009, T011 can run in parallel once CLI runner skeleton exists.

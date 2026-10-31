# Tasks: Topological Sorting and Cycle Diagnosis

**Input**: Design documents from `/specs/002-topological-sort/` (`spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/cli-contract.md`, `quickstart.md`).

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/cli-contract.md`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel.
- **[Story]**: User story mapping (`[US1]`, `[US2]`, `[US3]`).

---

## Phase 1: Setup

- [ ] T015 [P] Add `CycleDetectedError` domain exception in `src/graphlab/errors.py`

---

## Phase 2: Foundational (Topological Sort Engine & Cycle Diagnosis)

- [ ] T016 Write unit tests in `tests/test_algo.py` covering Kahn's algorithm determinism, self-loop detection, and cycle vs blocked node separation
- [ ] T017 Implement `CycleDiagnosis` and `TopologicalSorter` in `src/graphlab/algo.py` using Kahn's algorithm with `heapq` and Tarjan's SCC analysis for cycle isolation

**Checkpoint**: Core algorithm engine implemented and unit tested.

---

## Phase 3: User Story 1 - Ordenamiento Topológico Determinista de Grafos Acíclicos (Priority: P1)

- [ ] T018 [P] [US1] Add oracle tests in `tests/test_oracle.py` verifying that `TopologicalSorter.sort()` on `small-dag.csv` and `cs-curriculum.csv` produces valid topological orders verified by `networkx`
- [ ] T019 [US1] Export `TopologicalSorter`, `CycleDiagnosis`, and `CycleDetectedError` in `src/graphlab/__init__.py`

---

## Phase 4: User Story 2 - Diagnóstico Preciso de Ciclos y Vértices Bloqueados (Priority: P1)

- [ ] T020 [P] [US2] Write tests in `tests/test_algo.py` and `tests/test_cli.py` confirming `build-with-cycle.csv` raises `CycleDetectedError`, reports `metrics -> metrics` and `auth -> session -> user-profile -> auth` as cycles, and `api`, `web` as blocked

---

## Phase 5: User Story 3 - Integración Fluida en la Interfaz CLI (Priority: P2)

- [ ] T021 [P] [US3] Add CLI integration tests in `tests/test_cli.py` for `--sort` option across all three reference CSVs and error exits
- [ ] T022 [US3] Update `src/graphlab/cli.py` to support `--sort`, emitting `Topological Order:` on stdout and structured cycle diagnostics to stderr

---

## Phase 6: Polish & Verification

- [ ] T023 [P] Execute CLI manually against `data/small-dag.csv`, `data/cs-curriculum.csv`, and `data/build-with-cycle.csv` verifying against `quickstart.md`
- [ ] T024 Run full test suite with `pytest` ensuring 100% test pass rate

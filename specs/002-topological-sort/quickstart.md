# Quickstart: Topological Sorting and Cycle Diagnosis

**Feature Branch**: `002-topological-sort`
**Date**: 2026-10-31

## 1. Running Topological Sorting on Valid DAGs

### Small DAG
```bash
py -m graphlab data/small-dag.csv --sort
```
Expected output:
- Returns exit code 0.
- Prints `Topological Order:` with garments in valid precedence order (e.g. `undershorts` before `pants`, `pants` before `shoes`).

### CS Curriculum
```bash
py -m graphlab data/cs-curriculum.csv --sort
```
Expected output:
- Returns exit code 0.
- Prints `Topological Order:` with 19 courses correctly sequenced according to prerequisites.

## 2. Running Topological Sorting on Cyclic Graph

### Build with Cycle
```bash
py -m graphlab data/build-with-cycle.csv --sort
```
Expected output:
- Returns exit code 1.
- In `stderr`:
  - Identifies cycles: `metrics -> metrics` and `auth -> session -> user-profile -> auth`.
  - Identifies blocked vertices: `api`, `web`.

# Quickstart: Directed Graph Loading and Inspection

**Feature Branch**: `001-directed-graphs`
**Date**: 2026-10-30

This guide validates the Feature 1 implementation end-to-end.

## 1. Prerequisites
- Python 3.11+ installed.
- (Optional for test execution): `pytest` and `networkx`.

## 2. Running the CLI on Sample Datasets

### A. Small DAG (`data/small-dag.csv`)
```bash
py -m graphlab.cli data/small-dag.csv
```
Expected output:
- Vertices count: `9`
- Edges count: `9`
- Isolated vertex `watch` is listed under Vertices.

### B. CS Curriculum (`data/cs-curriculum.csv`)
```bash
py -m graphlab.cli data/cs-curriculum.csv
```
Expected output:
- Vertices count: `19`
- Edges count: `23`
- Duplicate edge `Data Structures -> Algorithms` is deduplicated and appears once.

### C. Build with Cycle (`data/build-with-cycle.csv`)
```bash
py -m graphlab.cli data/build-with-cycle.csv
```
Expected output:
- Vertices count: `11`
- Edges count: `13`
- Self-loop `metrics -> metrics` is listed under Edges.

## 3. Running Automated Tests

```bash
py -m pytest tests/ -v
```
All unit tests and acceptance tests must pass with 100% success.

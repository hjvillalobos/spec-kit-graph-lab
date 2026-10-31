# CLI Contract: Topological Sorting and Cycle Diagnosis

**Feature Branch**: `002-topological-sort`
**Date**: 2026-10-31

## Invocation

```bash
python -m graphlab <path_to_csv> [--sort]
# or
py -m graphlab <path_to_csv> [--sort]
```

### Options
- `<path_to_csv>`: Positional path to the CSV file.
- `--sort`: Flag requesting topological sort instead of graph inspection.

## Exit Codes

| Exit Code | Meaning | Condition |
| :---: | :--- | :--- |
| `0` | Success | DAG sorted successfully, or graph inspected without `--sort` |
| `1` | Cycle / Validation Error | Graph contains cycles when `--sort` is requested, or CSV data is malformed |
| `2` | File / Invocation Error | File not found, permission denied, or missing CSV argument |

## Standard Output Protocol (`stdout` with `--sort`)

```text
Topological Order:
  <vertex_1>
  <vertex_2>
  ...
```

## Standard Error Protocol (`stderr` with `--sort` on cyclic graph)

```text
Error: Graph contains cycle(s). Topological ordering is not possible.
Cycles detected:
  - <v1> -> <v2> -> ... -> <v1>
Blocked vertices (not in cycle):
  - <b1>
  - <b2>
```

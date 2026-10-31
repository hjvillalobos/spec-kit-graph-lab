# CLI Contract: Directed Graph Loading and Inspection

**Feature Branch**: `001-directed-graphs`
**Date**: 2026-10-30

## Invocation

The CLI is invoked via Python standard module execution:

```bash
python -m graphlab.cli <path_to_csv>
# or
py -m graphlab.cli <path_to_csv>
```

### Positional Arguments
- `<path_to_csv>`: Path to the dependency graph CSV file to load and display.

## Exit Codes

| Exit Code | Meaning | Example Condition |
| :---: | :--- | :--- |
| `0` | Success | Valid CSV processed and printed to `stdout` |
| `1` | Validation / Data Error | Empty file, invalid header, row missing source (`,target`), invalid column count |
| `2` | File / Invocation Error | File not found, permission denied, missing `<path_to_csv>` argument |

## Standard Output Protocol (`stdout`)

On exit code `0`, `stdout` emits the combined, lexicographically sorted summary and listing:

```text
Vertices: <vertex_count>
Edges: <edge_count>

Vertices:
  <vertex_1>
  <vertex_2>
  ...

Edges:
  <source_1> -> <target_1>
  <source_2> -> <target_2>
  ...
```

If the graph has 0 vertices or 0 edges, the corresponding section remains cleanly formatted with 0 entries under its header.

## Standard Error Protocol (`stderr`)

On exit codes `1` and `2`, `stderr` emits a clean, single-line or multi-line error explanation without raw Python tracebacks:

```text
Error: [Description of validation or file access problem]
```

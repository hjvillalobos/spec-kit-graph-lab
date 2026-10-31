"""Command Line Interface for GraphLab."""

import sys
from typing import List, Optional
from graphlab.core import DirectedGraph
from graphlab.loader import CSVLoader
from graphlab.algo import TopologicalSorter
from graphlab.errors import (
    GraphLabError,
    FileAccessError,
    DataValidationError,
    CycleDetectedError,
)


def format_graph_output(graph: DirectedGraph) -> str:
    """Format the graph vertices and edges into a deterministic, human-readable string."""
    lines: List[str] = [
        f"Vertices: {graph.vertex_count()}",
        f"Edges: {graph.edge_count()}",
        "",
        "Vertices:",
    ]
    for vertex in graph.get_vertices():
        lines.append(f"  {vertex}")

    lines.append("")
    lines.append("Edges:")
    for src, dst in graph.get_edges():
        lines.append(f"  {src} -> {dst}")

    return "\n".join(lines)


def format_topological_output(order: List[str]) -> str:
    """Format the topological ordering of vertices for stdout."""
    lines: List[str] = ["Topological Order:"]
    for vertex in order:
        lines.append(f"  {vertex}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entrypoint function. Returns process exit code."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        sys.stderr.write("Error: Missing CSV file path argument.\n")
        sys.stderr.write("Usage: python -m graphlab <path_to_csv> [--sort]\n")
        return 2

    # Parse arguments
    sort_requested = False
    csv_paths: List[str] = []

    for arg in argv:
        if arg == "--sort":
            sort_requested = True
        elif arg.startswith("-"):
            sys.stderr.write(f"Error: Unknown option '{arg}'.\n")
            return 2
        else:
            csv_paths.append(arg)

    if not csv_paths:
        sys.stderr.write("Error: Missing CSV file path argument.\n")
        return 2

    if len(csv_paths) > 1:
        sys.stderr.write("Error: Only one CSV file path may be provided.\n")
        return 2

    csv_path = csv_paths[0]

    try:
        graph = CSVLoader.load_from_path(csv_path)

        if sort_requested:
            order = TopologicalSorter.sort(graph)
            output = format_topological_output(order)
            sys.stdout.write(output + "\n")
        else:
            output = format_graph_output(graph)
            sys.stdout.write(output + "\n")

        return 0
    except FileAccessError as e:
        sys.stderr.write(f"Error: {e}\n")
        return 2
    except CycleDetectedError as e:
        sys.stderr.write(f"{e}\n")
        return 1
    except DataValidationError as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1
    except GraphLabError as e:
        sys.stderr.write(f"Error: {e}\n")
        return e.exit_code
    except Exception as e:
        sys.stderr.write(f"Unexpected error: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

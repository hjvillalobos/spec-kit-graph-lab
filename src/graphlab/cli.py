"""Command Line Interface for GraphLab."""

import sys
from typing import List, Optional
from graphlab.core import DirectedGraph
from graphlab.loader import CSVLoader
from graphlab.errors import GraphLabError, FileAccessError, DataValidationError


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


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entrypoint function. Returns process exit code."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        sys.stderr.write("Error: Missing CSV file path argument.\n")
        sys.stderr.write("Usage: python -m graphlab <path_to_csv>\n")
        return 2

    csv_path = argv[0]

    try:
        graph = CSVLoader.load_from_path(csv_path)
        output = format_graph_output(graph)
        sys.stdout.write(output + "\n")
        return 0
    except FileAccessError as e:
        sys.stderr.write(f"Error: {e}\n")
        return 2
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

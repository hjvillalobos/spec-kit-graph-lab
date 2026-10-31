"""CSV loader and validator for GraphLab."""

import csv
from pathlib import Path
from typing import Union
from graphlab.core import DirectedGraph
from graphlab.errors import DataValidationError, FileAccessError


class CSVLoader:
    """Parses and validates CSV dependency files into DirectedGraph instances."""

    @classmethod
    def load_from_path(cls, file_path: Union[str, Path]) -> DirectedGraph:
        """Load and return a DirectedGraph from a CSV file path.

        Raises FileAccessError if the file does not exist or cannot be read.
        Raises DataValidationError if header or rows are malformed.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileAccessError(f"File not found: '{path}'")

        try:
            with open(path, mode="r", encoding="utf-8-sig") as f:
                content = f.read()
        except OSError as e:
            raise FileAccessError(f"Could not read file '{path}': {e}") from e

        if not content.strip():
            raise DataValidationError(f"File '{path}' is empty.")

        graph = DirectedGraph()
        reader = csv.reader(content.splitlines())

        # Validate header
        header_found = False
        line_num = 0
        for row in reader:
            line_num += 1
            if not row or not any(field.strip() for field in row):
                continue

            if len(row) != 2:
                raise DataValidationError(
                    f"Line {line_num}: Header must have exactly 2 columns ('source,target')."
                )

            col1 = row[0].strip().lstrip("\ufeff").lower()
            col2 = row[1].strip().lower()
            if col1 != "source" or col2 != "target":
                raise DataValidationError(
                    f"Line {line_num}: Invalid CSV header. Expected 'source,target', got '{row[0]},{row[1]}'."
                )
            header_found = True
            break

        if not header_found:
            raise DataValidationError(f"File '{path}' does not contain a valid CSV header.")

        # Process data rows
        for row in reader:
            line_num += 1
            if not row or not any(field.strip() for field in row):
                continue

            if len(row) != 2:
                raise DataValidationError(
                    f"Line {line_num}: Expected 2 columns, got {len(row)}."
                )

            source = row[0].strip().lstrip("\ufeff")
            target = row[1].strip()

            if not source and target:
                raise DataValidationError(
                    f"Line {line_num}: Malformed row with missing source vertex (', {target}')."
                )

            if source and not target:
                # Isolated vertex declaration
                graph.add_vertex(source)
            elif source and target:
                # Directed edge
                graph.add_edge(source, target)

        return graph

"""GraphLab: Dependency graph modeling and topological analysis toolkit.

Built without external graph libraries in production.
"""

from graphlab.core import DirectedGraph
from graphlab.loader import CSVLoader
from graphlab.errors import GraphLabError, DataValidationError, FileAccessError

__all__ = [
    "DirectedGraph",
    "CSVLoader",
    "GraphLabError",
    "DataValidationError",
    "FileAccessError",
]
__version__ = "0.1.0"

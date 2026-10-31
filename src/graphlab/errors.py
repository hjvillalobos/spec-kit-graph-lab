"""Domain exception hierarchy for GraphLab."""

from typing import Any, Optional


class GraphLabError(Exception):
    """Base exception for all GraphLab domain errors."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code

    def __str__(self) -> str:
        return self.message


class DataValidationError(GraphLabError):
    """Raised when CSV structure, headers, or rows violate data constraints."""

    def __init__(self, message: str) -> None:
        super().__init__(message, exit_code=1)


class FileAccessError(GraphLabError):
    """Raised when an input file cannot be accessed or does not exist."""

    def __init__(self, message: str) -> None:
        super().__init__(message, exit_code=2)


class CycleDetectedError(GraphLabError):
    """Raised when topological sorting cannot be computed due to cycles."""

    def __init__(self, message: str, diagnosis: Optional[Any] = None) -> None:
        super().__init__(message, exit_code=1)
        self.diagnosis = diagnosis

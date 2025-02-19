"""
Common types used across the library.
"""

from typing import TypedDict


class ArrayCoordinate(TypedDict):
    """
    A single coordinate.
    """

    x: int
    y: int
    z: int

"""
Common types used across the library.
"""

from math import floor
from typing import Self

import SimpleITK as sitk
from pydantic import BaseModel


class PhysicalCoordinate(BaseModel):
    """
    A single coordinate in physical space.
    """

    x: float
    y: float
    z: float

    def to_array_coordinate(self, *, voxel_size: float) -> "ArrayCoordinate":
        """
        Given a voxel size, convert this physical coordinate to an array coordinate.
        """
        return ArrayCoordinate(
            x=floor(self.x / voxel_size),
            y=floor(self.y / voxel_size),
            z=floor(self.z / voxel_size),
        )

    def transform(self, t: sitk.Transform) -> Self:
        """
        Transform this coordinate.

        Notes
        -----
        The transform is applied in zyx order.

        """
        new_coord = t.TransformPoint((self.z, self.y, self.x))  # type: ignore[no-untyped-call]
        return self.__class__(z=new_coord[0], y=new_coord[1], x=new_coord[2])


class ArrayCoordinate(BaseModel):
    """
    A single coordinate in array space.
    """

    x: int
    y: int
    z: int

    def to_physical_coordinate(self, *, voxel_size: float) -> "PhysicalCoordinate":
        """
        Given a voxel size, convert this array coordinate to a physical coordinate.
        """
        return PhysicalCoordinate(
            x=self.x * voxel_size, y=self.y * voxel_size, z=self.z * voxel_size
        )

"""
Tools for working with volumes of interest (VOIs).

A volume of interest is a sub-volume contained within a full dataset.
It is represented by the [`VOI`][hoa_tools.voi.VOI] class.

All coordinates are given in 'array coordinates',
where 0 is the centre of the first voxel, 1 is the centre of the second voxel etc.
"""

import itertools
from math import ceil, floor
from typing import Literal

import xarray as xr
from pydantic import BaseModel

from hoa_tools.dataset import Dataset
from hoa_tools.registration import Inventory as RegInventory
from hoa_tools.types import ArrayCoordinate


class VOI(BaseModel):
    """
    A volume of interest attached to a given dataset.
    """

    dataset: Dataset
    """Dataset that this VOI is in."""
    downsample_level: Literal[0, 1, 2, 3, 4]
    """Downsampling level of the dataset that this VOI is defined in."""
    lower_corner: ArrayCoordinate
    """Index of lower corner in array coordinates."""
    size: ArrayCoordinate
    """Size of VOI in array coordinates."""

    @property
    def upper_corner(self) -> ArrayCoordinate:
        """
        Upper corner of the VOI.
        """
        return ArrayCoordinate(
            x=self.lower_corner.x + self.size.x,
            y=self.lower_corner.y + self.size.y,
            z=self.lower_corner.z + self.size.z,
        )

    @property
    def corners(self) -> list[ArrayCoordinate]:
        """
        All 8 corners of the VOI.
        """
        corner_tuples: list[tuple[int, int, int]] = list(
            itertools.product(  # type: ignore[arg-type]
                *zip(
                    [self.lower_corner.x, self.lower_corner.y, self.lower_corner.z],
                    [self.upper_corner.x, self.upper_corner.y, self.upper_corner.z],
                )
            )
        )
        return [ArrayCoordinate(x=i[0], y=i[1], z=i[2]) for i in corner_tuples]

    def get_data_array(self) -> xr.DataArray:
        """
        Get data array for this VOI.
        """
        da = self.dataset.data_array(downsample_level=self.downsample_level)
        return da.isel(
            x=slice(self.lower_corner.x, self.upper_corner.x),
            y=slice(self.lower_corner.y, self.upper_corner.y),
            z=slice(self.lower_corner.z, self.upper_corner.z),
        )

    def change_downsample_level(
        self, *, new_downsample_level: Literal[0, 1, 2, 3, 4]
    ) -> "VOI":
        """
        Return a new VOI at a different downsample level.
        """
        resolution_ratio = (2**self.downsample_level) / (2**new_downsample_level)
        new_lower_corner = ArrayCoordinate(
            x=floor(self.lower_corner.x * resolution_ratio),
            y=floor(self.lower_corner.y * resolution_ratio),
            z=floor(self.lower_corner.z * resolution_ratio),
        )
        new_size = ArrayCoordinate(
            x=ceil(self.size.x * resolution_ratio),
            y=ceil(self.size.y * resolution_ratio),
            z=ceil(self.size.z * resolution_ratio),
        )
        return VOI(
            dataset=self.dataset,
            downsample_level=new_downsample_level,
            lower_corner=new_lower_corner,
            size=new_size,
        )

    def transform_to(self, dataset: Dataset) -> "VOI":
        """
        Transform this VOI to another dataset.

        The new VOI will completely contain the transformed original VOI.
        """
        if (self.dataset, dataset) not in RegInventory:
            msg = (
                f"Transform between {self.dataset.name} and {dataset.name} not found "
                "in registration inventory."
            )
            raise RuntimeError(msg)

        old_voi = self.change_downsample_level(new_downsample_level=0)
        transform = RegInventory.get_registration(
            source_datset=self.dataset, target_dataset=dataset
        )

        # Convert to physical space
        physical_corners = [
            c.to_physical_coordinate(voxel_size=self.dataset.data.voxel_size_um)
            for c in old_voi.corners
        ]
        # Transform
        physical_corners_transformed = [
            c.transform(transform) for c in physical_corners
        ]
        # Convert back to array space
        corners_transformed = [
            c.to_array_coordinate(voxel_size=dataset.data.voxel_size_um)
            for c in physical_corners_transformed
        ]
        lower_corner = ArrayCoordinate(
            z=min([c.z for c in corners_transformed]),
            y=min([c.y for c in corners_transformed]),
            x=min([c.x for c in corners_transformed]),
        )
        upper_corner = ArrayCoordinate(
            z=max([c.z for c in corners_transformed]) + 1,
            y=max([c.y for c in corners_transformed]) + 1,
            x=max([c.x for c in corners_transformed]) + 1,
        )
        return VOI(
            dataset=dataset,
            downsample_level=0,
            lower_corner=lower_corner,
            size=ArrayCoordinate(
                x=upper_corner.x - lower_corner.x,
                y=upper_corner.y - lower_corner.y,
                z=upper_corner.z - lower_corner.z,
            ),
        )

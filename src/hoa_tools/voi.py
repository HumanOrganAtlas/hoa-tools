"""
Tools for working with volumes of interest (VOIs).

A volume of interest is a sub-volume contained within a full dataset.
It is represented by the [`VOI`][hoa_tools.voi.VOI] class.
"""

import itertools
from math import ceil, floor
from typing import Literal

import numpy as np
import xarray as xr
from pydantic import BaseModel

from hoa_tools.dataset import Dataset
from hoa_tools.registration import Inventory as RegInventory
from hoa_tools.types import Coordinate


class VOI(BaseModel):
    """
    A volume of interest attached to a given dataset.
    """

    dataset: Dataset
    """Dataset that this VOI is in."""
    downsample_level: Literal[0, 1, 2, 3, 4]
    """Downsampling level of the dataset that this VOI is defined in."""
    lower_corner: Coordinate
    """Index of lower corner in array coordinates."""
    size: Coordinate
    """Size of VOI in array coordinates."""

    @property
    def upper_corner(self) -> Coordinate:
        """
        Upper corner of the VOI.
        """
        return {
            "x": self.lower_corner["x"] + self.size["x"],
            "y": self.lower_corner["y"] + self.size["y"],
            "z": self.lower_corner["z"] + self.size["z"],
        }

    @property
    def corners(self) -> list[Coordinate]:
        """
        All 8 corners of the VOI.
        """
        corner_tuples: list[tuple[int, int, int]] = list(
            itertools.product(  # type: ignore[arg-type]
                *zip(self.lower_corner.values(), self.upper_corner.values())
            )
        )
        return [{"x": i[0], "y": i[1], "z": i[2]} for i in corner_tuples]

    def get_data_array(self) -> xr.DataArray:
        """
        Get data array for this VOI.
        """
        da = self.dataset.data_array(downsample_level=self.downsample_level)
        return da.isel(
            x=slice(self.lower_corner["x"], self.upper_corner["x"]),
            y=slice(self.lower_corner["y"], self.upper_corner["y"]),
            z=slice(self.lower_corner["z"], self.upper_corner["z"]),
        )

    def change_downsample_level(
        self, *, new_downsample_level: Literal[0, 1, 2, 3, 4]
    ) -> "VOI":
        """
        Return a new VOI at a different downsample level.
        """
        resolution_ratio = (2**self.downsample_level) / (2**new_downsample_level)
        new_lower_corner = {
            k: floor(v * resolution_ratio)  # type: ignore[operator]
            for k, v in self.lower_corner.items()
        }
        new_size = {k: ceil(v * resolution_ratio) for k, v in self.size.items()}  # type: ignore[operator]
        return VOI(
            dataset=self.dataset,
            downsample_level=new_downsample_level,
            lower_corner=new_lower_corner,  # type: ignore[arg-type]
            size=new_size,  # type: ignore[arg-type]
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

        # Using zyx order from here
        corners_transformed = np.array(
            [
                transform.TransformPoint((corner["z"], corner["y"], corner["x"]))  # type: ignore[no-untyped-call]
                for corner in old_voi.corners
            ]
        )
        lower_corner = (
            np.floor(np.min(corners_transformed, axis=0)).astype(int).tolist()
        )
        upper_corner = np.ceil(np.max(corners_transformed, axis=0)).astype(int).tolist()
        # Converting back from zyx order here
        return VOI(
            dataset=dataset,
            downsample_level=0,
            lower_corner={
                "x": lower_corner[2],
                "y": lower_corner[1],
                "z": lower_corner[0],
            },
            size={
                "x": upper_corner[2] - lower_corner[2],
                "y": upper_corner[1] - lower_corner[1],
                "z": upper_corner[0] - lower_corner[0],
            },
        )

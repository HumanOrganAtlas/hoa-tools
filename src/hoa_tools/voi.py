from dataclasses import dataclass
from math import ceil, floor
from typing import Literal, TypedDict

import xarray as xr

from hoa_tools.dataset import Dataset


class Coordinate(TypedDict):
    """
    A single coordinate.
    """

    x: int
    y: int
    z: int


@dataclass(kw_only=True)
class VOI:
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

    def get_data_array(self) -> xr.DataArray:
        """
        Get data array for this VOI.
        """
        da = self.dataset.data_array(downsample_level=self.downsample_level)
        return da.sel(
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

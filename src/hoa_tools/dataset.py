"""
Tools for working with individual datasets.
"""

from functools import cached_property
from typing import Literal

import gcsfs
import pydantic
import unyt.array
import zarr.core
import zarr.n5

import hoa_tools.inventory
import hoa_tools.types

_BUCKET = "ucl-hip-ct-35a68e99feaae8932b1d44da0358940b"


@pydantic.dataclasses.dataclass(config={"arbitrary_types_allowed": True})
class Dataset:
    """
    An individual Human Organ Atlas dataset.
    """

    donor: str
    """Donor ID."""
    organ: hoa_tools.types.Organ
    """Organ name."""
    organ_context: str
    """Context for dataset within organ. Not always present."""
    roi: str
    """Region of Interest. Takes an arbitrary (and often not descriptive) value
    that is unique between scans of the same organ. Takes the special value
    'complete-organ' if the dataset is a scan of the full organ."""
    resolution: unyt.array.unyt_quantity
    """Size of a single voxel in the dataset. All datasets have isotropic voxels."""
    beamline: hoa_tools.types.Beamline
    """ESRF beamline ID."""
    nx: int
    """Number of voxels along the x-axis."""
    ny: int
    """Number of voxels along the y-axis."""
    nz: int
    """Number of voxels along the z-axis."""

    def _organ_str(self) -> str:
        """
        Get name of organ, with organ context appended if present.
        """
        organ_str = str(self.organ)
        if self.organ_context:
            organ_str += "_" + self.organ_context
        return organ_str

    def _resolution_str(self) -> str:
        # Make sure that resolution includes a .0 if an integer value.
        return str(float(self.resolution.to_value("um")))

    @property
    def name(self) -> str:
        """
        Unique name for dataset.
        """
        return (
            f"{self.donor}_{self._organ_str()}_{self.roi}_"
            f"{self._resolution_str()}um_{self.beamline}"
        )

    @property
    def is_full_organ(self) -> bool:
        """
        Whether this dataset contains the whole organ or not.
        """
        return self.roi.startswith("complete")

    def get_children(self) -> list["Dataset"]:
        """
        Get child dataset(s).

        Child datasets are high-resolution zooms of a full-organ dataset.

        Notes
        -----
        For full-organ datasets, this returns an empty list.

        """
        inventory = hoa_tools.inventory.load_inventory()
        # Filter on successive attributes
        inventory = inventory.loc[inventory["donor"] == self.donor]
        inventory = inventory.loc[inventory["organ"] == self.organ]
        inventory = inventory.loc[
            inventory["beamline"] == int(self.beamline.strip("bm"))
        ]
        # Only want non-full-organ datasets
        inventory = inventory.loc[inventory["roi"] != "complete-organ"]

        return [get_dataset(name) for name in inventory.index]

    def get_parents(self) -> list["Dataset"]:
        """
        Get parent dataset(s).

        Parent datasets are full-organ datasets from which a ROI dataset is taken from.

        Notes
        -----
        For ROI datasets, this returns an empty list.

        """
        inventory = hoa_tools.inventory.load_inventory()
        # Filter on successive attributes
        inventory = inventory.loc[inventory["donor"] == self.donor]
        inventory = inventory.loc[inventory["organ"] == self.organ]
        inventory = inventory.loc[
            inventory["beamline"] == int(self.beamline.strip("bm"))
        ]
        # Only want full-organ datasets
        inventory = inventory.loc[inventory["roi"] == "complete-organ"]

        return [get_dataset(name) for name in inventory.index]

    @cached_property
    def _remote_store(self) -> zarr.Group:
        """
        Remote data store.
        """
        path = f"/{self.donor}/{self.organ}"
        if self.organ_context:
            path += f"-{self.organ_context}"
        path += f"/{self.resolution.to_value('um')}um_{self.roi}_{self.beamline}"

        fs = gcsfs.GCSFileSystem(project=_BUCKET, token="anon", access="read_only")  # noqa: S106
        store = zarr.n5.N5FSStore(url=_BUCKET, fs=fs, mode="r")
        return zarr.open_group(store, mode="r", path=path)

    def remote_array(self, *, level: Literal[0, 1, 2, 3, 4]) -> zarr.core.Array:
        """
        Get an object representing the data array in the remote Google Cloud Store.
        """
        if level not in (levels := [0, 1, 2, 3, 4]):
            msg = f"'level' must be in {levels}"
            raise ValueError(msg)

        return self._remote_store[f"s{level}"]


def get_dataset(name: str) -> Dataset:
    """
    Get a dataset from its name.

    The name of datasets can be looked up using the `hoa_tools.inventory` module.
    """
    inventory = hoa_tools.inventory.load_inventory()
    dataset_row = inventory.loc[name]
    attributes = {
        attr: dataset_row[attr]
        for attr in [
            "donor",
            "organ",
            "organ_context",
            "roi",
            "resolution_um",
            "beamline",
            "nx",
            "ny",
            "nz",
        ]
    }
    attributes["resolution"] = attributes.pop("resolution_um") * unyt.um
    attributes["beamline"] = "bm" + str(attributes["beamline"]).zfill(2)
    return Dataset(**attributes)

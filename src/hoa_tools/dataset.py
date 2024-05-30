"""
Tools for working with individual datasets.
"""

import pydantic
import unyt

import hoa_tools.inventory
import hoa_tools.types


@pydantic.dataclasses.dataclass(config={"arbitrary_types_allowed": True})
class Dataset:
    """
    An individual Human Organ Atlas dataset.
    """

    donor: str
    """Donor ID."""
    organ: hoa_tools.types.Organ
    """Organ name."""
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

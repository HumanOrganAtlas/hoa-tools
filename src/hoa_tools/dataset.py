"""
Tools for working with individual datasets.
"""

from dataclasses import dataclass

import hoa_tools.inventory
import hoa_tools.types


@dataclass
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
    'full-organ' if the dataset is a scan of the full organ."""
    resolution: float
    """Size of a single voxel in the dataset. All datasets have isotropic voxels."""
    beamline: hoa_tools.types.Beamline
    """ESRF beamline ID."""
    nx: int
    """Number of voxels along the x-axis."""
    ny: int
    """Number of voxels along the y-axis."""
    nz: int
    """Number of voxels along the z-axis."""


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
    attributes["resolution"] = attributes.pop("resolution_um")
    return Dataset(**attributes)

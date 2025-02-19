"""
Tools for working with the dataset inventory.
"""

import pandas as pd

from hoa_tools.dataset import _DATASETS


def load_inventory() -> pd.DataFrame:
    """
    Load the dataset inventory.

    Returns
    -------
    inventory :
        Dataset inventory.

    """
    data = [
        {
            "donor": d.donor.id,
            "organ": d.sample.organ,
            "organ_context": d.sample.organ_context,
            "voi": d.voi,
            "voxel_size_um": d.data.voxel_size_um,
        }
        for d in _DATASETS.values()
    ]
    return pd.DataFrame(data=data, index=list(_DATASETS.keys()))

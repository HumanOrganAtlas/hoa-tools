"""
Tools for working with the Human Organ Atlas Inventory.
"""

from pathlib import Path

import pandas as pd


def load_inventory() -> pd.DataFrame:
    """
    Load the public HiP-CT inventory.

    Returns
    -------
    inventory :
        Inventory as a pandas DataFrame.

    """
    inventory_file = Path(__file__).parent / "data" / "hoa_inventory.csv"
    return pd.read_csv(
        inventory_file,
        index_col="name",
        keep_default_na=False,
    )

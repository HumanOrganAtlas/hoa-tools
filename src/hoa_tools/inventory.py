"""
Tools for working with the Human Organ Atlas Inventory.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = inventory_file = Path(__file__).parent / "data"


def load_inventory() -> pd.DataFrame:
    """
    Load the public Human Organ Atlas inventory.

    Returns
    -------
    inventory :
        Inventory as a pandas DataFrame.

    """
    inventory_file = DATA_DIR / "hoa_inventory.csv"
    return pd.read_csv(
        inventory_file,
        index_col="name",
        dtype={"organ_context": str},
        keep_default_na=False,
    )

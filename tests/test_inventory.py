import pandas as pd

import hoa_tools.inventory


def test_load_inventory() -> None:
    df = hoa_tools.inventory.load_inventory()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == [
        "donor",
        "organ",
        "organ_context",
        "voi",
        "voxel_size_um",
    ]

import hoa_tools.inventory
import pandas as pd


def test_load_inventory() -> None:
    df = hoa_tools.inventory.load_inventory()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == [
        "donor",
        "organ",
        "organ_context",
        "roi",
        "resolution_um",
        "beamline",
        "nx",
        "ny",
        "nz",
        "contrast_low",
        "contrast_high",
        "size_gb_uncompressed",
    ]

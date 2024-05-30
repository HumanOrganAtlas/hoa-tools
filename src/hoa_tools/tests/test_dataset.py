from hoa_tools.dataset import Dataset, get_dataset
from unyt import unyt_quantity


def test_child_datasets() -> None:
    whole_spleen = get_dataset("LADAF-2020-27_spleen_complete-organ_25.08um_bm05")
    child_datasets = whole_spleen.get_children()
    assert len(child_datasets) == 2

    assert child_datasets == [
        Dataset(
            donor="LADAF-2020-27",
            organ="spleen",
            roi="central-column",
            resolution=unyt_quantity(1.29, "μm"),
            beamline="bm05",
            nx=3823,
            ny=3823,
            nz=10982,
        ),
        Dataset(
            donor="LADAF-2020-27",
            organ="spleen",
            roi="central-column",
            resolution=unyt_quantity(6.05, "μm"),
            beamline="bm05",
            nx=3791,
            ny=3791,
            nz=7540,
        ),
    ]

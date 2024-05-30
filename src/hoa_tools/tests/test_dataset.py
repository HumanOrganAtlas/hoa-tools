import re

import pytest
from hoa_tools.dataset import Dataset, get_dataset
from unyt import unyt_quantity


@pytest.fixture()
def dataset() -> Dataset:
    return get_dataset("LADAF-2020-27_spleen_complete-organ_25.08um_bm05")


def test_child_datasets() -> None:
    whole_spleen = get_dataset("LADAF-2020-27_spleen_complete-organ_25.08um_bm05")
    child_datasets = whole_spleen.get_children()
    assert len(child_datasets) == 2

    assert child_datasets == [
        Dataset(
            donor="LADAF-2020-27",
            organ="spleen",
            organ_context="",
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
            organ_context="",
            roi="central-column",
            resolution=unyt_quantity(6.05, "μm"),
            beamline="bm05",
            nx=3791,
            ny=3791,
            nz=7540,
        ),
    ]


@pytest.mark.vcr()
def test_remote_array(dataset: Dataset) -> None:
    remote_arr = dataset.remote_array(level=2)
    assert remote_arr.shape == (475, 730, 538)


def test_invalid_level(dataset: Dataset) -> None:
    with pytest.raises(
        ValueError, match=re.escape("'level' must be in [0, 1, 2, 3, 4]")
    ):
        dataset.remote_array(level=-1)

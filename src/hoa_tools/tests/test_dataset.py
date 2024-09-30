import re

import pytest
from unyt import unyt_quantity

from hoa_tools.dataset import Dataset, get_dataset


@pytest.fixture
def dataset() -> Dataset:
    return get_dataset("LADAF-2020-27_spleen_complete-organ_25.08um_bm05")


def test_dataset_properties() -> None:
    name = "LADAF-2020-27_spleen_complete-organ_25.08um_bm05"
    dataset = get_dataset(name)

    assert dataset.name == name
    assert dataset.is_full_organ


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


def test_parent_datasets() -> None:
    roi = get_dataset("LADAF-2020-31_kidney_lateral-transect_2.5um_bm05")
    parent_datasets = roi.get_parents()
    assert len(parent_datasets) == 1

    assert parent_datasets == [
        Dataset(
            donor="LADAF-2020-31",
            organ="kidney",
            organ_context="",
            roi="complete-organ",
            resolution=unyt_quantity(25.0, "μm"),
            beamline="bm05",
            nx=2215,
            ny=3287,
            nz=4282,
        )
    ]


@pytest.mark.vcr
def test_remote_array(dataset: Dataset) -> None:
    remote_arr = dataset.remote_array(level=2)
    assert remote_arr.shape == (475, 730, 538)


def test_invalid_level(dataset: Dataset) -> None:
    with pytest.raises(
        ValueError, match=re.escape("'level' must be in [0, 1, 2, 3, 4]")
    ):
        dataset.remote_array(level=-1)  # type: ignore[arg-type]

import re

import pytest

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
            region="central-column",
            resolution_um=1.29,
            beamline="bm05",
            nx=3823,
            ny=3823,
            nz=10982,
        ),
        Dataset(
            donor="LADAF-2020-27",
            organ="spleen",
            organ_context="",
            region="central-column",
            resolution_um=6.05,
            beamline="bm05",
            nx=3791,
            ny=3791,
            nz=7540,
        ),
    ]


def test_parent_datasets() -> None:
    zoom = get_dataset("LADAF-2020-31_kidney_lateral-transect_2.5um_bm05")
    parent_datasets = zoom.get_parents()
    assert len(parent_datasets) == 1

    assert parent_datasets == [
        Dataset(
            donor="LADAF-2020-31",
            organ="kidney",
            organ_context="",
            region="complete-organ",
            resolution_um=25,
            beamline="bm05",
            nx=2215,
            ny=3287,
            nz=4282,
        )
    ]


@pytest.mark.vcr
def test_remote_array(dataset: Dataset) -> None:
    data_array = dataset.data_array(downsample_level=2)
    assert data_array.shape == (475, 730, 538)


def test_invalid_level(dataset: Dataset) -> None:
    with pytest.raises(
        ValueError, match=re.escape("'level' must be in [0, 1, 2, 3, 4]")
    ):
        dataset.data_array(downsample_level=-1)  # type: ignore[arg-type]

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

    assert [p.name for p in child_datasets] == [
        "LADAF-2020-27_spleen_central-column_6.05um_bm05",
        "LADAF-2020-27_spleen_central-column_1.29um_bm05",
    ]


def test_parent_datasets() -> None:
    zoom = get_dataset("LADAF-2020-31_kidney_lateral-transect_2.5um_bm05")
    parent_datasets = zoom.get_parents()
    assert len(parent_datasets) == 1

    assert [p.name for p in parent_datasets] == [
        "LADAF-2020-31_kidney_complete-organ_25.0um_bm05"
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

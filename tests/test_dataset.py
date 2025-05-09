import re
from pathlib import Path

import pytest

from hoa_tools.dataset import _META_DIR, Dataset, change_metadata_directory, get_dataset


@pytest.fixture
def dataset() -> Dataset:
    return get_dataset("LADAF-2020-27_spleen_complete-organ_25.08um_bm05")


def test_dataset_properties() -> None:
    name = "LADAF-2020-27_spleen_complete-organ_25.08um_bm05"
    dataset = get_dataset(name)

    assert dataset.name == name
    assert dataset.is_full_organ
    assert (
        str(dataset) == "Dataset(name=LADAF-2020-27_spleen_complete-organ_25.08um_bm05)"
    )


def test_child_datasets() -> None:
    whole_spleen = get_dataset("LADAF-2020-27_spleen_complete-organ_25.08um_bm05")
    child_datasets = whole_spleen.get_children()
    assert len(child_datasets) == 2

    assert sorted([p.name for p in child_datasets]) == sorted(
        [
            "LADAF-2020-27_spleen_central-column_6.05um_bm05",
            "LADAF-2020-27_spleen_central-column_1.29um_bm05",
        ]
    )


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


@pytest.mark.vcr
def test_remote_array_zarr() -> None:
    dataset = get_dataset("A186_lung_right_complete-organ_24.132um_bm18")
    assert dataset._remote_fmt == "zarr"  # noqa: SLF001
    data_array = dataset.data_array(downsample_level=2)
    assert data_array.shape == (2391, 2077, 2077)


def test_invalid_level(dataset: Dataset) -> None:
    with pytest.raises(ValueError, match=re.escape("level must be >= 0")):
        dataset.data_array(downsample_level=-1)  # type: ignore[arg-type]


def test_update_datasets() -> None:
    # Not the best test - this updates the directory to the same previous one
    # But it's at least a smoke test...
    change_metadata_directory(_META_DIR)


def test_update_datasets_error(tmp_path: Path) -> None:
    with pytest.raises(
        FileNotFoundError, match="Did not find any dataset metadata files at"
    ):
        change_metadata_directory(tmp_path)

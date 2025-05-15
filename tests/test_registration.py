import pytest

import hoa_tools.dataset
import hoa_tools.registration
import hoa_tools.voi
from hoa_tools.types import ArrayCoordinate


def test_transform_voi() -> None:
    overview = hoa_tools.dataset.get_dataset(
        "S-20-29_brain_complete-organ_25.33um_bm05"
    )
    child = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-04_6.5um_bm05")

    child_voi = hoa_tools.voi.VOI(
        dataset=child,
        downsample_level=0,
        lower_corner=ArrayCoordinate(x=3434, y=2060, z=2656),
        size=ArrayCoordinate(x=256, y=256, z=128),
    )

    overview_voi = child_voi.transform_to(overview)
    assert overview_voi.dataset.name == "S-20-29_brain_complete-organ_25.33um_bm05"
    assert overview_voi.downsample_level == 0
    assert overview_voi.lower_corner == ArrayCoordinate(x=2975, y=1689, z=4316)
    assert overview_voi.size == ArrayCoordinate(x=69, y=69, z=33)


def test_inverse_registration() -> None:
    overview = hoa_tools.dataset.get_dataset(
        "S-20-29_brain_complete-organ_25.33um_bm05"
    )
    zoom = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-04_6.5um_bm05")

    transform = hoa_tools.registration.Inventory.get_registration(
        source_dataset=zoom, target_dataset=overview
    )
    transform_inv = hoa_tools.registration.Inventory.get_registration(
        source_dataset=overview, target_dataset=zoom
    )

    assert transform.GetParameters() == (
        0.020069870800809003,
        0.0,
        0.0,
        92062.68586067778,
        30372.305582420606,
        52529.27516774854,
        1.0000012996591003,
    )

    # Check transform roundtrip
    point = (0, 0, 0)
    assert transform_inv.TransformPoint(transform.TransformPoint(point)) == point


def test_transform_path() -> None:
    # Test getting transform between two datasets that aren't directly registered
    zoom1 = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-04_6.5um_bm05")
    zoom2 = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-05_6.5um_bm05")

    hoa_tools.registration.Inventory.get_registration(
        source_dataset=zoom1, target_dataset=zoom2
    )


def test_no_transform_path() -> None:
    # Test getting transform between two datasets that aren't directly registered
    d1 = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-04_6.5um_bm05")
    d2 = hoa_tools.dataset.get_dataset(
        "LADAF-2020-27_spleen_complete-organ_25.08um_bm05"
    )

    assert (d1, d2) not in hoa_tools.registration.Inventory

    with pytest.raises(
        ValueError,
        match=(
            "No registration path between S-20-29_brain_VOI-04_6.5um_bm05 and "
            "LADAF-2020-27_spleen_complete-organ_25.08um_bm05"
        ),
    ):
        hoa_tools.registration.Inventory.get_registration(
            source_dataset=d1, target_dataset=d2
        )


def test_registered() -> None:
    # Test getting transform between two datasets that aren't directly registered
    d = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-04_6.5um_bm05")
    registered = d.get_registered()
    assert {d.name for d in registered} == {
        "S-20-29_brain_complete-organ_25.33um_bm05",
        "S-20-29_brain_VOI-04_2.5um_bm05",
        "S-20-29_brain_VOI-03_6.5um_bm05",
        "S-20-29_brain_VOI-01_2.5um_bm05",
        "S-20-29_brain_VOI-03_2.5um_bm05",
        "S-20-29_brain_VOI-01b_6.5um_bm05",
        "S-20-29_brain_VOI-02_2.5um_bm05",
        "S-20-29_brain_VOI-01_6.5um_bm05",
        "S-20-29_brain_VOI-02_6.5um_bm05",
        "S-20-29_brain_VOI-05_2.5um_bm05",
        "S-20-29_brain_VOI-04_6.5um_bm05",
        "S-20-29_brain_VOI-05_6.5um_bm05",
    }


def test_transform_zoom_to_zoom() -> None:
    zoom1 = hoa_tools.dataset.get_dataset("LADAF-2021-64_heart_VOI-07_6.51um_bm18")
    zoom2 = hoa_tools.dataset.get_dataset("LADAF-2021-64_heart_VOI-7.1_2.26um_bm18")

    voi = hoa_tools.voi.VOI(
        dataset=zoom1,
        downsample_level=0,
        lower_corner={"x": 3434, "y": 2060, "z": 2656},
        size={"x": 256, "y": 256, "z": 128},
    )

    voi.transform_to(zoom2)

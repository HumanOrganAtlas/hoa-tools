import hoa_tools.dataset
import hoa_tools.registration
import hoa_tools.voi


def test_transform_voi() -> None:
    overview = hoa_tools.dataset.get_dataset(
        "S-20-29_brain_complete-organ_25.33um_bm05"
    )
    child = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-04_6.5um_bm05")

    child_voi = hoa_tools.voi.VOI(
        dataset=child,
        downsample_level=0,
        lower_corner={"x": 3434, "y": 2060, "z": 2656},
        size={"x": 256, "y": 256, "z": 128},
    )

    transform = hoa_tools.registration.build_transform(
        translation={"x": 2073.796888, "y": 1199.064571, "z": 3634.531617},
        rotation_deg=2.299992208,
        scale=0.2566130457,
    )

    hoa_tools.registration.Inventory.add_registration(
        source_dataset=child,
        target_dataset=overview,
        transform=transform,
    )

    overview_voi = child_voi.transform_to(overview)
    assert overview_voi.dataset.name == "S-20-29_brain_complete-organ_25.33um_bm05"
    assert overview_voi.downsample_level == 0
    assert overview_voi.lower_corner == {"x": 2975, "y": 1689, "z": 4316}
    assert overview_voi.size == {"x": 69, "y": 69, "z": 33}

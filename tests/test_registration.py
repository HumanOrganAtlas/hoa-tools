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

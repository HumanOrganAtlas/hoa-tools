from hoa_tools.dataset import get_dataset
from hoa_tools.voi import VOI


def test_voi_properties() -> None:
    dataset = get_dataset("LADAF-2020-27_spleen_complete-organ_25.08um_bm05")
    voi = VOI(
        dataset=dataset,
        downsample_level=2,
        lower_corner={"x": 1, "y": 2, "z": 3},
        size={"x": 30, "y": 20, "z": 10},
    )

    assert voi.voxel_size_um == 100.32

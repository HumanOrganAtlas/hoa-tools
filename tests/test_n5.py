from pathlib import Path

import numpy as np
import zarr

from hoa_tools._n5 import N5FSStore


def test_n5_fsstore(tmp_path: Path) -> None:
    """
    Roundtrip test for N5 fsstore.
    """
    store = N5FSStore(url=tmp_path)
    array = zarr.zeros(shape=(2, 3), dtype="uint8", store=store)
    array[:] = np.arange(6).reshape(2, 3)

    np.testing.assert_equal(array[:], np.arange(6).reshape(2, 3))

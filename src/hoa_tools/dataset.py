"""
Tools for working with individual datasets.
"""

from functools import cached_property
from pathlib import Path
from typing import Literal

import dask.array.core
import gcsfs
import numpy as np
import xarray as xr
import zarr.core
import zarr.n5

from hoa_tools._hoa_model import HOAMetadata
from hoa_tools._n5 import N5FSStore

__all__ = ["Dataset", "get_dataset"]


class Dataset(HOAMetadata):
    """
    An individual Human Organ Atlas dataset.
    """

    def _organ_str(self) -> str:
        """
        Get name of organ, with organ context appended if present.
        """
        organ_str = str(self.sample.organ)
        if self.sample.organ_context:
            organ_str += "_" + self.sample.organ_context
        return organ_str

    def _voxel_size_str(self) -> str:
        # Make sure that voxel size includes a .0 if an integer value.
        return str(float(self.data.voxel_size_um))

    @property
    def is_full_organ(self) -> bool:
        """
        Whether this dataset contains the whole organ or not.
        """
        return self.voi.startswith("complete")

    @property
    def is_zoom(self) -> bool:
        """
        Whether this dataset is a zoom or not.
        """
        return not self.is_full_organ

    def get_children(self) -> list["Dataset"]:
        """
        Get child dataset(s).

        Child datasets are high-resolution zooms of a full-organ dataset.

        Notes
        -----
        For full-organ datasets, this returns an empty list.

        """
        return [
            d
            for d in _DATASETS.values()
            if (
                d.donor.id == self.donor.id
                and d.sample.organ == self.sample.organ
                and d.scan.beamline == self.scan.beamline
                and d.is_zoom
            )
        ]

    def get_parents(self) -> list["Dataset"]:
        """
        Get parent dataset(s).

        Parent datasets are full-organ datasets from which a zoom dataset is taken from.

        Notes
        -----
        For zoom datasets, this returns an empty list.

        """
        return [
            d
            for d in _DATASETS.values()
            if (
                d.donor.id == self.donor.id
                and d.sample.organ == self.sample.organ
                and d.scan.beamline == self.scan.beamline
                and d.is_full_organ
            )
        ]

    @cached_property
    def _remote_store(self) -> zarr.Group:
        """
        Remote data store.
        """
        gcs_url = self.data.gcs_url
        if not gcs_url.startswith("n5://"):
            raise RuntimeError("Only N5 supported")

        gcs_url = gcs_url.removeprefix("n5://gs://")
        # n5://gs://ucl-hip-ct-35a68e99feaae8932b1d44da0358940b/S-20-29/heart/2.5um_VOI-01_bm05/
        bucket, path = gcs_url.split("/", maxsplit=1)

        fs = gcsfs.GCSFileSystem(project=bucket, token="anon", access="read_only")  # noqa: S106
        store = N5FSStore(url=bucket, fs=fs, mode="r")
        return zarr.open_group(store, mode="r", path=path)

    def _remote_array(
        self, *, downsample_level: Literal[0, 1, 2, 3, 4]
    ) -> zarr.core.Array:
        """
        Get an object representing the data array in the remote Google Cloud Store.
        """
        if downsample_level not in (levels := [0, 1, 2, 3, 4]):
            msg = f"'level' must be in {levels}"
            raise ValueError(msg)

        return self._remote_store[f"s{downsample_level}"]

    def data_array(self, *, downsample_level: Literal[0, 1, 2, 3, 4]) -> xr.DataArray:
        """
        Get a DataArray representing the array for this image.
        """
        remote_array = self._remote_array(downsample_level=downsample_level)
        dask_array = dask.array.core.from_array(  # type: ignore[no-untyped-call]
            remote_array, chunks=remote_array.chunks
        )
        spacing = self.data.voxel_size_um * 2**downsample_level
        return xr.DataArray(
            dask_array,
            name=self.name,
            dims=["z", "y", "x"],
            coords={
                "z": xr.DataArray(
                    data=(np.arange(dask_array.shape[0]) * spacing),
                    dims=["z"],
                    attrs={"units": "μm"},
                ),
                "y": xr.DataArray(
                    data=(np.arange(dask_array.shape[1]) * spacing),
                    dims=["y"],
                    attrs={"units": "μm"},
                ),
                "x": xr.DataArray(
                    data=(np.arange(dask_array.shape[2]) * spacing),
                    dims=["x"],
                    attrs={"units": "μm"},
                ),
            },
        )


_DATA_DIR = inventory_file = Path(__file__).parent / "data"
_DATASETS = {
    f.stem: Dataset.model_validate_json(f.read_text())
    for f in (_DATA_DIR / "metadata" / "metadata").glob("*.json")
}
if len(_DATASETS) == 0:
    raise ImportError(
        "Did not find any dataset metadata files. "
        "This means there is something wrong with the hoa-tools installation. "
        "If you are installing from source, you might need to "
        "initialise and fetch git submodules. "
    )


def get_dataset(name: str) -> Dataset:
    """
    Get a dataset from its name.

    The name of datasets can be looked up using the `hoa_tools.inventory` module.
    """
    return _DATASETS[name]

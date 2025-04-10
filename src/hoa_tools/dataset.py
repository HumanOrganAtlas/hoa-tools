"""
Tools for working with individual datasets.

The core class representing a single dataset is [`Dataset`][hoa_tools.dataset.Dataset].
This inherits from [`HOAMetadata`][hoa_tools.metadata.HOAMetadata],
which stores all the metadata for a given dataset.

[`Dataset`][hoa_tools.dataset.Dataset] objects are not designed to be created by users.
To get a [`Dataset`][hoa_tools.dataset.Dataset], use the
[`get_dataset`][hoa_tools.dataset.get_dataset] function in this module.
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
import zarr.storage

from hoa_tools._n5 import N5FSStore
from hoa_tools.metadata import HOAMetadata

__all__ = ["Dataset", "get_dataset"]


class Dataset(HOAMetadata):
    """
    An individual Human Organ Atlas dataset.
    """

    def __str__(self) -> str:
        return f"Dataset(name={self.name})"

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
        children = [
            d
            for d in _DATASETS.values()
            if (
                d.donor.id == self.donor.id
                and d.sample.organ == self.sample.organ
                and d.scan.beamline == self.scan.beamline
                and d.is_zoom
            )
        ]
        return sorted(children, key=lambda c: c.name)

    def get_parents(self) -> list["Dataset"]:
        """
        Get parent dataset(s).

        Parent datasets are full-organ datasets from which a zoom dataset is taken from.

        Notes
        -----
        For zoom datasets, this returns an empty list.

        """
        parents = [
            d
            for d in _DATASETS.values()
            if (
                d.donor.id == self.donor.id
                and d.sample.organ == self.sample.organ
                and d.scan.beamline == self.scan.beamline
                and d.is_full_organ
            )
        ]
        return sorted(parents, key=lambda c: c.name)

    @property
    def _remote_fmt(self) -> Literal["n5", "zarr"]:
        if self.data.gcs_url.startswith("n5://"):
            return "n5"
        if self.data.gcs_url.startswith("zarr://"):
            return "zarr"
        raise RuntimeError("URL must start with n5:// or zarr://")

    @cached_property
    def _remote_store(self) -> zarr.Group:
        """
        Remote data store.
        """
        gcs_url = self.data.gcs_url
        gcs_path = gcs_url.removeprefix("n5://gs://").removeprefix("zarr://gs://")

        # n5://gs://ucl-hip-ct-35a68e99feaae8932b1d44da0358940b/S-20-29/heart/2.5um_VOI-01_bm05/
        bucket, path = gcs_path.split("/", maxsplit=1)
        fs = gcsfs.GCSFileSystem(project=bucket, token="anon", access="read_only")  # noqa: S106
        if self._remote_fmt == "n5":
            store = N5FSStore(url=bucket, fs=fs, mode="r")
        elif self._remote_fmt == "zarr":
            store = zarr.storage.FSStore(url=bucket, fs=fs, mode="r")

        return zarr.open_group(store, mode="r", path=path)

    def _remote_array(self, *, downsample_level: int) -> zarr.core.Array:
        """
        Get an object representing the data array in the remote Google Cloud Store.
        """
        if not downsample_level >= 0:
            msg = "level must be >= 0"
            raise ValueError(msg)

        if self._remote_fmt == "n5":
            key = f"s{downsample_level}"
        else:
            key = f"{downsample_level}"
        return self._remote_store[key]

    def data_array(self, *, downsample_level: int) -> xr.DataArray:
        """
        Get a DataArray representing the array for this image.
        """
        remote_array = self._remote_array(downsample_level=downsample_level)
        dask_array = dask.array.core.from_array(  # type: ignore[no-untyped-call]
            remote_array, chunks=remote_array.chunks
        )
        if self._remote_fmt == "zarr":
            dask_array = dask_array.T

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


def _get_datasets(data_dir: Path) -> dict[str, Dataset]:
    """
    Load dataset metadtata files.
    """
    return {
        f.stem: Dataset.model_validate_json(f.read_text())
        for f in (data_dir).glob("*.json")
    }


_META_DIR = Path(__file__).parent / "data" / "metadata" / "metadata"
_DATASETS = _get_datasets(_META_DIR)
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


def change_metadata_directory(data_dir: Path) -> None:
    """
    Update available datasets from another directory of metadata files.

    Designed for internal project members to load metadata files that aren't yet public.
    """
    global _DATASETS  # noqa: PLW0603
    _DATASETS = _get_datasets(data_dir)
    if len(_DATASETS) == 0:
        raise FileNotFoundError(
            f"Did not find any dataset metadata files at {data_dir}"  # noqa: EM102
        )

"""
Tools for working with individual datasets.

The core class representing a single dataset is [`Dataset`][hoa_tools.dataset.Dataset].
This inherits from [`HOAMetadata`][hoa_tools.metadata.HOAMetadata],
which stores all the metadata for a given dataset.

[`Dataset`][hoa_tools.dataset.Dataset] objects are not designed to be created by users.
To get a [`Dataset`][hoa_tools.dataset.Dataset], use the
[`get_dataset`][hoa_tools.dataset.get_dataset] function in this module.
"""

import warnings
from functools import cached_property
from pathlib import Path
from typing import Literal

import dask.array.core
import gcsfs
import networkx as nx
import numpy as np
import xarray as xr
import zarr.core
import zarr.n5
import zarr.storage

from hoa_tools._n5 import N5FSStore
from hoa_tools.metadata import HOAMetadata
from hoa_tools.types import PhysicalCoordinate

__all__ = ["Dataset", "get_dataset"]


_DATASETS: dict[str, "Dataset"]


class Dataset(HOAMetadata):
    """
    An individual Human Organ Atlas dataset.
    """

    def __str__(self) -> str:
        return f"Dataset(name={self.name})"

    def __hash__(self) -> int:
        return hash(self.name)

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

    def get_registered(self) -> set["Dataset"]:
        """
        Get a set of all datasets that are registered (even indirectly) to this dataset.
        """
        import hoa_tools.registration  # noqa: PLC0415

        dataset_names = nx.node_connected_component(
            hoa_tools.registration.Inventory._graph.to_undirected(),  # noqa: SLF001
            self.name,
        )
        return {get_dataset(name) for name in dataset_names}

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


def _load_datasets_from_files(data_dir: Path) -> dict[str, Dataset]:
    """
    Load dataset metadtata files.
    """
    datasets = {
        f.stem: Dataset.model_validate_json(f.read_text())
        for f in (data_dir).glob("*.json")
    }
    if len(datasets) == 0:
        raise FileNotFoundError(
            f"Did not find any dataset metadata files at {data_dir}"  # noqa: EM102
        )
    return datasets


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
    _DATASETS = _load_datasets_from_files(data_dir)
    _populate_registrations_from_metadata(_DATASETS)


def _populate_registrations_from_metadata(datasets: dict[str, Dataset]) -> None:
    from hoa_tools.registration import Inventory, build_transform  # noqa: PLC0415

    Inventory._clear()  # noqa: SLF001
    for dataset_name in datasets:
        dataset = _DATASETS[dataset_name]
        if (registration := dataset.registration) is not None:
            source_dataset = _DATASETS[registration.source_dataset]
            if registration.target_dataset not in _DATASETS:
                # Some datasets don't have their parent datasets release yet - only warn
                # if we're expecting a parent dataset
                if registration.source_dataset not in [
                    "A129_lung_VOI-02_2.0um_bm18"
                ] and not registration.source_dataset.startswith("LADAF-2021-17_brain"):
                    warnings.warn(
                        f"Did not find target dataset {registration.target_dataset} "
                        f"in dataset inventory. "
                        f"Not adding {registration.source_dataset} "
                        "to registration inventory.",
                        stacklevel=1,
                    )
                continue
            target_dataset = _DATASETS[registration.target_dataset]
            transform = build_transform(
                translation=PhysicalCoordinate(
                    x=registration.translation[0] * target_dataset.data.voxel_size_um,
                    y=registration.translation[1] * target_dataset.data.voxel_size_um,
                    z=registration.translation[2] * target_dataset.data.voxel_size_um,
                ),
                rotation_deg=registration.rotation,
                scale=registration.scale
                * target_dataset.data.voxel_size_um
                / source_dataset.data.voxel_size_um,
            )
            Inventory.add_registration(
                source_dataset=_DATASETS[registration.source_dataset],
                target_dataset=_DATASETS[registration.target_dataset],
                transform=transform,
            )


_META_DIR = Path(__file__).parent / "data" / "metadata" / "metadata"
try:
    change_metadata_directory(_META_DIR)
except FileNotFoundError as e:
    raise ImportError(
        "Did not find any dataset metadata files. "
        "This means there is something wrong with the hoa-tools installation.\n"
        "Please report this at https://github.com/HumanOrganAtlas/hoa-tools\n"
        "If you are installing from source, you might need to "
        "initialise and fetch git submodules. "
    ) from e

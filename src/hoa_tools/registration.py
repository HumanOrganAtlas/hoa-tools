"""
Registration inventory and helpers.

A registration defines a transform between two datasets.
The transform is defined in physical space, and in this library data is always
in units of micro-meters (μm).

Transforms are defined using the `SimpleITK` library.
"""

import numpy as np
import SimpleITK as sitk

from hoa_tools.dataset import Dataset
from hoa_tools.types import PhysicalCoordinate


class RegistrationInventory:
    """
    Inventory of transforms between datasets.

    Transforms are defined as acting on the zyx axes in that order. Note that this
    is different from the order in which the SimpleITK API defines axes in its function
    signatures.
    """

    def __init__(self) -> None:
        """
        Create registration inventory.
        """
        self._registrations: dict[tuple[str, str], sitk.Transform] = {}

    def __contains__(self, item: tuple[Dataset, Dataset]) -> bool:
        """
        Check for existence of registration between two datasets.
        """
        return (item[0].name, item[1].name) in self._registrations

    def get_registration(
        self, *, source_dataset: Dataset, target_dataset: Dataset
    ) -> sitk.Transform:
        """
        Get a registration.
        """
        return self._registrations[(source_dataset.name, target_dataset.name)]

    def add_registration(
        self,
        *,
        source_dataset: Dataset,
        target_dataset: Dataset,
        transform: sitk.Transform,
    ) -> None:
        """
        Add a new transform to the inventory.

        Notes
        -----
        This will override any already defined transforms for these two datasets.

        """
        self._registrations[(source_dataset.name, target_dataset.name)] = transform
        self._registrations[(target_dataset.name, source_dataset.name)] = (
            transform.GetInverse()  # type: ignore[no-untyped-call]
        )

    def _clear(self) -> None:
        """
        Remove all registrations.
        """
        self._registrations = {}


def build_transform(
    *, translation: PhysicalCoordinate, rotation_deg: float, scale: float
) -> sitk.Similarity3DTransform:
    """
    Build a transform from a translation, scale, and rotation.
    """
    axis = (1, 0, 0)
    center = (0, 0, 0)
    return sitk.Similarity3DTransform(  # type: ignore[no-untyped-call]
        scale,
        axis,
        np.deg2rad(rotation_deg),
        (translation.z, translation.y, translation.x),
        center,
    )


Inventory = RegistrationInventory()

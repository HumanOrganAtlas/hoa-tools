import numpy as np
import SimpleITK as sitk

from hoa_tools.dataset import Dataset
from hoa_tools.types import ArrayCoordinate


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
        self, *, source_datset: Dataset, target_dataset: Dataset
    ) -> sitk.Transform:
        """
        Get a registration.
        """
        return self._registrations[(source_datset.name, target_dataset.name)]

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


Inventory = RegistrationInventory()


def build_transform(
    *, translation: ArrayCoordinate, rotation_deg: float, scale: float
) -> sitk.CompositeTransform:
    """
    Build a transform from a translation, scale, and rotation.
    """
    dims = 3
    T1 = sitk.ScaleTransform(dims, (scale, scale, scale))  # type: ignore[no-untyped-call]
    T2 = sitk.Euler3DTransform((0, 0, 0), np.deg2rad(rotation_deg), 0, 0)  # type: ignore[no-untyped-call]
    T3 = sitk.TranslationTransform(  # type: ignore[no-untyped-call]
        dims, (translation["z"], translation["y"], translation["x"])
    )
    return sitk.CompositeTransform([T3, T2, T1])  # type: ignore[no-untyped-call]

import SimpleITK as sitk

from hoa_tools.dataset import Dataset


class RegistrationInventory:
    """
    Inventory of transforms between datasets.
    """

    def __init__(self) -> None:
        """
        Create registration inventory.
        """
        self._registrations: dict[tuple[Dataset, Dataset], sitk.Transform] = {}

    def __contains__(self, item: tuple[Dataset, Dataset]) -> bool:
        """
        Check for existence of registration.
        """
        return item in self._registrations

    def get_registration(
        self, *, source_datset: Dataset, target_dataset: Dataset
    ) -> sitk.Transform:
        """
        Get a registration.
        """
        return self._registrations[(source_datset, target_dataset)]

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
        self._registrations[(source_dataset, target_dataset)] = transform
        self._registrations[(target_dataset, source_dataset)] = transform.GetInverse()


Inventory = RegistrationInventory()

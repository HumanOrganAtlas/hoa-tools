"""
Registration inventory and helpers.

A registration defines a transform between two datasets.
The transform is defined in physical space, and in this library data is always
in units of micro-meters (μm).

Transforms are defined using the `SimpleITK` library.
"""

import itertools
from typing import Any

import networkx as nx
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
        self._graph: nx.DiGraph[Any] = nx.DiGraph()

    def __contains__(self, item: tuple[Dataset, Dataset]) -> bool:
        """
        Check for existence of registration between two datasets.
        """
        try:
            nx.shortest_path(self._graph, item[0].name, item[1].name)
        except nx.exception.NetworkXNoPath:
            return False
        else:
            return True

    def get_registration(
        self, *, source_dataset: Dataset, target_dataset: Dataset
    ) -> sitk.Transform:
        """
        Get a registration.
        """
        try:
            path = nx.shortest_path(
                self._graph, source_dataset.name, target_dataset.name
            )
        except nx.exception.NetworkXNoPath:
            msg = (
                f"No registration path between {source_dataset.name} and "
                f"{target_dataset.name}"
            )
            raise ValueError(msg) from None

        transforms: list[sitk.Transform] = [
            self._graph[p1][p2]["transform"] for p1, p2 in itertools.pairwise(path)
        ]
        if len(transforms) == 1:
            return transforms[0]

        ndim = 3
        t = sitk.CompositeTransform(ndim)  # type: ignore[no-untyped-call]
        for transform in transforms:
            t.AddTransform(transform)  # type: ignore[no-untyped-call]
        return t

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
        self._graph.add_edge(
            source_dataset.name, target_dataset.name, transform=transform
        )
        self._graph.add_edge(
            target_dataset.name,
            source_dataset.name,
            transform=transform.GetInverse(),  # type: ignore[no-untyped-call]
        )

    def _clear(self) -> None:
        """
        Remove all registrations.
        """
        self._graph = nx.DiGraph()


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

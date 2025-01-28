from typing import Any

import zarr.n5
from zarr.storage import FSStore


# Override __init__ to prevent the deprecation warning from showing up
class N5FSStore(zarr.n5.N5FSStore):  # type: ignore[misc]
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        FSStore.__init__(self, *args, **kwargs)

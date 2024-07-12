import math

from .dataset import Dataset


class BoundingBox:
    """
    A cuboid-shaped bounding box for a given dataset at a given downsampling level.
    """

    def __init__(
        self,
        dataset: Dataset,
        *,
        downsample_level: int,
        xmin: int,
        xmax: int,
        ymin: int,
        ymax: int,
        zmin: int,
        zmax: int,
    ) -> None:
        """
        Parameters
        ----------
        dataset :
            Dataset associated with this bounding box.
        downsample_level :
            Downsampling level associated with this bounding box.
            Must be in the range 0 to 4 inclusive.
        xmin, ymin, zmin :
            Coordinates of lower corner of bounding box.
        xmax, ymax, zmax :
            Coordinates of the upper corner of bounding box.
        """
        self.dataset = dataset
        self.downsample_level = downsample_level
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def transform_to_level(self, downsample_level: int) -> "BoundingBox":
        """
        Transform bounding box to a different downsampling level.

        When transforming to a lower-resolution level, the bounding box is
        expanded outwards (ie minimum bounds floored and maximum bounds ceil'ed)
        so that all the pixels of the original box fall within the new box.
        """
        scale_factor = 2.0 ** (self.downsample_level - downsample_level)
        return BoundingBox(
            self.dataset,
            downsample_level=downsample_level,
            xmin=math.floor(self.xmin * scale_factor),
            xmax=math.ceil(self.xmax * scale_factor),
            ymin=math.floor(self.ymin * scale_factor),
            ymax=math.ceil(self.ymax * scale_factor),
            zmin=math.floor(self.zmin * scale_factor),
            zmax=math.ceil(self.zmax * scale_factor),
        )

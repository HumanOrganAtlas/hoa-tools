Working with coordinates
========================

Getting a high-res zoom
-----------------------
The above image shows the lowest resolution data available for this dataset.
If we're intetested in a small volume in the middle of this dataset,
we can define and download the high resolution version.

First, lets define and plot a small bounding box to look at in higher detail::


    >>> from hoa_tools.coordinates import BoundingBox
    >>> bbox = BoundingBox(dataset, downsample_level=4, xmin=105, xmax=125, ymin=120, ymax=130, zmin=z, zmax=z+1)
    >>>
    >>> crop_slice = middle_slice[bbox.ymin:bbox.ymax, bbox.xmin:bbox.xmax]
    >>> plt.imshow(skimage.exposure.equalize_hist(crop_slice))


.. plot::
    :include-source: false

    from hoa_tools.coordinates import BoundingBox
    bbox = BoundingBox(dataset, downsample_level=4, xmin=105, xmax=125, ymin=120, ymax=130, zmin=z, zmax=z+1)

    crop_slice = middle_slice[bbox.ymin:bbox.ymax, bbox.xmin:bbox.xmax]
    plt.imshow(skimage.exposure.equalize_hist(crop_slice))

The bounding box object contains a helpful method to convert it to a higher resolution.
Lets convert it to the highest resolution data available::

    >>> bbox_l0 = bbox.transform_to_level(0)
    >>> print(bbox_l0)

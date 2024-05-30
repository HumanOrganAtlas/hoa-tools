Fetching data
=============

In this tutorial we will fetch some of the data. All public Human Organ Atlas
data is available through a read-only public Google Cloud Storage bucket in
the N5 data format. This is a chunked data format, making it easy to access
sub-volumes of data.

Getting a remote data store
---------------------------

First we'll fetch a `Dataset` object from the inventory::

    >>> import hoa_tools.inventory
    >>> import hoa_tools.dataset
    >>>
    >>> inventory = hoa_tools.inventory.load_inventory()
    >>> dataset_name = inventory.index[0]
    >>> print(dataset_name)
    FO-20-129_lung_left_upper_lobe_VOI-aa_0.65um_bm05
    >>> dataset = hoa_tools.dataset.get_dataset(dataset_name)
    >>> print(dataset)
    Dataset(donor='FO-20-129', organ='lung', organ_context='left_upper_lobe', roi='VOI-aa', resolution=unyt_quantity(0.65, 'μm'), beamline='bm05', nx=3794, ny=3794, nz=7626)

The `Dataset.remote_array` property gives us access to a data array for a dataset.
The ``level`` parameter lets us choose a downsampling level: ``level=0`` is the original
resolution dataset, and each time the level goes up by one the dataset is downsampled
by a factor of 2. All datasets are downsampled to ``level=4``, so lets get the lowest
resolution copy of the data:

    >>> remote_array_l4 = dataset.remote_array(level=4)
    >>> print(remote_array_l4)
    <zarr.core.Array '/FO-20-129/lung-left_upper_lobe/0.65um_VOI-aa_bm05/s4' (477, 238, 238) uint16 read-only>

Here we can see that the array is read-only, 16 bit, and has shape ``(477, 238, 238)``.
This array can be accessed like any normal numpy array. As an example, lets fetch and
show a slice in the x-y plane::

    >>> import matplotlib.pyplot as plt
    >>> import skimage.exposure
    >>>
    >>> middle_slice = remote_array_l4[437, :, :]
    >>> plt.imshow(skimage.exposure.equalize_hist(middle_slice))
    <matplotlib.image.AxesImage object at ...>

.. plot::
    :include-source: false

    import hoa_tools.dataset
    import matplotlib.pyplot as plt
    import skimage.exposure

    dataset = hoa_tools.dataset.get_dataset('FO-20-129_lung_left_upper_lobe_VOI-aa_0.65um_bm05')
    remote_array_l4 = dataset.remote_array(level=4)

    middle_slice = remote_array_l4[437, :, :]
    plt.imshow(skimage.exposure.equalize_hist(middle_slice))

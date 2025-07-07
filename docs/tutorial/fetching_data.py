# # Fetching data

# In this tutorial we will fetch some of the data. All public Human Organ Atlas
# data is available through a read-only public Google Cloud Storage bucket.
# in a chunked data format, making it easy to access sub-volumes of data.

# ## Getting a remote data store

# First we'll fetch a `Dataset` object from the inventory.

import hoa_tools.dataset
import hoa_tools.inventory

inventory = hoa_tools.inventory.load_inventory()
dataset_name = inventory.index[0]
print(dataset_name)

dataset = hoa_tools.dataset.get_dataset(dataset_name)
print(dataset)

# The `Dataset.remote_array` property gives us access to a remote data array for a dataset.
# The ``level`` parameter lets us choose a downsampling level: ``level=0`` is the original
# resolution dataset, and each time the level goes up by one the dataset is downsampled
# by a factor of 2. All datasets are downsampled to ``level=4``, so lets get a remote store
# for the lowest resolution copy of the data.

data_array = dataset.data_array(downsample_level=4)
data_array

# Here we can see that the array is read-only, 16 bit, and has shape ``(477, 238, 238)``.
# At this point no data has been downloaded - to download data you need to index the remote array.
# As an example, lets fetch and show a slice in the x-y plane::


middle_slice = data_array.isel(z=337)
im = middle_slice.plot(cmap="Grays_r")
im.axes.set_aspect("equal")


# If you want to save a part of the array for later analysis, see the [xarray guide
# to reading and writing files](https://docs.xarray.dev/en/stable/user-guide/io.html).

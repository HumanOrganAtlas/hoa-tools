# # Volumes of interest
#
# In this tutorial we will look at how to represent volumes of
# interest in datasets.

import matplotlib.pyplot as plt
import skimage.exposure

import hoa_tools.dataset
from hoa_tools.voi import VOI

# First we'll get a dataset, and inspect the data array

dataset = hoa_tools.dataset.get_dataset(
    "LADAF-2020-27_spleen_complete-organ_25.08um_bm05"
)
dataset.data_array(downsample_level=4)

# Now we'll define a volume of interest (VOI) object

voi = VOI(
    dataset=dataset,
    downsample_level=4,
    lower_corner={"x": 100, "y": 50, "z": 23},
    size={"x": 20, "y": 10, "z": 1},
)

# Once we have a VOI, there's a number of useful things we can do.
# Lets get the data array for the VOI and plot it:

data_array = voi.get_data_array()
data_array

data_array.values = skimage.exposure.equalize_hist(data_array.values)
plt.figure()
ax = data_array.plot(cmap="Grays_r")
ax.axes.set_aspect("equal")


# ## Transforming VOIs
#
# VOIs can be transformed to the different resolution levels of the same dataset.
# Lets get a higher resolution version of the data we plotted above:

new_voi = voi.change_downsample_level(new_downsample_level=2)
new_voi

# Because we've increased the resolution (equivalently, decreased the downsampling level)
# the VOI is now bigger.

new_data_array = new_voi.get_data_array()
new_data_array

new_data_array.values = skimage.exposure.equalize_hist(new_data_array.values)
plt.figure()
ax = new_data_array.isel(z=0).plot(cmap="Grays_r")
ax.axes.set_aspect("equal")

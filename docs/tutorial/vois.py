# # Volumes of interest
#
# In this tutorial we will look at how to represent volumes of
# interest in datasets.

# +
import matplotlib.pyplot as plt

import hoa_tools.dataset
import hoa_tools.voi

# -

# First we'll get a dataset.

dataset = hoa_tools.dataset.get_dataset(
    "LADAF-2020-27_spleen_complete-organ_25.08um_bm05"
)

# Now we'll define a volume of interest (VOI) object. This represents a cuboid shape area within our dataset.

voi = hoa_tools.voi.VOI(
    dataset=dataset,
    downsample_level=4,
    lower_corner={"x": 100, "y": 50, "z": 23},
    size={"x": 40, "y": 20, "z": 1},
)

# Once we have a VOI, there's a number of useful things we can do.
# Lets get the data array for the VOI and plot it:

data_array = voi.get_data_array()
data_array

plt.figure()
ax = data_array.plot(cmap="Grays_r")
ax.axes.set_aspect("equal")
ax.axes.set_title("Downsample level = 4")


# ## Transforming between dowsample levels
#
# VOIs can be transformed to the different resolution levels of the same dataset.
# Lets get a higher resolution version of the data we plotted above:

high_res_voi = voi.change_downsample_level(new_downsample_level=2)

# Because we've increased the resolution (equivalently, decreased the downsampling level)
# the VOI is now bigger.

high_res_data_array = high_res_voi.get_data_array()

# +
fig, axs = plt.subplots(nrows=2)
high_res_data_array.isel(z=0).plot(cmap="Grays_r", ax=axs[0])
axs[0].set_aspect("equal")
axs[0].set_title("Downsample level = 2")

data_array.isel(z=0).plot(cmap="Grays_r", ax=axs[1])
axs[1].set_aspect("equal")
axs[1].set_title("Downsample level = 4")

fig.tight_layout()

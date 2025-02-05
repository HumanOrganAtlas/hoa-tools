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

overview_dataset = hoa_tools.dataset.get_dataset(
    "LADAF-2020-27_spleen_complete-organ_25.08um_bm05"
)

# Now we'll define a volume of interest (VOI) object. This represents a cuboid shape area within our dataset.

voi = hoa_tools.voi.VOI(
    dataset=overview_dataset,
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
# -

# ## Transforming between registered datasets
#
# Now we'll step through transforming a VOI between two datasets that have been registered to each other.
# We'll start by getting one of the children of the overview dataset used above.

children = overview_dataset.get_children()
children

child = children[1]
child

child_array = child.data_array(downsample_level=0)
child_array

# Now select a smaller volume of interest from the child array, and plot it

child_voi = hoa_tools.voi.VOI(
    dataset=child,
    downsample_level=0,
    lower_corner={"x": 1871, "y": 2389, "z": 3770},
    size={"x": 256, "y": 256, "z": 128},
)
child_array = child_voi.get_data_array()
child_array

plt.figure()
ax = child_array.isel(z=0).plot(cmap="Grays_r")
ax.axes.set_aspect("equal")
ax.axes.set_title("VOI slice")

# +

import hoa_tools.registration

# -

transform = hoa_tools.registration.build_transform(
    translation=(591.9188598, 904.645141, 267.368216),
    rotation_deg=0.5000321977,
    scale=0.2412282173,
)
transform.TransformPoint((0, 0, 0))

hoa_tools.registration.Inventory.add_registration(
    source_dataset=child,
    target_dataset=overview_dataset,
    transform=transform,
)


overview_voi = child_voi.transform_to(overview_dataset)
overview_voi

overview_voi.get_data_array()

im = overview_voi.get_data_array().isel(z=0).plot(cmap="Grays_r")
im.axes.set_aspect('equal')



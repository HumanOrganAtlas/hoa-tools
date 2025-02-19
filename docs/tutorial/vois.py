# mypy: disable-error-code="call-arg"

# # Volumes of interest
#
# In this tutorial we will look at how to represent volumes of
# interest in datasets.

# +
import matplotlib.pyplot as plt

import hoa_tools.dataset
import hoa_tools.voi
from hoa_tools.types import PhysicalCoordinate

# -

# First we'll get a dataset.

overview_dataset = hoa_tools.dataset.get_dataset(
    "S-20-29_brain_complete-organ_25.33um_bm05"
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
data_array.isel(z=0).plot(cmap="Grays_r", ax=axs[0])
axs[0].set_aspect("equal")
axs[0].set_title("Downsample level = 4")

high_res_data_array.isel(z=0).plot(cmap="Grays_r", ax=axs[1])
axs[1].set_aspect("equal")
axs[1].set_title("Downsample level = 2")

fig.tight_layout()
# -

# ## Transforming between registered datasets
#
# Now we'll step through transforming a VOI between two datasets that have been registered to each other.
# We'll start by getting one of the children of the overview dataset used above.

children = overview_dataset.get_children()
child = children[9]
child

child_array = child.data_array(downsample_level=0)
child_array

# Now we'll select a smaller volume of interest from the child array, and plot it

child_voi = hoa_tools.voi.VOI(
    dataset=child,
    downsample_level=0,
    lower_corner={"x": 3434, "y": 2060, "z": 2656},
    size={"x": 256, "y": 256, "z": 128},
)
child_array = child_voi.get_data_array()

plt.figure()
ax = child_array.isel(z=0).plot(cmap="Grays_r")
ax.axes.set_aspect("equal")
ax.axes.set_title("Zoom dataset slice")

# Next we'll define a transform between these two datasets. For now this is entered manually, but in the future we will automatically populate the registration inventory with transforms between datasets.

import hoa_tools.registration

transform = hoa_tools.registration.build_transform(
    translation=PhysicalCoordinate(
        x=2073.796888 * overview_dataset.data.voxel_size_um,
        y=1199.064571 * overview_dataset.data.voxel_size_um,
        z=3634.531617 * overview_dataset.data.voxel_size_um,
    ),
    rotation_deg=2.299992208,
    scale=0.2566130457 * overview_dataset.data.voxel_size_um / child.data.voxel_size_um,
)

# With the trainsform defined, add it to the registration inventory.

hoa_tools.registration.Inventory.add_registration(
    source_dataset=child,
    target_dataset=overview_dataset,
    transform=transform,
)


# Now that `hoa_tools` has this transformation in the registration registry, it can transform a VOI in one dataset to the other dataset.

overview_voi = child_voi.transform_to(overview_dataset)
overview_voi

# Finally, lets plot the overview and child datasets together. We can see that the same structures are visible in both, so the registration is approximately accurate, and all the transformations worked.
#
# In the next tutorial section we'll see how to do a more accurate registration of just these small sub-volumes of data in order to do quantitative comparisons.

overview_array = overview_voi.get_data_array()

# +
fig, axs = plt.subplots(nrows=2, figsize=(6, 9))

ax = axs[0]
child_array.isel(z=0).plot(cmap="Grays_r", ax=ax)
ax.set_aspect("equal")
ax.set_title("Zoom dataset")

ax = axs[1]
overview_array.isel(z=0).plot(cmap="Grays_r", ax=ax)
ax.set_aspect("equal")
ax.set_title("Overview dataset")
fig.tight_layout()

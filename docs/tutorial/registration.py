# # Improved registrations
#
# Although datasets in the Human Organ Atlas come with a rough registration, sometimes it's useful to do a more accurate registration on a smaller volume of interest of data.
# This can help quantitative comparisons where an accurate registration is important.

# +
import matplotlib.pyplot as plt

import hoa_tools.dataset
import hoa_tools.registration
import hoa_tools.voi

# -

# Lets start by getting an overview dataset, and seeing what datasets are registered to it.

overview_dataset = hoa_tools.dataset.get_dataset(
    "S-20-29_brain_complete-organ_25.33um_bm05"
)
sorted([d.name for d in overview_dataset.get_registered()])

# From these we'll take a zoom dataset, and define a VOI in the zoom dataset.

zoom_dataset = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-04_6.5um_bm05")
zoom_voi = hoa_tools.voi.VOI(
    dataset=zoom_dataset,
    downsample_level=0,
    lower_corner={"x": 3434, "y": 2060, "z": 2656},
    size={"x": 256, "y": 256, "z": 128},
)


# Get the data in the VOI

# +
zoom_array = zoom_voi.get_data_array()

overview_voi = zoom_voi.transform_to(overview_dataset)
overview_array = overview_voi.get_data_array()
# -

# Plot the data

# +
fig = plt.figure()
ax = zoom_array.isel(z=0).plot(cmap="Grays_r")
ax.axes.set_aspect("equal")
ax.axes.set_title("Zoom dataset")

fig = plt.figure()
ax = overview_array.isel(z=0).plot(cmap="Grays_r")
ax.axes.set_aspect("equal")
ax.axes.set_title("Overview dataset")
# -

# These plots show that the two datasets are defined on different grids.
# In order to do a quanititive comparison, we need to resample one dataset on to the grid of the other datsaet.
# Here we resample the overview VOI on to the grid of the zoom VOI:

import SimpleITK as sitk

resampled_overview = overview_voi.get_data_array_on_voi(
    zoom_voi, interpolator=sitk.sitkNearestNeighbor
)

# Now they are resampled, lets plot the middle slice of each dataset as a simple qualititive comparison

# +
yslice = 70
zslice = 64

fig = plt.figure()
im = zoom_array.isel(z=zslice).plot(cmap="Grays_r")
im.axes.set_aspect("equal")
im.axes.set_title("Zoom dataset")
im.axes.axhline(zoom_array.coords["y"][yslice], color="tab:blue")

fig = plt.figure()
im = resampled_overview.isel(z=zslice).plot(cmap="Grays_r")
im.axes.set_aspect("equal")
im.axes.set_title("Overview dataset\n(resampled on zoom dataset grid)")
im.axes.axhline(resampled_overview.coords["y"][yslice], color="tab:red")

fig, ax = plt.subplots()

zoom_array.isel(z=zslice, y=yslice).plot(ax=ax, color="tab:blue")

ax2 = ax.twinx()
resampled_overview.isel(z=zslice, y=yslice).plot(ax=ax2, color="tab:red")
ax2.set_title("")

ax.set_title("Zoom (blue) and resampled overview (red) comparison")
# -

# ## A more accurate registration
#
# Although it's possible to do a 1:1 comparison after resampling, the images aren't aligned very well.
# In this section we'll step through doing a better registration, using the registration from hoa-tools' registration inventory as a starting point.
#
# To do this we'll use SimpleITK.
# The example here largely follows the [registration introduction](https://insightsoftwareconsortium.github.io/SimpleITK-Notebooks/Python_html/60_Registration_Introduction.html) in the [SimpleITK tutorial notebooks](https://insightsoftwareconsortium.github.io/SimpleITK-Notebooks/).
#
# To start, we'll get both VOIs as SimpleITK images.

zoom_image = zoom_voi.get_sitk_image()
overview_image = overview_voi.get_sitk_image()

# Now we'll get the initial transform from the hoa-tools registration inventory, and then update it so the cnetre of rotation of the transform is in the middle of the zoom image.

initial_transform = hoa_tools.registration.Inventory.get_registration(
    source_dataset=zoom_voi.dataset, target_dataset=overview_voi.dataset
)
initial_transform = sitk.CenteredTransformInitializer(
    zoom_image, overview_image, initial_transform
)

# Now we'll set up the registration and run it.

# +
registration_method = sitk.ImageRegistrationMethod()

registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
registration_method.SetMetricSamplingPercentage(0.1)

registration_method.SetInterpolator(sitk.sitkLinear)

registration_method.SetOptimizerAsGradientDescent(
    learningRate=1.0,
    numberOfIterations=100,
    convergenceMinimumValue=1e-6,
    convergenceWindowSize=10,
)
registration_method.SetOptimizerScalesFromPhysicalShift()

registration_method.SetInitialTransform(initial_transform, inPlace=False)
final_transform = registration_method.Execute(
    sitk.Cast(zoom_image, sitk.sitkFloat32), sitk.Cast(overview_image, sitk.sitkFloat32)
)
# -

# Using the new transform, resample the overview VOI to the zoom VOI.

resampled_overview = overview_voi.get_data_array_on_voi(
    zoom_voi, interpolator=sitk.sitkLinear, transform=final_transform.GetInverse()
)

# And finally, plot as before.
# Hopefully you can see that the data is aligned much better now, and we can do a more meaningful comparison.

# +
yslice = 180
zslice = 64

fig = plt.figure()
im = zoom_array.isel(z=zslice).plot(cmap="Grays_r")
im.axes.set_aspect("equal")
im.axes.set_title("Zoom dataset")
im.axes.axhline(zoom_array.coords["y"][yslice], color="tab:blue")

fig = plt.figure()
im = resampled_overview.isel(z=zslice).plot(cmap="Grays_r")
im.axes.set_aspect("equal")
im.axes.set_title("Overview dataset\n(resampled on zoom dataset grid)")
im.axes.axhline(resampled_overview.coords["y"][yslice], color="tab:red")

fig, ax = plt.subplots()

zoom_array.isel(z=zslice, y=yslice).plot(ax=ax, color="tab:blue")

ax2 = ax.twinx()
resampled_overview.isel(z=zslice, y=yslice).plot(ax=ax2, color="tab:red")
ax2.set_title("")

ax.set_title("Zoom (blue) and resampled overview (red) comparison")

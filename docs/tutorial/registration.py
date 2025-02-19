# # Improved registrations
#
# Although datasets in the Human Organ Atlas come with a rough registration, sometimes it's useful to do a more accurate registration on a smaller volume of interest of data.
# This can help quantitative comparisons where an accurate registration is important.

# +
import matplotlib.pyplot as plt

import hoa_tools.dataset
import hoa_tools.voi

# -

overview_dataset = hoa_tools.dataset.get_dataset(
    "S-20-29_brain_complete-organ_25.33um_bm05"
)
zoom_dataset = hoa_tools.dataset.get_dataset("S-20-29_brain_VOI-04_6.5um_bm05")

# +
zoom_voi = hoa_tools.voi.VOI(
    dataset=zoom_dataset,
    downsample_level=0,
    lower_corner={"x": 3434, "y": 2060, "z": 2656},
    size={"x": 256, "y": 256, "z": 128},
)

zoom_array = zoom_voi.get_data_array()

overview_voi = zoom_voi.transform_to(overview_dataset)
overview_array = overview_voi.get_data_array()

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

resampled_overview = overview_voi.get_data_array_on_voi(zoom_voi)

# +
yslice = 128
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

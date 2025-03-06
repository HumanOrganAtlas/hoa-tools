# # Individual datasets
#
# In this chapter we'll look at what we can do with an individual dataset.
# In ``hoa-tools`` individual datasets are represented by `Dataset` objects.

import pandas as pd

import hoa_tools.dataset
import hoa_tools.inventory

pd.options.display.width = None  # type: ignore[assignment]

# First, lets print all the spleen datasets available from the inventory::

inventory = hoa_tools.inventory.load_inventory()
spleen_inventory = inventory[inventory["organ"] == "spleen"]
spleen_inventory

# We can see that three datasets are available. They are from the same organ, with one being the full
# organ dataset and two being high resolution region of interest datasets. Lets get the full organ
# dataset

whole_spleen = hoa_tools.dataset.get_dataset(
    "LADAF-2020-27_spleen_complete-organ_25.08um_bm05"
)
whole_spleen

# Because this is a full-organ dataset, it will have a number of child datasets. These are scans of
# the same organ taken at a higher resolution over a subset of the full volume. For our selected
# dataset these child datasets are::

child_datasets = whole_spleen.get_children()
for dataset in child_datasets:
    print(dataset)

# We can see there are two child datasets, one at a resolution of 1.29 μm and one at a
# resolution of 6.05 μm.

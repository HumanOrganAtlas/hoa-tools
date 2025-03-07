# # Dataset Inventory

# In the first tutorial we will show how to search for available data
# using the `hoa_tools.inventory` module. By the end you should know
# how to search and filter the built in dataset inventory.

import pandas as pd

import hoa_tools.inventory

pd.options.display.width = None  # type: ignore[assignment]

# ## Loading the inventory
#
# First we'll load the inventory::


inventory = hoa_tools.inventory.load_inventory()
inventory

# The inventory is a `pandas.DataFrame` object. Each row is a different dataset, and each column
# contains the properties of the dataset. The available columns are::

print(list(inventory.columns))

# ## Searching the inventory
#
# To find all the spleen datasets we can filter the dataframe::

inventory[inventory["organ"] == "spleen"]

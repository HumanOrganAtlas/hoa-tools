# # Dataset Inventory

# In this tutorial we will use the  `hoa_tools.inventory` module
# to find all the spleen datasets in the Human Organ Atlas.

import pandas as pd

import hoa_tools.inventory

pd.options.display.width = None

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

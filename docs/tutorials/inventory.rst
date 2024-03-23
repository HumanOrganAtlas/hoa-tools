Working with the dataset inventory
==================================

The `hoa_tools.inventory` module contains tools for loading and working with
the inventory of datasets available in the Human Organ Atlas.

In this tutorial the end goal is to find all the datasets that are lungs.

Loading the inventory
---------------------
First we'll load the inventory::

    >>> import hoa_tools.inventory
    >>>
    >>> inventory = hoa_tools.inventory.load_inventory()
    >>> print(inventory)
                                                     name          donor   organ     organ_context  ...     nz  contrast_low  contrast_high  size_gb_uncompressed
    0   FO-20-129_lung_left_upper_lobe_VOI-aa_0.65um_bm05      FO-20-129    lung   left_upper_lobe  ...   7626         15545          22743            219.543938
    1   FO-20-129_lung_left_upper_lobe_VOI-01.2b_2.22u...      FO-20-129    lung   left_upper_lobe  ...  50838         17480          36263           1503.180526
    2   FO-20-129_lung_left_upper_lobe_VOI-03.2_2.22um...      FO-20-129    lung   left_upper_lobe  ...  20119          8950          21600            595.808251
    3   FO-20-129_lung_left_upper_lobe_VOI-08.2_2.22um...      FO-20-129    lung   left_upper_lobe  ...   7466          4058           8465            220.525467
    4   FO-20-129_lung_left_upper_lobe_VOI-03b-bis_2.2...      FO-20-129    lung   left_upper_lobe  ...   7281         10655          34421            199.677187
    ...

The inventory is a `pandas.DataFrame` object. Each row is a different dataset, and each column
contains the properties of the dataset. The available columns are::

    >>> print(list(inventory.columns))
     ['name', 'donor', 'organ', 'organ_context', 'roi', 'resolution_um', 'beamline', 'nx', 'ny', 'nz', 'contrast_low', 'contrast_high', 'size_gb_uncompressed']

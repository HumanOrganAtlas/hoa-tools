Dataset Inventory
=================

In this tutorial we will use the  `hoa_tools.inventory` module
to find all the spleen datasets in the Human Organ Atlas.

    >>> import pandas as pd
    >>> pd.options.display.max_rows = 10
    >>> pd.options.display.width = None

Loading the inventory
---------------------
First we'll load the inventory::

    >>> import hoa_tools.inventory
    >>>
    >>> inventory = hoa_tools.inventory.load_inventory()
    >>> print(inventory)
                                                            donor organ    organ_context             roi  resolution_um  beamline    nx    ny     nz  contrast_low  contrast_high  size_gb_uncompressed
    name
    FO-20-129_lung_left_upper_lobe_VOI-aa_0.65um_bm05   FO-20-129  lung  left_upper_lobe          VOI-aa           0.65         5  3794  3794   7626         15545          22743            219.543938
    FO-20-129_lung_left_upper_lobe_VOI-01.2_2.22um_...  FO-20-129  lung  left_upper_lobe        VOI-01.2           2.22         5  3853  3853   5296         14609          47690            157.244691
    FO-20-129_lung_left_upper_lobe_VOI-01.2b_2.22um...  FO-20-129  lung  left_upper_lobe       VOI-01.2b           2.22         5  3845  3845  50838         17480          36263           1503.180526
    FO-20-129_lung_left_upper_lobe_VOI-02.2_2.22um_...  FO-20-129  lung  left_upper_lobe        VOI-02.2           2.22         5  3848  3848  16505         12837          31615            488.782503
    FO-20-129_lung_left_upper_lobe_VOI-03.2_2.22um_...  FO-20-129  lung  left_upper_lobe        VOI-03.2           2.22         5  3848  3848  20119          8950          21600            595.808251
    ...                                                       ...   ...              ...             ...            ...       ...   ...   ...    ...           ...            ...                   ...
    S-20-29_lung_left_complete-organ_25.31um_bm05         S-20-29  lung             left  complete-organ          25.31         5  3814  5350   6391         17445          19828            260.815432
    S-20-29_lung_left_VOI-01_6.5um_bm05                   S-20-29  lung             left          VOI-01           6.50         5  3838  3838  20756          2967           7876            611.481889
    S-20-29_lung_left_VOI-02_6.5um_bm05                   S-20-29  lung             left          VOI-02           6.50         5  3838  3838  10586          4910           9132            311.868726
    S-20-29_lung_left_VOI-04_6.5um_bm05                   S-20-29  lung             left          VOI-04           6.50         5  3835  3835   8890          3573           8607            261.494461
    S-20-29_lung_left_VOI-05_6.5um_bm05                   S-20-29  lung             left          VOI-05           6.50         5  3833  3833  20077          4620           8124            589.938111
    <BLANKLINE>
    [149 rows x 12 columns]

The inventory is a `pandas.DataFrame` object. Each row is a different dataset, and each column
contains the properties of the dataset. The available columns are::

    >>> print(list(inventory.columns))
    ['donor', 'organ', 'organ_context', 'roi', 'resolution_um', 'beamline', 'nx', 'ny', 'nz', 'contrast_low', 'contrast_high', 'size_gb_uncompressed']

Searching the inventory
-----------------------

To find all the spleen datasets we can filter the dataframe::

    >>> spleen_inventory = inventory[inventory["organ"] == "spleen"]
    >>> print(spleen_inventory)
                                                              donor   organ organ_context             roi  resolution_um  beamline    nx    ny     nz  contrast_low  contrast_high  size_gb_uncompressed
    name
    LADAF-2020-27_spleen_central-column_1.29um_bm05   LADAF-2020-27  spleen                central-column           1.29         5  3823  3823  10982         27852          30408            321.011086
    LADAF-2020-27_spleen_complete-organ_25.08um_bm05  LADAF-2020-27  spleen                complete-organ          25.08         5  2919  2151   1900         28069          33269             23.859322
    LADAF-2020-27_spleen_central-column_6.05um_bm05   LADAF-2020-27  spleen                central-column           6.05         5  3791  3791   7540          4139           7143            216.724949
    LADAF-2021-17_spleen_complete-organ_25.0um_bm05   LADAF-2021-17  spleen                complete-organ          25.00         5  3521  2352   4798         14608          38970             79.468238

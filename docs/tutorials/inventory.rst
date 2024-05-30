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
                                                                donor  organ    organ_context          roi  resolution_um  beamline    nx    ny     nz  contrast_low  contrast_high  size_gb_uncompressed
    name
    FO-20-129_lung_left_upper_lobe_VOI-aa_0.65um_bm05       FO-20-129   lung  left_upper_lobe       VOI-aa           0.65         5  3794  3794   7626         15545          22743            219.543938
    FO-20-129_lung_left_upper_lobe_VOI-01.2b_2.22um...      FO-20-129   lung  left_upper_lobe    VOI-01.2b           2.22         5  3845  3845  50838         17480          36263           1503.180526
    FO-20-129_lung_left_upper_lobe_VOI-03.2_2.22um_...      FO-20-129   lung  left_upper_lobe     VOI-03.2           2.22         5  3848  3848  20119          8950          21600            595.808251
    FO-20-129_lung_left_upper_lobe_VOI-08.2_2.22um_...      FO-20-129   lung  left_upper_lobe     VOI-08.2           2.22         5  3843  3843   7466          4058           8465            220.525467
    FO-20-129_lung_left_upper_lobe_VOI-03b-bis_2.2u...      FO-20-129   lung  left_upper_lobe  VOI-03b-bis           2.20         5  3703  3703   7281         10655          34421            199.677187
    ...                                                           ...    ...              ...          ...            ...       ...   ...   ...    ...           ...            ...                   ...
    LADAF-2021-64_heart_VOI-02_6.51um_bm18              LADAF-2021-64  heart                        VOI-02           6.51        18  3836  3836   5227          2303           3680            153.829523
    LADAF-2021-64_heart_VOI-04_6.51um_bm18              LADAF-2021-64  heart                        VOI-04           6.51        18  3839  3839   6761          5148          10233            199.286168
    LADAF-2021-64_heart_VOI-05_6.51um_bm18              LADAF-2021-64  heart                        VOI-05           6.51        18  3839  3839   8295         19545          42582            244.502109
    LADAF-2021-64_heart_VOI-06_6.51um_bm18              LADAF-2021-64  heart                        VOI-06           6.51        18  3837  3837   9062          1960           4024            266.831841
    LADAF-2021-64_heart_VOI-07_6.51um_bm18              LADAF-2021-64  heart                        VOI-07           6.51        18  3837  3837  14425          4105           9311            424.746116
    <BLANKLINE>
    [82 rows x 12 columns]

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

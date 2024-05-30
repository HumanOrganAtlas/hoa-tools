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
                                                                donor   organ                   roi  resolution_um  beamline    nx     ny     nz  contrast_low  contrast_high  size_gb_uncompressed
    name
    FO-20-129_lung_left_upper_lobe_VOI-aa_0.65um_bm05       FO-20-129    lung                VOI-aa           0.65         5  3794   3794   7626         15545          22743            219.543938
    FO-20-129_lung_left_upper_lobe_VOI-01.2b_2.22um...      FO-20-129    lung             VOI-01.2b           2.22         5  3845   3845  50838         17480          36263           1503.180526
    FO-20-129_lung_left_upper_lobe_VOI-03.2_2.22um_...      FO-20-129    lung              VOI-03.2           2.22         5  3848   3848  20119          8950          21600            595.808251
    FO-20-129_lung_left_upper_lobe_VOI-08.2_2.22um_...      FO-20-129    lung              VOI-08.2           2.22         5  3843   3843   7466          4058           8465            220.525467
    FO-20-129_lung_left_upper_lobe_VOI-03b-bis_2.2u...      FO-20-129    lung           VOI-03b-bis           2.20         5  3703   3703   7281         10655          34421            199.677187
    ...                                                           ...     ...                   ...            ...       ...   ...    ...    ...           ...            ...                   ...
    LADAF-2020-31_brain_cerebellum_2.45um_bm05          LADAF-2020-31   brain            cerebellum           2.45         5  3895   3895   6334         14966          30947            192.186545
    LADAF-2020-31_brain_complete-organ_25.08um_bm05     LADAF-2020-31   brain        complete-organ          25.08         5  5965   5965   6991         15671          24381            497.496688
    LADAF-2020-31_brain_cerebellum-occipital_6.05um...  LADAF-2020-31   brain  cerebellum-occipital           6.05         5  3867   3867   4678         13047          30883            139.906714
    LADAF-2020-31_kidney_lateral-transect_2.5um_bm05    LADAF-2020-31  kidney      lateral-transect           2.50         5  3873  15091   1354             0          19230            158.275676
    LADAF-2020-31_kidney_complete-organ_25.0um_bm05     LADAF-2020-31  kidney        complete-organ          25.00         5  2215   3287   4282         13367          33403             62.351958
    <BLANKLINE>
    [51 rows x 11 columns]

The inventory is a `pandas.DataFrame` object. Each row is a different dataset, and each column
contains the properties of the dataset. The available columns are::

    >>> print(list(inventory.columns))
    ['donor', 'organ', 'roi', 'resolution_um', 'beamline', 'nx', 'ny', 'nz', 'contrast_low', 'contrast_high', 'size_gb_uncompressed']

Searching the inventory
-----------------------

To find all the spleen datasets we can filter the dataframe::

    >>> spleen_inventory = inventory[inventory["organ"] == "spleen"]
    >>> print(spleen_inventory)
                                                              donor   organ             roi  resolution_um  beamline    nx    ny     nz  contrast_low  contrast_high  size_gb_uncompressed
    name
    LADAF-2020-27_spleen_central-column_1.29um_bm05   LADAF-2020-27  spleen  central-column           1.29         5  3823  3823  10982         27852          30408            321.011086
    LADAF-2020-27_spleen_complete-organ_25.08um_bm05  LADAF-2020-27  spleen  complete-organ          25.08         5  2919  2151   1900         28069          33269             23.859322
    LADAF-2020-27_spleen_central-column_6.05um_bm05   LADAF-2020-27  spleen  central-column           6.05         5  3791  3791   7540          4139           7143            216.724949

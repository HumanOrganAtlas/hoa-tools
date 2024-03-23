Dataset Inventory
=================

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
                                                                donor   organ     organ_context  ... contrast_low  contrast_high  size_gb_uncompressed
    name                                                                                         ...
    FO-20-129_lung_left_upper_lobe_VOI-aa_0.65um_bm05       FO-20-129    lung   left_upper_lobe  ...        15545          22743            219.543938
    FO-20-129_lung_left_upper_lobe_VOI-01.2b_2.22um...      FO-20-129    lung   left_upper_lobe  ...        17480          36263           1503.180526
    FO-20-129_lung_left_upper_lobe_VOI-03.2_2.22um_...      FO-20-129    lung   left_upper_lobe  ...         8950          21600            595.808251
    FO-20-129_lung_left_upper_lobe_VOI-08.2_2.22um_...      FO-20-129    lung   left_upper_lobe  ...         4058           8465            220.525467
    FO-20-129_lung_left_upper_lobe_VOI-03b-bis_2.2u...      FO-20-129    lung   left_upper_lobe  ...        10655          34421            199.677187
    FO-20-129_lung_left_upper_lobe_VOI-aa-bis_2.2um...      FO-20-129    lung   left_upper_lobe  ...         7380          16425            473.839094
    FO-20-129_lung_left_upper_lobe_complete-upper-l...      FO-20-129    lung   left_upper_lobe  ...         8245          29777            125.625583
    FO-20-129_lung_left_upper_lobe_complete-upper-l...      FO-20-129    lung   left_upper_lobe  ...        52962          58138            107.019297
    FO-20-129_lung_left_upper_lobe_VOI-01_6.24um_bm05       FO-20-129    lung   left_upper_lobe  ...        13849          31712            635.712307
    FO-20-129_lung_left_upper_lobe_VOI-03_6.24um_bm05       FO-20-129    lung   left_upper_lobe  ...        17314          35417            419.919904
    FO-20-129_lung_left_upper_lobe_VOI-04_6.24um_bm05       FO-20-129    lung   left_upper_lobe  ...        10673          23044            153.593950
    FO-20-129_lung_left_upper_lobe_VOI-04-bis_6.5um...      FO-20-129    lung   left_upper_lobe  ...        13795          31538            168.247186
    FO-20-129_lung_right_upper_lobe_core-biopsy_2.2...      FO-20-129    lung  right_upper_lobe  ...         2880           5377            164.970667
    GLR-163_lung_right_lower_lobe_core-biopsy_2.45u...        GLR-163    lung  right_lower_lobe  ...        14199          28254            125.517429
    LADAF-2020-27_heart_L-vent-muscle_2.22um_bm05       LADAF-2020-27   heart               NaN  ...        25660          35923            367.381112
    LADAF-2020-27_heart_complete-organ_25.08um_bm05     LADAF-2020-27   heart               NaN  ...        22695          26334            443.696114
    LADAF-2020-27_heart_LR-vent-muscles-ramus-inter...  LADAF-2020-27   heart               NaN  ...        22136          25560            293.563001
    LADAF-2020-27_kidney_left_central-column_1.29um...  LADAF-2020-27  kidney              left  ...        24572          27468            325.882986
    LADAF-2020-27_kidney_left_complete-organ_25.08u...  LADAF-2020-27  kidney              left  ...        17549          21593             58.301390
    LADAF-2020-27_kidney_left_central-column_6.05um...  LADAF-2020-27  kidney              left  ...        11179          20929            217.182537
    LADAF-2020-27_lung_left_VOI-01-upper-lobe-apica...  LADAF-2020-27    lung              left  ...        19456          37967            101.268298
    LADAF-2020-27_lung_left_VOI-02-lower-lobe-basal...  LADAF-2020-27    lung              left  ...        11357          29938            142.415249
    LADAF-2020-27_lung_left_VOI-06-lower-lobe-basal...  LADAF-2020-27    lung              left  ...        14710          40222             59.426738
    LADAF-2020-27_lung_left_FSC-A_2.51um_bm05           LADAF-2020-27    lung              left  ...        16648          39717             37.030162
    LADAF-2020-27_lung_left_FSC-B_2.51um_bm05           LADAF-2020-27    lung              left  ...        16537          40056             37.030162
    LADAF-2020-27_lung_left_VOI-01-upper-lobe-apica...  LADAF-2020-27    lung              left  ...         3736           7687            384.796902
    LADAF-2020-27_lung_left_VOI-02b-upper-lobe-apic...  LADAF-2020-27    lung              left  ...         5937           9556            168.522379
    LADAF-2020-27_lung_left_VOI-03-upper-lobe-apica...  LADAF-2020-27    lung              left  ...        18039          35928            168.348645
    LADAF-2020-27_lung_left_VOI-04-upper-lobe-media...  LADAF-2020-27    lung              left  ...         3009           7352            168.175000
    LADAF-2020-27_lung_left_VOI-05-lower-lobe-basal...  LADAF-2020-27    lung              left  ...         4353           7927            457.582883
    LADAF-2020-27_lung_left_complete-organ_25.08um_...  LADAF-2020-27    lung              left  ...        19516          21139            623.923053
    LADAF-2020-27_lung_left_FSC-A_25.25um_bm05          LADAF-2020-27    lung              left  ...         2528           6996              2.539565
    LADAF-2020-27_lung_left_FSC-B_25.25um_bm05          LADAF-2020-27    lung              left  ...         2435           6933              2.539565
    LADAF-2020-27_lung_left_VOI-01-upper-lobe-apica...  LADAF-2020-27    lung              left  ...         9692          33163             36.762903
    LADAF-2020-27_lung_left_VOI-02-lower-lobe-basal...  LADAF-2020-27    lung              left  ...         1987           6526            203.175954
    LADAF-2020-27_lung_left_VOI-06-lower-lobe-basal...  LADAF-2020-27    lung              left  ...         3659           7330            236.098638
    LADAF-2020-27_lung_left_FSC-A_6.5um_bm05            LADAF-2020-27    lung              left  ...         3488           8146             14.093923
    LADAF-2020-27_lung_left_FSC-B_6.5um_bm05            LADAF-2020-27    lung              left  ...         3526           8063             14.069134
    LADAF-2020-27_lung_left_VOI-01-upper-lobe-apica...  LADAF-2020-27    lung              left  ...         8024          12078            223.034263
    LADAF-2020-27_lung_left_VOI-02b-upper-lobe-medi...  LADAF-2020-27    lung              left  ...        12592          19828            122.119980
    LADAF-2020-27_lung_left_VOI-03b-interlobular-fi...  LADAF-2020-27    lung              left  ...        12458          44014             41.554223
    LADAF-2020-27_lung_left_VOI-04b-lower-lobe-basa...  LADAF-2020-27    lung              left  ...        12215          17307            484.974690
    LADAF-2020-27_lung_left_VOI-05-upper-lobe-apica...  LADAF-2020-27    lung              left  ...         9214          13131            272.905359
    LADAF-2020-27_spleen_central-column_1.29um_bm05     LADAF-2020-27  spleen               NaN  ...        27852          30408            321.011086
    LADAF-2020-27_spleen_complete-organ_25.08um_bm05    LADAF-2020-27  spleen               NaN  ...        28069          33269             23.859322
    LADAF-2020-27_spleen_central-column_6.05um_bm05     LADAF-2020-27  spleen               NaN  ...         4139           7143            216.724949
    LADAF-2020-31_brain_cerebellum_2.45um_bm05          LADAF-2020-31   brain               NaN  ...        14966          30947            192.186545
    LADAF-2020-31_brain_complete-organ_25.08um_bm05     LADAF-2020-31   brain               NaN  ...        15671          24381            497.496688
    LADAF-2020-31_brain_cerebellum-occipital_6.05um...  LADAF-2020-31   brain               NaN  ...        13047          30883            139.906714
    LADAF-2020-31_kidney_lateral-transect_2.5um_bm05    LADAF-2020-31  kidney               NaN  ...            0          19230            158.275676
    LADAF-2020-31_kidney_complete-organ_25.0um_bm05     LADAF-2020-31  kidney               NaN  ...        13367          33403             62.351958
    <BLANKLINE>
    [51 rows x 12 columns]

The inventory is a `pandas.DataFrame` object. Each row is a different dataset, and each column
contains the properties of the dataset. The available columns are::

    >>> print(list(inventory.columns))
    ['donor', 'organ', 'organ_context', 'roi', 'resolution_um', 'beamline', 'nx', 'ny', 'nz', 'contrast_low', 'contrast_high', 'size_gb_uncompressed']

Individual datasets
===================

In this tutorial we'll look at what we can do with an individual dataset.
In ``hoa-tools`` individual datasets are represented by `Dataset` objects.

    >>> import pandas as pd
    >>> pd.options.display.max_rows = 10
    >>> pd.options.display.width = None

First, lets print all the spleen datasets available from the inventory::


    >>> import hoa_tools.inventory
    >>>
    >>> inventory = hoa_tools.inventory.load_inventory()
    >>> spleen_inventory = inventory[inventory["organ"] == "spleen"]
    >>> print(spleen_inventory)
                                                              donor   organ organ_context             roi  resolution_um  beamline    nx    ny     nz  contrast_low  contrast_high  size_gb_uncompressed
    name
    LADAF-2020-27_spleen_central-column_1.29um_bm05   LADAF-2020-27  spleen                central-column           1.29         5  3823  3823  10982         27852          30408            321.011086
    LADAF-2020-27_spleen_complete-organ_25.08um_bm05  LADAF-2020-27  spleen                complete-organ          25.08         5  2919  2151   1900         28069          33269             23.859322
    LADAF-2020-27_spleen_central-column_6.05um_bm05   LADAF-2020-27  spleen                central-column           6.05         5  3791  3791   7540          4139           7143            216.724949
    LADAF-2021-17_spleen_complete-organ_25.0um_bm05   LADAF-2021-17  spleen                complete-organ          25.00         5  3521  2352   4798         14608          38970             79.468238

We can see that three datasets are available. They are from the same organ, with one being the full
organ dataset and two being high resolution region of interest datasets. Lets get the full organ
dataset::

    >>> import hoa_tools.dataset
    >>>
    >>> whole_spleen = hoa_tools.dataset.get_dataset('LADAF-2020-27_spleen_complete-organ_25.08um_bm05')
    >>> print(whole_spleen)
    Dataset(donor='LADAF-2020-27', organ='spleen', organ_context='', roi='complete-organ', resolution=unyt_quantity(25.08, 'μm'), beamline='bm05', nx=2919, ny=2151, nz=1900)

Because this is a full-organ dataset, it will have a number of child datasets. These are scans of
the same organ taken at a higher resolution over a subset of the full volume. For our selected
dataset these child datasets are::

    >>> child_datasets = whole_spleen.get_children()
    >>> for dataset in child_datasets:
    ...     print(dataset)
    Dataset(donor='LADAF-2020-27', organ='spleen', organ_context='', roi='central-column', resolution=unyt_quantity(1.29, 'μm'), beamline='bm05', nx=3823, ny=3823, nz=10982)
    Dataset(donor='LADAF-2020-27', organ='spleen', organ_context='', roi='central-column', resolution=unyt_quantity(6.05, 'μm'), beamline='bm05', nx=3791, ny=3791, nz=7540)

We can see there are two child datasets, one at a resolution of 1.29 μm and one at a
resolution of 6.05 μm.

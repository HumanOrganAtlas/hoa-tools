Individual datasets
===================

In this tutorial we'll look at what we can do with an individual dataset.
In ``hoa-tools`` individual datasets are represented by `Dataset` objects.

First, lets print all the spleen datasets available from the inventory::


    >>> import hoa_tools.inventory
    >>>
    >>> inventory = hoa_tools.inventory.load_inventory()
    >>> spleen_inventory = inventory[inventory["organ"] == "spleen"]
    >>> print(spleen_inventory)
                                                              donor   organ organ_context             roi  resolution_um  ...    ny     nz  contrast_low  contrast_high  size_gb_uncompressed
    name                                                                                                                  ...
    LADAF-2020-27_spleen_central-column_1.29um_bm05   LADAF-2020-27  spleen                central-column           1.29  ...  3823  10982         27852          30408            321.011086
    LADAF-2020-27_spleen_complete-organ_25.08um_bm05  LADAF-2020-27  spleen                complete-organ          25.08  ...  2151   1900         28069          33269             23.859322
    LADAF-2020-27_spleen_central-column_6.05um_bm05   LADAF-2020-27  spleen                central-column           6.05  ...  3791   7540          4139           7143            216.724949
    <BLANKLINE>
    [3 rows x 12 columns]

We can see that three datasets are available. They are from the same organ, with one being the full
organ dataset and two being high resolution region of interest datasets. Lets get the full organ
dataset::

    >>> import hoa_tools.dataset
    >>>
    >>> whole_spleen = hoa_tools.dataset.get_dataset('LADAF-2020-27_spleen_complete-organ_25.08um_bm05')
    >>> print(whole_spleen)
    donor='LADAF-2020-27' organ='spleen' organ_context='' roi='complete-organ' resolution=25.08 beamline='bm05' nx=2919 ny=2151 nz=1900

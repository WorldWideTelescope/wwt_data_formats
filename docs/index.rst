====================================
AAS WorldWide Telescope Data Formats
====================================

`wwt_data_formats`_ is a low-level Python package that interfaces with the
various XML serialization formats used by the AAS_ `WorldWide Telescope`_. The
documentation of this package aims to provide a comprehensive reference for
these data formats.

.. _wwt_data_formats: https://wwt-data-formats.readthedocs.io/
.. _AAS: https://aas.org/
.. _WorldWide Telescope: http://www.worldwidetelescope.org/home

The core data formats documented here are:

- :ref:`Image Sets <image-sets>`

This package also includes a CLI (command-line interface) tool, ``wwtdatatool``,
that provides some useful ways of working with various WWT data files. See the
:ref:`cli-reference` for a list of its functionality.


Detailed Table of Contents
==========================

.. toctree::
   :maxdepth: 2

   installation
   imagesets
   cli
   api


Getting help
============

If you run into any issues when using `wwt_data_formats`_, please open an
issue `on its GitHub repository
<https://github.com/WorldWideTelescope/wwt_data_formats/issues>`_.


Acknowledgments
===============

`wwt_data_formats`_ is part of the `AAS`_ `WorldWide Telescope`_ system, a
`.NET Foundation`_ project managed by the non-profit `American Astronomical
Society`_ (AAS). Work on WWT has been supported by the AAS, the US `National
Science Foundation`_ (grants 1550701_ and 1642446_), the `Gordon and Betty
Moore Foundation`_, and `Microsoft`_.

.. _.NET Foundation: https://dotnetfoundation.org/
.. _American Astronomical Society: https://aas.org/
.. _National Science Foundation: https://www.nsf.gov/
.. _1550701: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1550701
.. _1642446: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1642446
.. _Gordon and Betty Moore Foundation: https://www.moore.org/
.. _Microsoft: https://www.microsoft.com/

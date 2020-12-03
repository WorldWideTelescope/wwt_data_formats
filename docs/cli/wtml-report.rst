.. _cli-wtml-report:

===========================
``wwtdatatool wtml report``
===========================

The ``report`` subcommand analyzes an input `WTML`_ file, assumed to contain
exactly one dataset, and prints its metadata out for human vetting.

.. _WTML: https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/

This command requires that the Python package `beautifulsoup4`_ be installed.

.. _beautifulsoup4: https://www.crummy.com/software/BeautifulSoup/

Usage
=====

.. code-block:: shell

   wwtdatatool wtml report {WTML}

The ``WTML`` argument is the path to the input WTML file to be analyzed.

Example
=======

Typical usage is as straightforward as:

.. code-block:: shell

   wwtdatatool wtml report newdata/index_rel.wtml

This tool is tuned for the `Toasty`_ image-processing pipeline. It expects the
WTML file to contain one ``<Place>`` item, itself containing one
``<ForegroundImageSet>``. This tool prints out descriptive metadata, such as the
credits URL and description, but doesn’t do anything with other items such as
the astrometric data.

.. _Toasty: https://toasty.readthedocs.io/

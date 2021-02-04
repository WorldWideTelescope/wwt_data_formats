.. _cli-wtml-transfer-astrometry:

========================================
``wwtdatatool wtml transfer-astrometry``
========================================

The ``transfer-astrometry`` subcommand takes astrometric data from one `WTML`_
file and transfers them into other WTML files.

.. _WTML: https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/

The main purpose of this command is to enable a workflow for efficiently
fine-tuning image astrometry using the WWT Windows client.

Many images imported to WWT come with decent, but not excellent, astrometric
information. Sometimes the easiest way to improve the astrometry of an image is
to do so manually, using the image editing mode of the WWT Windows client. This
editing mode allows you to write out a WTML file with improved astrometry for a
batch of images. If you’re preparing an image for upload into the cloud,
however, you’re likely dealing with two sets of WTMLs: one set for local
editing, and one set for publication on the cloud. The WWT editing mode can only
rewrite the first set. This tool gives a mechanism for transferring improved
astrometry from the former to the latter.

Usage
=====

.. code-block:: shell

   wwtdatatool wtml transfer-astrometry {INPUT-WTML} {UPDATE-WTMLS...}

- The ``INPUT-WTML`` argument is the path to an input WTML file.
- The ``UPDATE-WTMLS`` argument gives the paths of one or more WTML files that
  will be updated with astrometric information from the input.

Example
=======

In typical usage, you might have a group of images being prepared for cloud
upload. Each lives in its own directory, with an ``index_rel.wtml`` file
defining the image specifications, including approximate astrometry. To refine
the astrometry manually, first you might merge the individual index files into a
master file:

.. code-block:: shell

    wwtdatatool wtml merge img*/index_rel.wtml before_rel.wtml

Then you would generate a version of the file using local disk paths, suitable for
opening in the WWT Windows client:

.. code-block:: shell

    wwtdatatool wtml rewrite-disk before_rel.wtml before_disk.wtml

Then you would open this file in the WWT Windows client, tune up the astrometry,
and save the results as, say ``after_disk.wtml``.

Finally you would use this command to transfer the improved astrometry back to
the source files:

.. code-block:: shell

    wwtdatatool wtml transfer-astrometry after_disk.wtml img*/index_rel.wtml

You’d now be ready to continue your workflow of finalizing the data for
publication and upload.

Notes
=====

This tool works by matching up imagesets and places in the input file and the
output files. This matching is done *by name*, since folder structures and URLs
might vary (as in the example above). Therefore, if there are multiple different
images with the same name, you’ll get unpredictable results. The tool will
report when it detects duplicated names in the input file.

See Also
========

- :ref:`cli-wtml-rewrite-disk`
- :ref:`cli-wtml-merge`

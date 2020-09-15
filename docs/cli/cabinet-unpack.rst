.. _cli-cabinet-unpack:

==============================
``wwtdatatool cabinet unpack``
==============================

The ``cabinet unpack`` extracts the files packed into a WWT “file cabinet”
container file. WWT data files that use the “file cabinet” format include layer
files (``.wwtl``) and tour files (``.wtt``).

Usage
=====

.. code-block:: shell

   wwtdatatool cabinet unpack {CABINET-PATH}

- The ``CABINET-PATH`` argument gives the path to the cabinet file that will be
  unpacked.

Example
=======

.. code-block:: shell

   $ wwtdatatool cabinet unpack NeedsManualFixing.WTT


Details
=======

The new files will be created in the current directory, or subdirectories
thereof.

The code that processes the paths as specified inside the cabinet file is pretty
naive. If you manually create a file with funky elements like parent-directory
refereneces (``..``) or non-ASCII file names, it is quite possible that you’ll
get weird results.

See Also
========

- :ref:`cli-cabinet-list`
- :ref:`cli-cabinet-pack`

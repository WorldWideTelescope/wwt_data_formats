.. _cli-cabinet-pack:

============================
``wwtdatatool cabinet pack``
============================

The ``cabinet pack`` creates a WWT “file cabinet” container file from a set of
input files on disk. WWT data files that use the “file cabinet” format include
layer files (``.wwtl``) and tour files (``.wtt``).

Usage
=====

.. code-block:: shell

   wwtdatatool cabinet pack {CABINET-PATH} {INPUT-PATH ...}

- The ``CABINET-PATH`` argument gives the path to the cabinet file that will be
  created.
- One or more ``INPUT-PATH`` arguments give the paths to the input files that will
  be inserted into the new cabinet file.

Example
=======

.. code-block:: shell

   $ wwtdatatool cabinet pack mytour.wtt fixedfile.wwtxml music.mp4


Details
=======

The input file paths must be relative paths and not contain any special
directory indicators like ``.`` or ``..``.

The files will be packed into the cabinet in the order in which they are
provided on the command line. For many cabinet files, the first file should be a
special XML document, so beware of using globs (``*``) to list your inputs,
since they may yield the wrong ordering.

In the current implementation, the input files are stored in memory before
writing the new cabinet file to disk. This means that this tool may be unable to
create very large (gigabytes) cabinets. This restriction is purely from
laziness, so if you need to create a large cabinet file, file an issue.

See Also
========

- :ref:`cli-cabinet-list`
- :ref:`cli-cabinet-unpack`

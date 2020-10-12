.. _cli-wtml-merge:

==========================
``wwtdatatool wtml merge``
==========================

The ``merge`` subcommand takes one or more input `WTML`_ files and combines
their contents into a new file, rewriting any `relative URLs`_ to respect the
folder structure of the input files.

.. _WTML: https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/
.. _relative URLs: https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL

Usage
=====

.. code-block:: shell

   wwtdatatool wtml merge {INPUT-WTMLS...} {OUTPUT-WTML}

- The ``INPUT-WTMLS`` argument is the path to one or more input WTML files that
  may contain relative URLs for some of their data references.
- The ``OUTPUT-WTML`` argument is the path where the merged output WTML
  file will be written.

Example
=======

In typical usage, you might have several ``index.wtml`` or ``index_rel.wtml``
files for a group of images that you wish to into a combined collection. If each
of your imagesets is located in a sub-folder, you might run a command such as:

.. code-block:: shell

   wwtdatatool wtml merge \
     image1/index_rel.wtml \
     image2/index_rel.wtml \
     image3/index_rel.wtml \
     index_rel.wtml

Each input WTML file will have its outermost folder entry “unwrapped” and merged
into the output. For instance, if ``image1/index_rel.wtml`` contains a single
imageset named "global", ``image2/index_rel.wtml`` contains a single Place named
"highlight", and ``image3/index_rel.wtml`` contains three Places named "site1",
"site2", and "site3", the merged ``index_rel.wtml`` folder will contain five
items: "global", "highlight", "site1", "site2", and "site3".

If the input file ``image1/index_rel.wtml`` references a relative URL path
``./thumb.jpg``, in the output file the URL path will be rewritten to have the
form ``image1/thumb.jpg``. This URL structure is determined from the layout of
the input WTML files on disk, and not on their logical folder structure. For
instance, if you have inputs configured to run a command such as this:

.. code-block:: shell

   wwtdatatool wtml merge folder1/index.wtml folder2/output.wtml

The relative URLs in ``folder2/output.wtml`` will be rewritten to start with
``../folder1/``.

See Also
========

- :ref:`cli-wtml-rewrite-urls`

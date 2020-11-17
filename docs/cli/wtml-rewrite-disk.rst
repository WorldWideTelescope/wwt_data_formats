.. _cli-wtml-rewrite-disk:

=================================
``wwtdatatool wtml rewrite-disk``
=================================

The ``rewrite-disk`` subcommand takes a template `WTML`_ file populated with
`relative URLs`_ and writes out a new file in which they have been changed to
absolute paths on the local disk. Such a file is useful because it can be opened
in the WWT desktop application.

.. _WTML: https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/
.. _relative URLs: https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL

Usage
=====

.. code-block:: shell

   wwtdatatool wtml rewrite-disk {INPUT-WTML} {OUTPUT-WTML}

- The ``INPUT-WTML`` argument is the path to an input WTML file that may contain
  relative disk for some of its data references.
- The ``OUTPUT-WTML`` argument is the path where the modified output WTML
  file will be written.

Example
=======

In typical usage, it is expected that you’re preparing a data set for
use in WWT. Using a tool like `toasty`_, you’ve created data files and a WTML
file named ``index_rel.wtml`` describing them. This file contains relative data
URLs, which are useful for data preparation but not allowed by the WWT apps. To
test your WTML by opening it in the Windows app, you might run:

.. code-block:: shell

   wwtdatatool wtml rewrite-disk index_rel.wtml local.wtml

Then you’d open ``local.wtml`` in the WWT desktop application to see how your
data look.

.. _toasty: https://toasty.readthedocs.io/

See Also
========

- :ref:`cli-serve`

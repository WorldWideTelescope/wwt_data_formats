.. _cli-preview:

=======================
``wwtdatatool preview``
=======================

The ``preview`` command allows you to preview a draft `WTML`_ file by opening it
up in a browser window with the `WWT webclient`_. The file and its associated
data sets are made accessible to the webclient through an embedded HTTP server.

.. _WTML: https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/
.. _WWT webclient: https://worldwidetelescope.org/webclient/

Usage
=====

.. code-block:: shell

   wwtdatatool preview {WTML}

The ``WTML`` argument is the path of a WTML file. This may be an
``index_rel.wtml`` file, containing relative URLs, or a regular WTML file
containing only absolute URLs.

Details
=======

This command runs the same kind of local HTTP server as described in the
documentation for the :ref:`cli-serve` command.

See Also
========

- :ref:`cli-serve`
- :ref:`cli-wtml-rewrite-urls`

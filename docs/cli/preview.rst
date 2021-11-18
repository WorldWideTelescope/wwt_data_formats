.. _cli-preview:

=======================
``wwtdatatool preview``
=======================

The ``preview`` command allows you to preview a draft `WTML`_ file by opening it
up in a browser window with the `WWT webclient`_ or the `WWT research app`_. The
file and its associated data sets are made accessible to the webclient through
an embedded HTTP server.

.. _WTML: https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/
.. _WWT webclient: https://worldwidetelescope.org/webclient/
.. _WWT research app: https://docs.worldwidetelescope.org/research-app/latest/

Usage
=====

.. code-block:: shell

   wwtdatatool preview
      [--research] [-r]
      [-b BROWSER] [--browser BROWSER]
      [--appurl URL]
      {WTML}

The ``WTML`` argument is the path of a WTML file. This may be an
``index_rel.wtml`` file, containing relative URLs, or a regular WTML file
containing only absolute URLs.

If the ``-r`` or ``--research`` option is supplied, the file is previewed using
the WWT research app. By default, the WWT webclient is used.

The ``-b`` or ``--browser`` option specifies which web browser to use, using an
identifier as understood by the `Python "webbrowser" module`_. Typical choices
might be ``firefox``, ``safari``, or ``google-chrome``. If unspecified, a
sensible default will be used.

.. _Python "webbrowser" module: https://docs.python.org/3/library/webbrowser.html

The ``--appurl`` option can be used to override the base URL for the preview app
that will be used. This can be helpful when developing new features in one of
these apps.

Example
=======

After tiling an image with `toasty`_ into a directory named ``tiled``, preview
the tiled data:

.. _toasty: https://toasty.readthedocs.io/

.. code-block:: shell

   wwtdatatool preview tiled/index_rel.wtml


Details
=======

This command runs the same kind of local HTTP server as described in the
documentation for the :ref:`cli-serve` command.

See Also
========

- :ref:`cli-serve`
- :ref:`cli-wtml-rewrite-urls`

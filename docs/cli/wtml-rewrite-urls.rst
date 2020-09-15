.. _cli-wtml-rewrite-urls:

=================================
``wwtdatatool wtml rewrite-urls``
=================================

The ``rewrite-urls`` subcommand takes a template `WTML`_ file populated with
`relative URLs`_ and writes out a new file in which they have been changed to
absolute URLs.

.. _WTML: https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/
.. _relative URLs: https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL

Usage
=====

.. code-block:: shell

   wwtdatatool wtml rewrite-urls {INPUT-WTML} {BASE-URL} {OUTPUT-WTML}

- The ``INPUT-WTML`` argument is the path to an input WTML file that may contain
  relative URLs for some of its data references.
- The ``BASE-URL`` argument specifies the base URL that those relative URLs will
  be combined with to form absolute URLs (using `urllib.parse.urljoin`_).
- The ``OUTPUT-WTML`` argument is the path where the absolute-ized output WTML
  file will be written.

.. _urllib.parse.urljoin: https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin

Example
=======

In typical usage, it is expected that you are preparing a data set for
publication. Using a tool like `toasty`_, you have created data files and a WTML
file named ``index_rel.wtml`` describing them. This file contains relative data
URLs, which are useful but not allowed in published WTML files. When you’re
ready to publish, you have to choose the final URL at which the data will be
made available; let’s say that it will be
``http://data1.wwtassets.org/packages/2020/07_phat_m31/``. To write out the final
WTML, you’d run:

.. code-block:: shell

   wwtdatatool wtml rewrite-urls \
     index_rel.wtml \
     http://data1.wwtassets.org/packages/2020/07_phat_m31/ \
     index.wtml

Then you would upload all of your data, ideally including both the
``index_rel.wtml`` and the ``index.wtml`` file, to the data server. In the end
it should be true that people will be able to download your index file from the
URL `<http://data1.wwtassets.org/packages/2020/07_phat_m31/index.wtml>`_.

Note that ``BASE-URL`` should always use ``http://`` as its protocol, not
``https://``. The WWT web client will rewrite HTTP URLs to HTTPS if needed, but
the Windows client will get confused if you give it HTTPS.

.. _toasty: https://toasty.readthedocs.io/

See Also
========

- :ref:`cli-serve`

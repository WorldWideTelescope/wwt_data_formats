.. _cli-serve:

=====================
``wwtdatatool serve``
=====================

The ``serve`` command starts a local HTTP server that allows you to preview a
draft `WTML`_ file in WWT.

.. _WTML: https://docs.worldwidetelescope.org/data-guide/1/data-file-formats/collections/

Usage
=====

.. code-block:: shell

   wwtdatatool serve [--port PORT] {PATH}

- The ``PATH`` argument specifies the directory that will be used as the root
  for the files in the server
- The optional ``--port PORT`` argument allows you to specify the specific port
  at which the server will listen for connections

Details
=======

The HTTP server launched by this command is mostly a standard, fairly dumb
static file server. If it receives an HTTP request for the path ``/foo/bar``, it
will search for a file at the path ``PATH/foo/bar`` and serve up its contents.
It is powered by the Python `http.server`_ class.

.. _http.server: https://docs.python.org/3/library/http.server.html

However, the server specially handles WTML files. If a request is received for
an HTTP path ending in the form ``.../{basename}.wtml``, *and* there exists a
file on disk named ``.../{basename}_rel.wtml``, special logic is triggered. The
WTML content will be loaded and reprocessed so that any `relative URLs`_ in the
content will be converted to absolute URLs appropriate for the HTTP server. This
supports the recommended workflow where you prepare WTML content in a file
containing relative URLs, then use :ref:`cli-wtml-rewrite-urls` to create files
with the needed absolute URLs just before publishing them.

.. _relative URLs: https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL

Furthermore, the server also supplies globally open `CORS`_ headers so that the
data it returns are not blocked from the WWT web client by web browser security
protocols.

.. _CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

When the server starts up, it will print out its base URL and the URLs of any
“relative” WTML files it detects in its root directory. These URLs can be
copy-pasted into the WWT web client for easy prototyping.

Be aware that your web browser will cache content between multiple invocations
of the ``wwtdatatool serve`` command even if the data that you are serving have
changed. You may need to force your browser to reload new content to get updated
data. A quick way to avoid this issue is to launch the server using a new
``--port`` number.

See Also
========

- :ref:`cli-preview`
- :ref:`cli-wtml-rewrite-urls`

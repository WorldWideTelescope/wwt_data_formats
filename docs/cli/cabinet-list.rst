.. _cli-cabinet-list:

============================
``wwtdatatool cabinet list``
============================

The ``cabinet list`` prints out the contents of a WWT “file cabinet” container
file, which includes layer files (``.wwtl``) and tour files (``.wtt``).

Usage
=====

.. code-block:: shell

   wwtdatatool cabinet list {PATH}

- The ``PATH`` argument gives the path to the cabinet file.

Example
=======

.. code-block:: shell

   $ wwtdatatool cabinet list mytour.wtt
   Saturn Pack - August 2020.wwtxml
   90bdf9fd-9fc5-4967-9037-b35dd9020036\1cf8cf6d-db6a-4519-9688-3370d36543dd.thumb.png
   90bdf9fd-9fc5-4967-9037-b35dd9020036\f96b4b62-02a2-4a70-bdb2-6b0362ff761d.mp3
   90bdf9fd-9fc5-4967-9037-b35dd9020036\769e4fc6-bd50-43b1-b795-8071310bc2a2.thumb.png
   ...

Details
=======

The file names are printed out one per line. The directory separator is a
Windows-style backslash, ``\``.

See Also
========

- :ref:`cli-cabinet-pack`
- :ref:`cli-cabinet-unpack`

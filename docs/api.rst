=============
API Reference
=============

..
   Working around https://github.com/astropy/sphinx-automodapi/issues/132 : Our
   API docs were missing members for classes like ImageSet due to an esoteric
   bug related to ABCs (June 2021, sphinx-automodapi 0.13). Work around by
   forcing `:inherited-members:`, and do it everywhere to avoid any oversights.

.. automodapi:: wwt_data_formats
   :inheritance-diagram:
   :inherited-members:

.. automodapi:: wwt_data_formats.abcs
   :no-inheritance-diagram:
   :inherited-members:

.. automodapi:: wwt_data_formats.cli
   :no-inheritance-diagram:
   :no-inherited-members:

.. automodapi:: wwt_data_formats.enums
   :no-inheritance-diagram:
   :inherited-members:

.. automodapi:: wwt_data_formats.filecabinet
   :no-inheritance-diagram:
   :inherited-members:

.. automodapi:: wwt_data_formats.folder
   :no-inheritance-diagram:
   :inherited-members:

.. automodapi:: wwt_data_formats.imageset
   :no-inheritance-diagram:
   :inherited-members:

.. automodapi:: wwt_data_formats.layers
   :no-inheritance-diagram:
   :inherited-members:

.. automodapi:: wwt_data_formats.place
   :no-inheritance-diagram:
   :inherited-members:

.. automodapi:: wwt_data_formats.server
   :no-inheritance-diagram:
   :inherited-members:

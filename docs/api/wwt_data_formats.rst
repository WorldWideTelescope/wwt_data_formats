..
   Working around https://github.com/astropy/sphinx-automodapi/issues/132 : Our
   API docs were missing members for classes like ImageSet due to an esoteric
   bug related to ABCs (June 2021, sphinx-automodapi 0.13). Work around by
   forcing `:inherited-members:`, and do it liberally to avoid any oversights.

.. automodapi:: wwt_data_formats
   :no-inheritance-diagram:
   :inherited-members:

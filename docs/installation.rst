===========================
Installing wwt_data_formats
===========================

Installing wwt_data_formats with pip
====================================

You can install the latest release of ``wwt_data_formats`` using pip_::

  pip install wwt_data_formats

.. _pip: https://pip.pypa.io/en/stable/


Dependencies
============

If you install ``wwt_data_formats`` using pip_ as described above, any
required dependencies will get installed automatically. The `README in the Git
repository`_ lists the current dependencies if you would like to see an
explict list.

.. _README in the Git repository: https://github.com/WorldWideTelescope/wwt_data_formats/#readme


Installing the developer version
================================

If you want to use the very latest developer version, you should clone `this
repository <https://github.com/WorldWideTelescope/wwt_data_formats/>`_ and manually
install the package in “editable” mode::

  git clone https://github.com/WorldWideTelescope/wwt_data_formats.git
  cd wwt_data_formats
  pip install -e .

You can run the test suite with the command::

  pytest wwt_data_formats

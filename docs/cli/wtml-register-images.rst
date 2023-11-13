.. _cli-wtml-register-images:

====================================
``wwtdatatool wtml register-images``
====================================

The ``register-images`` subcommand iterates over all of the imagesets defined in
a WTML file and registers them with the WWT Constellations system.

This command requires that the `wwt-api-client`_ Python package is installed.

.. _wwt-api-client: https://wwt-api-client.readthedocs.io/

Usage
=====

.. code-block:: shell

   wwtdatatool wtml register-images
     --handle {HANDLE} 
     --copyright {COPYRIGHT}
     --license-id {LICENSE-ID}
     {WTML}

The ``WTML`` argument is the path to the input WTML file containing the
imageset(s) to register. The images must have been uploaded somewhere accessible
on the general web — do *not* run this command with an ``index_rel.wtml`` file!

The ``HANDLE`` argument is the Constellations “handle” that will own the images.
The Constellations login used by the ``wwt_api_client`` package needs to have
sufficient permissions to create images attached to the handle. (If you are
using the API programmatically for the first time, it will print a magic URL
that you will use to log in to your account, setting up the linkage.)

The ``COPYRIGHT`` argument is the copyright statement that will be attached to
the images. It can be edited after-the-fact if needed. Preferred form is along
the lines of “Copyright 2020 Henrietta Swan Leavitt” or “Public domain”. Note
that the correct information for this field *cannot* be determined
algorithmically. Note also that under the world’s current regime of intellectual
property law, virtually every single image in WWT can be presumed to be
copyrighted, with the major exception of images produced by employees of the US
Federal government in the course of their duties (e.g., NASA images).

The ``LICENSE-ID`` argument gives the `SPDX License Identifier`_ of the license
under which this image is made available through WWT. Use ``CC-PDDC`` for images
in the public domain. For images with known licenses that are not in the SPDX
list, use ``LicenseRef-$TEXT`` for some value of ``$TEXT``. The WWT validation
code recognizes ``LicenseRef-None`` for “All rights reserved” and
``LicenseRef-WWT`` for images in the legacy WWT corpus.

.. _SPDX License Identifier: https://spdx.org/licenses/


Example
=======

Typical usage for a JWST image might look like

.. code-block:: shell

   wwtdatatool wtml register-images
     --handle jwst
     --copyright "Public Domain"
     --license-id CC-PDDC
     jwst_batch.wtml

Once the images are added, you can use the Constellations UI to create “scenes”
displaying them.
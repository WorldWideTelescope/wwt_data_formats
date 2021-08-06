.. _image-sets:

==============
WWT Image Sets
==============

Images in the AAS WorldWide Telescope can come in a variety of formats:

- Standard bitmapped images like PNG or JPG files
- Scientific data in FITS files
- Large-size images converted into tile pyramids

Such images are described as ``<ImageSet>`` XML fragments in several of the WWT
file formats. In this package, the corresponding data structure is
:class:`wwt_data_formats.imageset.ImageSet`. Read the class documentation for
detailed explanations of the different imageset parameters.

The high-level structure of a standard, minimal WTML file to show a single image is:

.. code-block::

   <Folder ...>
      <Place ...>
        <ForegroundImageSet ...>
          <ImageSet ...>
            ...
          </ImageSet>
        </ForegroundImageSet>
      </Place>
   </Folder>

The corresponding code using ``wwt_data_formats`` is::

    from wwt_data_formats import folder, place, imageset

    f = folder.Folder()
    pl = place.Place()
    imgset = imageset.ImageSet()

    pl.foreground_image_set = imgset
    f.children = [pl]

This can then be written to XML with::

    from wwt_data_formats import write_xml_doc

    with open('myfile.wtml', 'wt', encoding='utf8') as f:
        write_xml_doc(f.to_xml(), dest_stream=f)

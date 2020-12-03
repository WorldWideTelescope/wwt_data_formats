# wwt_data_formats 0.7.0 (2020-12-03)

- Add a `wwtdatatool wtml report` command to report on the metadata contents
  of single-dataset WTML files. This is a bit of a hack intended for use in
  Toasty pipelines, but it might become more general.
- Improve support for open-ended annotation attributes in datasets.
  Specifically, add `Annotation` and `Description` in places, and note that
  `Description` in ImageSets isn't wired up in the apps and so should be
  avoided.
- Fix calculation of image centers when setting up WWT metadata based on a
  WCS data structure. I had the X and Y swapped, like a chump.


# wwt_data_formats 0.6.0 (2020-11-17)

- Add `wwtdatatool wtml rewrite-disk` to transform a "relative" WTML file to one
  containing on-disk file paths, to ease testing with the Windows desktop app.
- Fix XML files created on Windows to be sure that they specify UTF-8 encoding,
  not CP-1252.


# wwt_data_formats 0.5.0 (2020-10-12)

- Add a `wwtdatatool wtml merge` subcommand to ease the creation of "index" WTML
  files from single-dataset WTMLs.


# wwt_data_formats 0.4.6 (2020-10-05)

- Try to always read and write files with UTF-8 encoding, accepting Windows Byte
  Order Markers (BOMs) when present.


# wwt_data_formats 0.4.5 (2020-10-01)

- Wire up the AltUrl property of ImageSets
- In the CLI, group WTML tree commands under `tree` subcommand
- Report AltUrls in `tree print-image-urls`
- Add `tree print-dem-urls`


# wwt_data_formats 0.4.4 (2020-09-28)

- Still no code changes from 0.4.2-0.4.3. Attempting to fix automated upload to
  PyPI.


# wwt_data_formats 0.4.3 (2020-09-28)

- No code changes from 0.4.2. Attempting to fix automated upload to PyPI.


# wwt_data_formats 0.4.2 (2020-09-28)

- Convert to Cranko for release automation! And Codecov.io for coverage
  reporting, and Azure Pipelines for CI.
- HTTP hacks to try to get the server test to succeed reliably on CI.


# 0.4.1 (2020-Sep-18)

- Fix the test suite on Windows (hopefully).


# 0.4.0 (2020-Sep-15)

- Add a bunch of CLI documentation.
- No code changes.


# 0.3.0 (2020-Jul-30)

- Add `wwtdatatool serve` to locally serve WTML files with on-the-fly URL
  rewriting.
- Add `wwtdatatool wtml rewrite-urls` to allow you to take a WTML file with
  relative URLs and convert them into absolute ones.
- `wwtdatatool cabinet unpack`: copy with cabinet files whose paths begin with a
  leading slash (as in the default WWT installer `datafiles.cabinet` file).
- In `wwt_data_formats.layers`, support WWTL files where the data assets are not
  necessarily placed in a subdirectory named for the layer ID (observed in the
  wild).
- In `wwt_data_formats.imageset`, copy with WCS PC matrices that have non-unity
  determinants (also observed in the wild).


# 0.2.0 (2020-Jun-17)

- Clarify that the `requests` package is now always required.
- Add `wwt_data_formats.layers` for dealing with WWTL layer-export files.


# 0.1.3 (2020-Jun-06)

- Add a CLI tool, `wwtdatatool`, to provide interfaces to certain low-level
  operations
- Add some infrastructure to support walking of trees of folders with on-the-fly
  downloads as needed.
- Support the Imageset::reference_frame attribute
- Support Communities metadata
- Fix the test suite for Python 3.8


# 0.1.2 (2020-Mar-20)

- Fix roundtripping of imagesets with a non-empty QuadTreeMap, and add a few
  more attributes on the `<ImageSet>` type.
- Fix loading of XML files missing attributes that we expected to see.
- Allow "Tangent" as an alias for "Tan" when deserializing ProjectionType
  enums.
- Add `to_xml_string()` and `write_xml()` convenience methods on the
  LockedXmlTraits class that's a base class for most of our data types.


# 0.1.1 (2020-Mar-17)

- Fix `wwt_data_formats.imageset.ImageSet.set_position_from_wcs()` for the new
  metadata scheme.


# 0.1.0 (2020-Mar-17)

- Massive infrastructure rebuild. We now use traitlets and have a framework
  for XML serialization, rather than a bunch of boilerplate code. We can
  now deserialize folders and their contents.


# 0.0.2 (2020-Feb-05)

- Document the FileCabinet support
- Work with FITS files that have `CDELT{1,2}` but not `PC1_1` and `PC2_2`.
- Removed Python 2.7 from the CI.


# 0.0.1 (2019-Dec-04)

- First version

[![Build Status](https://dev.azure.com/aasworldwidetelescope/WWT/_apis/build/status/WorldWideTelescope.wwt_data_formats?branchName=master)](https://dev.azure.com/aasworldwidetelescope/WWT/_build/latest?definitionId=22&branchName=master)
[![PyPI version](https://badge.fury.io/py/wwt-data-formats.svg)](https://badge.fury.io/py/wwt-data-formats)
[![codecov](https://codecov.io/gh/WorldWideTelescope/wwt_data_formats/branch/master/graph/badge.svg?token=4no5LD8Sed)](https://codecov.io/gh/WorldWideTelescope/wwt_data_formats)

# WWT Data Formats

<!--pypi-begin-->
[wwt_data_formats] is a low-level Python package that interfaces with the
various XML serialization formats used by [WorldWide Telescope].

[wwt_data_formats]: https://wwt-data-formats.readthedocs.io/
[WorldWide Telescope]: https://worldwidetelescope.org/
<!--pypi-end-->

[//]: # (numfocus-fiscal-sponsor-attribution)

The WorldWide Telescope project uses an [open governance
model](https://worldwidetelescope.org/about/governance/) and is fiscally
sponsored by [NumFOCUS](https://numfocus.org/). Consider making a
[tax-deductible donation](https://numfocus.org/donate-for-worldwide-telescope)
to help the project pay for developer time, professional services, travel,
workshops, and a variety of other needs.

<div align="center">
  <a href="https://numfocus.org/donate-for-worldwide-telescope">
    <img height="60px"
         src="https://raw.githubusercontent.com/numfocus/templates/master/images/numfocus-logo.png">
  </a>
</div>


## Installation

The easiest way to install [wwt_data_formats] is through [pip]:

```
pip install wwt_data_formats
```

[pip]: https://pip.pypa.io/


## Documentation, Examples, etc.

For documentation and examples, go to:

https://wwt-data-formats.readthedocs.io/


## Contributions

Contributions to [wwt_data_formats] are welcome! See
[the WorldWide Telescope contributors’ guide] for applicable information. We
use a standard workflow with issues and pull requests. All participants in
[wwt_data_formats] and the WWT communities must abide by the
[WWT Code of Conduct].

[the WorldWide Telescope contributors’ guide]: https://worldwidetelescope.github.io/contributing/
[WWT Code of Conduct]: https://worldwidetelescope.github.io/code-of-conduct/


## Release History

Releases of [wwt_data_formats] are logged in the file
[CHANGELOG.md](https://github.com/WorldWideTelescope/wwt_data_formats/blob/release/CHANGELOG.md)
on the `release` branch of this repository, as well as release listings
maintained by
[GitHub](https://github.com/WorldWideTelescope/wwt_data_formats/releases) and
[PyPI](https://pypi.org/project/wwt_data_formats/#history).


## Dependencies

[wwt_data_formats] is a Python package so, yes, Python is required.

- [astropy] is not a required dependency, but can be used
- [beautifulsoup4] for the `wwtdatatool wtml report` command
- [pytest] to run the test suite
- [requests] is always required (in princple it could be optional)
- [traitlets] is always required

[astropy]: https://www.astropy.org/
[beautifulsoup4]: https://www.crummy.com/software/BeautifulSoup/
[pytest]: https://docs.pytest.org/
[requests]: https://requests.readthedocs.io/
[traitlets]: https://traitlets.readthedocs.io/


## Legalities

[wwt_data_formats] is copyright the .NET Foundation. It is licensed under the
[MIT License](./LICENSE).


## Acknowledgments

[wwt_data_formats] is part of the WorldWide Telescope system, a [.NET
Foundation] project. Work on WWT has been supported by the [American
Astronomical Society] (AAS), the US [National Science Foundation] (grants
[1550701], [1642446], and [2004840]), the [Gordon and Betty Moore Foundation], and
[Microsoft].

[.NET Foundation]: https://dotnetfoundation.org/
[American Astronomical Society]: https://aas.org/
[National Science Foundation]: https://www.nsf.gov/
[1550701]: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1550701
[1642446]: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1642446
[2004840]: https://www.nsf.gov/awardsearch/showAward?AWD_ID=2004840
[Gordon and Betty Moore Foundation]: https://www.moore.org/
[Microsoft]: https://www.microsoft.com/

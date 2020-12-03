[![Build Status](https://dev.azure.com/aasworldwidetelescope/WWT/_apis/build/status/WorldWideTelescope.wwt_data_formats?branchName=master)](https://dev.azure.com/aasworldwidetelescope/WWT/_build/latest?definitionId=22&branchName=master)
[![PyPI version](https://badge.fury.io/py/wwt-data-formats.svg)](https://badge.fury.io/py/wwt-data-formats)
[![codecov](https://codecov.io/gh/WorldWideTelescope/wwt_data_formats/branch/master/graph/badge.svg?token=4no5LD8Sed)](https://codecov.io/gh/WorldWideTelescope/wwt_data_formats)

# WWT Data Formats

<!--pypi-begin-->
[wwt_data_formats] is a low-level Python package that
interfaces with the various XML serialization formats used by the [AAS]
[WorldWide Telescope].

[wwt_data_formats]: https://wwt-data-formats.readthedocs.io/
[AAS]: https://aas.org/
[WorldWide Telescope]: http://www.worldwidetelescope.org/
<!--pypi-end-->


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

[wwt_data_formats] is part of the AAS WorldWide Telescope system, a [.NET Foundation]
project managed by the non-profit [American Astronomical Society] (AAS). Work
on WWT has been supported by the AAS, the US [National Science Foundation]
(grants [1550701] and [1642446]), the [Gordon and Betty Moore Foundation], and
[Microsoft].

[.NET Foundation]: https://dotnetfoundation.org/
[American Astronomical Society]: https://aas.org/
[National Science Foundation]: https://www.nsf.gov/
[1550701]: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1550701
[1642446]: https://www.nsf.gov/awardsearch/showAward?AWD_ID=1642446
[Gordon and Betty Moore Foundation]: https://www.moore.org/
[Microsoft]: https://www.microsoft.com/

# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License

from __future__ import absolute_import, division, print_function

import os
from setuptools import setup, Extension

def get_long_desc():
    in_preamble = True
    lines = []

    with open('README.md', 'rt', encoding='utf8') as f:
        for line in f:
            if in_preamble:
                if line.startswith('<!--pypi-begin-->'):
                    in_preamble = False
            else:
                if line.startswith('<!--pypi-end-->'):
                    break
                else:
                    lines.append(line)

    lines.append('''

For more information, including installation instructions, please visit [the
project homepage].

[the project homepage]: https://wwt-data-formats.readthedocs.io/
''')
    return ''.join(lines)


setup_args = dict(
    name = 'wwt_data_formats',  # cranko project-name
    version = '0.6.0',  # cranko project-version
    description = 'Low-level interface to AAS WorldWide Telescope data formats',
    long_description = get_long_desc(),
    long_description_content_type = 'text/markdown',
    url = 'https://wwt-data-formats.readthedocs.io/',
    license = 'MIT',
    platforms = 'Linux, Mac OS X',

    author = 'AAS WorldWide Telescope Team',
    author_email = 'wwt@aas.org',

    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Visualization',
    ],

    packages = [
        'wwt_data_formats',
        'wwt_data_formats.tests',
    ],
    include_package_data = True,

    entry_points = {
        'console_scripts': [
            'wwtdatatool=wwt_data_formats.cli:entrypoint',
        ],
    },

    install_requires = [
        'requests',
        'traitlets',
    ],

    extras_require = {
        'test': [
            'mock',
            'pytest-cov',
        ],
        'docs': [
            'astropy-sphinx-theme',
            'numpydoc',
            'sphinx',
            'sphinx-automodapi',
        ],
    },
)

if __name__ == '__main__':
    setup(**setup_args)

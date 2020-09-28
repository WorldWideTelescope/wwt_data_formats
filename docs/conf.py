# -*- coding: utf-8 -*-

project = 'wwt_data_formats'
author = 'The AAS WorldWide Telescope Team'
copyright = '2019-2020 the .NET Foundation'

release = '0.dev0'  # cranko project-version
version = '.'.join(release.split('.')[:2])

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx_automodapi.automodapi',
    'sphinx_automodapi.smart_resolver',
    'numpydoc',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'bootstrap-astropy'
html_theme_options = {
    'logotext1': 'wwt_data_formats',
    'logotext2': '',
    'logotext3': ':docs',
    'astropy_project_menubar': False,
}
html_static_path = ['_static']
htmlhelp_basename = 'wwtdataformatsdoc'

intersphinx_mapping = {
    'python': (
        'https://docs.python.org/3/',
        (None, 'http://data.astropy.org/intersphinx/python3.inv')
    ),

    'numpy': (
        'https://docs.scipy.org/doc/numpy/',
        (None, 'http://data.astropy.org/intersphinx/numpy.inv')
    ),

    'astropy': (
        'http://docs.astropy.org/en/stable/',
        None
    ),

    'requests': (
        'https://requests.readthedocs.io/en/stable/',
        None
    ),

    'traitlets': (
        'https://traitlets.readthedocs.io/en/stable/',
        None
    ),
}

numpydoc_show_class_members = False

nitpicky = True
nitpick_ignore = [
    ('py:class', 'traitlets.traitlets.MetaHasTraits'),
]

default_role = 'obj'

html_logo = 'images/logo.png'

linkcheck_retries = 5
linkcheck_timeout = 10

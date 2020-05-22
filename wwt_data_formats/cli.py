# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

"""Entrypoint for the "wwtdatatool" command-line interface.

"""
import argparse
import os.path
import sys


# General CLI utilities

def die(msg):
    print('error:', msg, file=sys.stderr)
    sys.exit(1)

def warn(msg):
    print('warning:', msg, file=sys.stderr)


# "fetch-tree" subcommand

def fetch_tree_getparser(parser):
    parser.add_argument(
        'root_url',
        metavar = 'URL',
        help = 'The URL of the initial WTML file to download.',
    )


def fetch_tree_impl(settings):
    from .folder import fetch_folder_tree

    def on_fetch(url):
        print('Fetching', url, '...')

    fetch_folder_tree(settings.root_url, '.', on_fetch)


# "print-tree-image-urls" subcommand

def print_tree_image_urls_getparser(parser):
    pass


def print_tree_image_urls_impl(settings):
    from .folder import Folder, walk_cached_folder_tree
    from .imageset import ImageSet
    from .place import Place

    done_urls = set()

    for treepath, item in walk_cached_folder_tree('.'):
        imgset = None

        if isinstance(item, ImageSet):
            imgset = item
        elif isinstance(item, Place):
            imgset = item.as_imageset()

        if imgset is None:
            continue

        if imgset.url in done_urls:
            continue

        done_urls.add(imgset.url)
        print(imgset.url, imgset.name)


# "summarize-tree" subcommand

def summarize_tree_getparser(parser):
    pass


def summarize_tree_impl(settings):
    from .folder import Folder, walk_cached_folder_tree
    from .imageset import ImageSet
    from .place import Place

    for treepath, item in walk_cached_folder_tree('.'):
        pfx = '  ' * len(treepath)

        if isinstance(item, Folder):
            print(pfx + 'Folder', item.name)
        elif isinstance(item, ImageSet):
            index = treepath[-1]
            print(f'{pfx}{index:03d}', 'ImageSet:', item.name, '@', item.url)
        elif isinstance(item, Place):
            maybe_imgset = item.as_imageset()
            if maybe_imgset is not None:
                index = treepath[-1]
                print(f'{pfx}{index:03d}', 'Place+ImgSet:', item.name, '@', maybe_imgset.url)


# The CLI driver:

def entrypoint(args=None):
    """The entrypoint for the \"wwtdatatool\" command-line interface.

    Parameters
    ----------
    args : iterable of str, or None (the default)
      The arguments on the command line. The first argument should be
      a subcommand name or global option; there is no ``argv[0]``
      parameter.

    """
    # Set up the subcommands from globals()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    commands = set()

    for py_name, value in globals().items():
        if py_name.endswith('_getparser'):
            cmd_name = py_name[:-10].replace('_', '-')
            subparser = subparsers.add_parser(cmd_name)
            value(subparser)
            commands.add(cmd_name)

    # What did we get?

    settings = parser.parse_args(args)

    if settings.subcommand is None:
        print('Run me with --help for help. Allowed subcommands are:')
        print()
        for cmd in sorted(commands):
            print('   ', cmd)
        return

    py_name = settings.subcommand.replace('-', '_')

    impl = globals().get(py_name + '_impl')
    if impl is None:
        die('no such subcommand "{}"'.format(settings.subcommand))

    # OK to go!

    impl(settings)

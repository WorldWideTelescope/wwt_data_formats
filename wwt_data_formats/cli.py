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


# "cabinet" subcommand

def cabinet_getparser(parser):
    subparsers = parser.add_subparsers(dest='cabinet_command')

    p = subparsers.add_parser('list')
    p.add_argument(
        'path',
        metavar = 'PATH',
        help = 'The path to a cabinet file.',
    )

    p = subparsers.add_parser('pack')
    p.add_argument(
        'cab_path',
        metavar = 'PATH',
        help = 'The path of the cabinet file to create.',
    )
    p.add_argument(
        'input_paths',
        nargs = '+',
        metavar = 'PATHS',
        help = 'Paths to files to put into the cabinet.',
    )

    p = subparsers.add_parser('unpack')
    p.add_argument(
        'path',
        metavar = 'PATH',
        help = 'The path to a cabinet file.',
    )


def cabinet_list(settings):
    from .filecabinet import FileCabinetReader

    with open(settings.path, 'rb') as f:
        reader =  FileCabinetReader(f)

        for fn in reader.filenames():
            print(fn)


def cabinet_pack(settings):
    from .filecabinet import FileCabinetWriter
    import os.path

    writer = FileCabinetWriter()

    for fn in settings.input_paths:
        with open(fn, 'rb') as f:
            data = f.read()

        # TODO: smarter splitting
        pieces = fn.split(os.path.sep)

        for p in pieces:
            if p in ('.', '..', ''):
                die(f'illegal input path "{fn}": must be relative with no ".", ".." components')

        writer.add_file_with_data('\\'.join(pieces), data)

    with open(settings.cab_path, 'wb') as f_out:
        writer.emit(f_out)


def cabinet_unpack(settings):
    from .filecabinet import FileCabinetReader
    from os import makedirs
    from os.path import join

    with open(settings.path, 'rb') as f_in:
        reader =  FileCabinetReader(f_in)

        for fn in reader.filenames():
            data = reader.read_file(fn)
            pieces = fn.split('\\')  # paths are Windows-style

            # At least the MakeDataCabinetFile tool creates a file whose
            # paths all begin with \. We are not gonna treat those as
            # absolute paths or anything like that.
            if not len(pieces[0]):
                pieces = pieces[1:]

            if len(pieces) > 1:
                makedirs(join(*pieces[:-1]), exist_ok=True)

            with open(join(*pieces), 'wb') as f_out:
                f_out.write(data)


def cabinet_impl(settings):
    if settings.cabinet_command is None:
        print('Run the "cabinet" command with `--help` for help on its subcommands')
        return

    if settings.cabinet_command == 'list':
        return cabinet_list(settings)
    elif settings.cabinet_command == 'pack':
        return cabinet_pack(settings)
    elif settings.cabinet_command == 'unpack':
        return cabinet_unpack(settings)
    else:
        die('unrecognized "cabinet" subcommand ' + settings.cabinet_command)


# "serve" subcommand

def serve_getparser(parser):
    parser.add_argument(
        '--port',
        '-p',
        metavar = 'PORT',
        type = int,
        default = 8080,
        help = 'The port on which to listen for connections.'
    )
    parser.add_argument(
        'root_dir',
        metavar = 'PATH',
        default = '.',
        help = 'The path to the base directory of the server.',
    )


def serve_impl(settings):
    from .server import run_server
    run_server(settings)


# "tree" subcommand

def tree_getparser(parser):
    subparsers = parser.add_subparsers(dest='tree_command')

    p = subparsers.add_parser('fetch')
    p.add_argument(
        'root_url',
        metavar = 'URL',
        help = 'The URL of the initial WTML file to download.',
    )

    p = subparsers.add_parser('print-dem-urls')
    p = subparsers.add_parser('print-image-urls')
    p = subparsers.add_parser('summarize')


def tree_impl(settings):
    if settings.tree_command is None:
        print('Run the "tree" command with `--help` for help on its subcommands')
        return

    if settings.tree_command == 'fetch':
        return tree_fetch(settings)
    elif settings.tree_command == 'print-dem-urls':
        return tree_print_dem_urls(settings)
    elif settings.tree_command == 'print-image-urls':
        return tree_print_image_urls(settings)
    elif settings.tree_command == 'summarize':
        return tree_summarize(settings)
    else:
        die('unrecognized "tree" subcommand ' + settings.tree_command)


def tree_fetch(settings):
    from .folder import fetch_folder_tree

    def on_fetch(url):
        print('Fetching', url, '...')

    fetch_folder_tree(settings.root_url, '.', on_fetch)


def tree_print_dem_urls(settings):
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

        if not imgset.dem_url or imgset.dem_url in done_urls:
            continue

        done_urls.add(imgset.dem_url)
        print(imgset.dem_url, imgset.name)


def tree_print_image_urls(settings):
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

        for url, tag in zip((imgset.url, imgset.alt_url), ('', ' (alt)')):
            if not url or url in done_urls:
                continue

            done_urls.add(url)
            print(url, imgset.name + tag)


def tree_summarize(settings):
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


# "wtml" subcommand

def wtml_getparser(parser):
    subparsers = parser.add_subparsers(dest='wtml_command')

    p = subparsers.add_parser('merge')
    p.add_argument(
        '--merged-name',
        default = 'Folder',
        help = 'The name to give to the merged folder.',
    )
    p.add_argument(
        '--merged-thumb-url',
        default = '',
        help = 'The thumbnail URL to give to the merged folder.',
    )
    p.add_argument(
        'in_paths',
        nargs = '+',
        metavar = 'IN-WTML-PATH',
        help = 'The path to the input WTML files.',
    )
    p.add_argument(
        'out_path',
        metavar = 'OUT-WTML-PATH',
        help = 'The path to the output WTML file.',
    )

    p = subparsers.add_parser('rewrite-disk')
    p.add_argument(
        'in_path',
        metavar = 'INPUT-WTML',
        help = 'The path to the input WTML file.',
    )
    p.add_argument(
        'out_path',
        metavar = 'OUTPUT-WTML',
        help = 'The path of the rewritten, output WTML file.',
    )

    p = subparsers.add_parser('rewrite-urls')
    p.add_argument(
        'in_path',
        metavar = 'INPUT-WTML',
        help = 'The path to the input WTML file.',
    )
    p.add_argument(
        'baseurl',
        metavar = 'BASE-URL',
        help = 'The new base URL to use in the file\'s contents',
    )
    p.add_argument(
        'out_path',
        metavar = 'OUTPUT-WTML',
        help = 'The path of the rewritten, output WTML file.',
    )


def wtml_impl(settings):
    if settings.wtml_command is None:
        print('Run the "wtml" command with `--help` for help on its subcommands')
        return

    if settings.wtml_command == 'merge':
        return wtml_merge(settings)
    elif settings.wtml_command == 'rewrite-disk':
        return wtml_rewrite_disk(settings)
    elif settings.wtml_command == 'rewrite-urls':
        return wtml_rewrite_urls(settings)
    else:
        die('unrecognized "wtml" subcommand ' + settings.wtml_command)


def wtml_merge(settings):
    from urllib.parse import urljoin, urlsplit
    from .folder import Folder

    out_folder = Folder()
    out_folder.name = settings.merged_name
    out_folder.thumbnail = settings.merged_thumb_url

    rel_base = os.path.dirname(settings.out_path)

    for path in settings.in_paths:
        in_folder = Folder.from_file(path)
        cur_base_url = path.replace(os.path.sep, '/')

        def mutator(url):
            if not url:
                return url
            if urlsplit(url).netloc:
                return url  # this URL is absolute

            # Resolve this relative URL, using the path of the source WTML
            # as the basis.
            url = urljoin(cur_base_url, url)

            # Now go back to filesystem-path land, so that we can use relpath to
            # compute the new path relative to the merged folder file.
            rel = os.path.relpath(url.replace('/', os.path.sep), rel_base)

            # Finally, re-express that as a URL
            return rel.replace(os.path.sep, '/')

        in_folder.mutate_urls(mutator)
        out_folder.children += in_folder.children

    with open(settings.out_path, 'wt', encoding='utf8') as f_out:
        out_folder.write_xml(f_out)


def wtml_rewrite_disk(settings):
    from .folder import Folder, make_filesystem_url_mutator

    # Note that data URLs should be relative to the *source* WTML, which is why
    # we're basing against in_path, not out_path.
    rootdir = os.path.abspath(os.path.dirname(settings.in_path))
    mutator = make_filesystem_url_mutator(rootdir)

    f = Folder.from_file(settings.in_path)
    f.mutate_urls(mutator)

    with open(settings.out_path, 'wt', encoding='utf8') as f_out:
        f.write_xml(f_out)


def wtml_rewrite_urls(settings):
    from .folder import Folder, make_absolutizing_url_mutator

    f = Folder.from_file(settings.in_path)
    f.mutate_urls(make_absolutizing_url_mutator(settings.baseurl))

    with open(settings.out_path, 'wt', encoding='utf8') as f_out:
        f.write_xml(f_out)


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

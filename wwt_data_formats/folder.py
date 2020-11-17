# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
Folder
fetch_folder_tree
make_absolutizing_url_mutator
make_filesystem_url_mutator
walk_cached_folder_tree
'''.split()

import os.path
import re
import requests
from traitlets import Bool, Instance, Int, List, Unicode, Union, UseEnum
from xml.etree import ElementTree as etree

from . import LockedXmlTraits, XmlSer
from .abcs import UrlContainer
from .enums import FolderType

class Folder(LockedXmlTraits, UrlContainer):
    """A grouping of WWT content assets.

    Children can be: places (aka "Items"), imagesets, linesets, tours,
    folders, or IThumbnail objects (to be explored).

    """
    name = Unicode('').tag(xml=XmlSer.attr('Name'))
    group = Unicode('Explorer').tag(xml=XmlSer.attr('Group'))
    url = Unicode('').tag(xml=XmlSer.attr('Url'))
    """The URL at which the full contents of this folder can be downloaded in WTML
    format.

    """
    thumbnail = Unicode('').tag(xml=XmlSer.attr('Thumbnail'))
    browseable = Bool(True).tag(xml=XmlSer.attr('Browseable'))
    searchable = Bool(True).tag(xml=XmlSer.attr('Searchable'))
    type = UseEnum(
        FolderType,
        default_value = FolderType.SKY,
    ).tag(xml=XmlSer.attr('Type'))
    sub_type = Unicode('').tag(xml=XmlSer.attr('SubType'))
    msr_community_id = Int(0).tag(xml=XmlSer.attr('MSRCommunityId'))
    """The ID number of the WWT Community that this content came from."""

    msr_component_id = Int(0).tag(xml=XmlSer.attr('MSRComponentId'))
    """The ID number of this content item on the WWT Communities system."""

    permission = Int(0).tag(xml=XmlSer.attr('Permission'))
    "TBD."

    children = List(
        trait = Union([
            Instance('wwt_data_formats.folder.Folder', args=()),
            Instance('wwt_data_formats.place.Place', args=()),
            Instance('wwt_data_formats.imageset.ImageSet', args=()),
        ]),
        default_value = ()
    ).tag(xml=XmlSer.inner_list())

    def _tag_name(self):
        return 'Folder'

    def walk(self, download=False):
        yield (0, (), self)

        for index, child in enumerate(self.children):
            if isinstance(child, Folder):
                if not len(child.children) and child.url and download:
                    url = child.url
                    child = Folder.from_url(url)
                    child.url = url
                    self.children[index] = child

                for depth, path, subchild in child.walk(download=download):
                    yield (depth + 1, (index,) + path, subchild)
            else:
                yield (1, (index,), child)

    def mutate_urls(self, mutator):
        if self.url:
            self.url = mutator(self.url)
        if self.thumbnail:
            self.thumbnail = mutator(self.thumbnail)

        for c in self.children:
            c.mutate_urls(mutator)


def make_absolutizing_url_mutator(baseurl):
    """Return a function that makes relative URLs absolute.

    Parameters
    ----------
    baseurl : string, absolute URL
        The absolute URL with which to combine relative URLs

    Returns
    -------
    A mutator function suitable for use with :meth:`wwt_data_formats.abcs.UrlContainer.mutate_urls`.

    Notes
    -----
    This function is designed for usage with :meth:`wwt_data_formats.abcs.UrlContainer.mutate_urls`.
    It returns a mutator function that can be passed to this method. The mutator will take
    relative URLs and make them absolute by combining them with the *baseurl* argument. Input URLs
    that are already absolute will be unchanged.

    """
    from urllib.parse import urljoin, urlsplit

    def mutator(url):
        if not url:
            return url
        if urlsplit(url).netloc:
            return url  # this URL is absolute
        return urljoin(baseurl, url)

    return mutator


def make_filesystem_url_mutator(basedir):
    """Return a function that converts relative URLs to filesystem paths.

    Parameters
    ----------
    basedir : string, path
        An absolute path that the relative URLs will be combined with.

    Returns
    -------
    A mutator function suitable for use with
    :meth:`wwt_data_formats.abcs.UrlContainer.mutate_urls`.

    Notes
    -----
    This function is designed for usage with
    :meth:`wwt_data_formats.abcs.UrlContainer.mutate_urls`. It returns a mutator
    function that can be passed to this method. The mutator will take relative
    URLs and convert them to filesystem paths by combining them with the
    *basedir* argument. Input URLs that are absolute will be unchanged.

    """
    from urllib.parse import unquote, urlsplit

    def mutator(url):
        if not url:
            return url

        split = urlsplit(url)
        if split.netloc:
            return url  # this URL is absolute

        # TODO: this should work with '..' but pretty much only by luck
        return os.path.join(basedir, *(unquote(s) for s in split.path.split('/')))

    return mutator


def _sanitize_name(name):
    s = re.sub('[^-_a-zA-Z0-9]+', '_', name)
    s = re.sub('^_+', '', s)
    s = re.sub('_+$', '', s)
    return s


def fetch_folder_tree(root_url, root_cache_path, on_fetch=None):
    done_urls = set()

    def get_folder(url):
        if url in done_urls:
            return None, None

        on_fetch(url)
        resp = requests.get(url)
        resp.encoding = 'utf-8-sig'  # see LockedXmlTraits.from_url()
        elem = etree.fromstring(resp.text)
        done_urls.add(url)
        return resp.text, Folder.from_xml(elem)

    root_text, root_folder = get_folder(root_url)
    with open(os.path.join(root_cache_path, 'index.wtml'), 'wt', encoding='utf8') as f:
        f.write(root_text)

    def walk(cur_folder, cur_cache_path):
        for index, child in enumerate(cur_folder.children):
            if not isinstance(child, Folder):
                continue

            text = None
            subdir_base = f'{index:03d}_{_sanitize_name(child.name)}'
            child_cache_path = os.path.join(cur_cache_path, subdir_base)

            if not len(child.children) and child.url:
                text, child = get_folder(child.url)
                if child is None:
                    continue

                os.makedirs(child_cache_path, exist_ok=True)
                with open(os.path.join(child_cache_path, 'index.wtml'), 'wt', encoding='utf8') as f:
                    f.write(text)

            walk(child, child_cache_path)

    walk(root_folder, root_cache_path)


def walk_cached_folder_tree(root_cache_path):
    seen_urls = set()

    root_folder = Folder.from_file(os.path.join(root_cache_path, 'index.wtml'))

    def walk(cur_treepath, cur_folder, cur_cache_path):
        yield (cur_treepath, cur_folder)

        for index, child in enumerate(cur_folder.children):
            child_treepath = cur_treepath + (index,)

            if not isinstance(child, Folder):
                yield (child_treepath, child)
            else:
                subdir_base = f'{index:03d}_{_sanitize_name(child.name)}'
                child_cache_path = os.path.join(cur_cache_path, subdir_base)

                if not len(child.children) and child.url:
                    if child.url in seen_urls:
                        continue

                    seen_urls.add(child.url)
                    child = Folder.from_file(os.path.join(child_cache_path, 'index.wtml'))

                for sub_treepath, sub_child in walk(child_treepath, child, child_cache_path):
                    yield (sub_treepath, sub_child)

    for info in walk((), root_folder, root_cache_path):
        yield info

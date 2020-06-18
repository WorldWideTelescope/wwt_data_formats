# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

"""Some abstract base classes (ABCs).

"""
from __future__ import absolute_import, division, print_function

__all__ = '''
UrlContainer
'''.split()

from abc import ABC, abstractmethod


class UrlContainer(ABC):
    """A data object that may contain URLs. This ABC provides a generic
    interface for mutating those URLs.

    This ABC helps establish a simple framework for walking a WWT folder structure
    and rewriting relative into absolute URLs.

    """

    @abstractmethod
    def mutate_urls(self, mutator):
        """Visit all URLs inside this container and potentially mutate them.

        Parameters
        ----------
        mutator : callable(str) -> str
            A function taking a URL string and returning a URL string.

        Notes
        -----
        For each URL inside the container, the URL is updated with the mutator's return value::

            this.some_url = mutator(this.some_url)

        If you just want to visit all of the URLs inside this container, you can write a mutator
        the returns its input unmodified.

        Implementors should not call the mutator if the URL is an optional parameter that is ``None``
        (or otherwise unset).
        """

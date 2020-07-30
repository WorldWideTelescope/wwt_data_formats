# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

from http.server import HTTPServer as HTTPServerClass
import pytest

from . import test_path
from .. import server


def test_smoke():
    """Dumb smoketest."""

    server_address = ('', 0)

    with HTTPServerClass(server_address, server.WWTRequestHandler) as httpd:
        pass

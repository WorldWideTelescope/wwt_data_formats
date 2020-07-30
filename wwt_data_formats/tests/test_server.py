# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

from argparse import Namespace
from http.server import HTTPServer
import pytest
import requests
from threading import Thread

from . import test_path
from .. import folder, server


class TestServer(object):
    @classmethod
    def setup_class(cls):
        cls.server_port = 33007 # just hope it's not taken

        settings = Namespace()
        settings.port = cls.server_port
        settings.root_dir = test_path()

        cls.thread = Thread(target=lambda: server.run_server(settings))
        cls.thread.setDaemon(True)
        cls.thread.start()

    def test_wtml_rewrite(self):
        base_url = 'http://localhost:{}/'.format(self.server_port)
        f = folder.Folder.from_url(base_url + 'test1.wtml')
        assert f.children[0].thumbnail == base_url + 'thumb.jpg'


def test_smoke():
    """Dumb smoketest."""

    server_address = ('', 0)

    with HTTPServer(server_address, server.WWTRequestHandler) as httpd:
        pass

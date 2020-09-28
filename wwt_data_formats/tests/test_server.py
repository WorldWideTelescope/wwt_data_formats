# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

from argparse import Namespace
from http.server import HTTPServer
import pytest
import requests
from threading import Thread
from time import sleep

from . import test_path
from .. import folder, server

TIMEOUT = 120

class TestServer(object):
    @classmethod
    def setup_class(cls):
        cls.server_port = 33007 # just hope it's not taken

        settings = Namespace()
        settings.port = cls.server_port
        settings.root_dir = test_path()

        # Note: there can be a race condition between server startup and the
        # execution of the tests. There doesn't seem to be any mechanism to
        # enable the tests to rigorously wait for the server to be fully started
        # up.
        cls.thread = Thread(target=lambda: server.run_server(settings))
        cls.thread.setDaemon(True)
        cls.thread.start()

        # In an attempt to help mitigate the above issue, set up requests to
        # retry requests if they fail. This is hardly expected to help since if
        # the server isn't yet running, the failures and retries will occur
        # instantly, but it's not bad to have an example of the pattern anyway.
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry
        retry_strategy = Retry(
            total=10,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        cls.session = requests.Session()
        cls.session.mount("https://", adapter)
        cls.session.mount("http://", adapter)

    def test_wtml_rewrite(self):
        base_url = 'http://localhost:{}/'.format(self.server_port)

        # More race condition mitigation
        for attempt in range(10):
            try:
                f = folder.Folder.from_url(base_url + 'test1.wtml', timeout=TIMEOUT, session=self.session)
                break
            except requests.ConnectionError:
                sleep(5)

        assert f.children[0].thumbnail == base_url + 'thumb.jpg'


def test_smoke():
    """Dumb smoketest."""

    server_address = ('', 0)

    with HTTPServer(server_address, server.WWTRequestHandler) as httpd:
        pass

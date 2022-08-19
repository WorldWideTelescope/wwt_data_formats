# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2022 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

from argparse import Namespace
from http.server import HTTPServer
import io
import os
import pytest
import requests
import sys
from threading import Thread
from time import sleep

from . import test_path
from .. import folder, server

TIMEOUT = 120


class TestRunServer(object):
    @classmethod
    def setup_class(cls):
        cls.server_port = 33007  # just hope it's not taken

        settings = Namespace()
        settings.port = cls.server_port
        settings.root_dir = test_path()
        settings.heartbeat = False

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
        base_url = "http://localhost:{}/".format(self.server_port)

        # More race condition mitigation
        for attempt in range(10):
            try:
                f = folder.Folder.from_url(
                    base_url + "test1.wtml", timeout=TIMEOUT, session=self.session
                )
                break
            except requests.ConnectionError:
                sleep(5)

        assert f.children[0].thumbnail == base_url + "thumb.jpg"


class TestPreviewWtml(object):
    """
    This is basically a smoketest to get code coverage of the preview function.
    """

    @classmethod
    def setup_class(cls):
        cls.opened_url = None

        import webbrowser

        class DummyBrowser(object):
            def open(self, url, **kwargs):
                cls.opened_url = url

        webbrowser.register("wwtdummy", DummyBrowser)

        # Note: there can be a race condition between server startup and the
        # execution of the tests. There doesn't seem to be any mechanism to
        # enable the tests to rigorously wait for the server to be fully started
        # up.
        cls.thread = Thread(
            target=lambda: server.preview_wtml(
                test_path("test1_rel.wtml"), browser="wwtdummy"
            )
        )
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

    def test_preview(self):
        for attempt in range(10):
            if self.opened_url is not None:
                break
            sleep(5)

        assert "_rel" not in self.opened_url


def test_smoke():
    """Dumb smoketest."""

    server_address = ("", 0)

    with HTTPServer(server_address, server.WWTRequestHandler) as _httpd:
        pass


@pytest.mark.skipif(os.name != "posix", reason="heartbeat test requires Unix OS")
def test_heartbeat():
    settings = Namespace()
    settings.port = 0  # we don't care
    settings.root_dir = test_path()
    settings.heartbeat = True

    read_me, write_me = os.pipe()
    pid = os.fork()

    if pid == 0:
        # Child process: run server
        os.close(read_me)
        sys.stdout = io.TextIOWrapper(os.fdopen(write_me, "wb"))
        try:
            server.run_server(settings)
        except Exception as e:
            print(e, file=sys.stderr, flush=True)
        os._exit(10)

    # Parent process: see if we can kill it by closing its stdout
    os.close(write_me)
    sleep(3)
    os.close(read_me)
    sleep(3)
    wpid, wstatus = os.waitpid(pid, os.WNOHANG)

    assert wpid == pid

    if hasattr(os, "waitstatus_to_exitcode"):
        ec = os.waitstatus_to_exitcode(wstatus)
    elif os.WIFEXITED(wstatus):
        ec = os.WEXITSTATUS(wstatus)
    else:
        ec = -1

    assert ec == 10

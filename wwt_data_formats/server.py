# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2022 the .NET Foundation
# Licensed under the MIT License.

"""
A basic HTTP server for local testing of WTML files and other WWT data products.

The key motivation for the existence of this server is that WWT WTML
"collection" files must contain absolute URLs. This means that if you're locally
testing a file, you need to include one set of (localhost) URLs, while the
production file must be different. Keeping these in sync is tedious and
error-prone.

This server is basically a generic local static-file server. But, if
specially-marked WTML files are requested, any relative URLs are rewritten
on-the-fly to be absolute relative to the server's address. That way, you can do
all of your development with the relative-URL files, and you only need to do one
substitution at the very end when the files are ready for upload to the
production server. (You can do this with ``wwtdatatool wtml rewrite-urls``.)

This module also contains some helpers for launching web browsers that can
interact with this server to display data in the WWT environment.
"""

from __future__ import absolute_import, division, print_function

__all__ = """
launch_app_for_wtml
preview_wtml
run_server
""".split()

import base64
from functools import partial
import json
import http.server
import os.path
from urllib.parse import quote as urlquote
import webbrowser

from .folder import Folder, make_absolutizing_url_mutator

try:
    from http.server import ThreadingHTTPServer as HTTPServerClass
except ImportError:
    from http.server import HTTPServer as HTTPServerClass


class WWTRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.command in ("GET", "HEAD"):
            self.send_header(
                "Access-Control-Allow-Headers",
                "Content-Disposition,Content-Encoding,Content-Type",
            )
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET,HEAD")
        return super(WWTRequestHandler, self).end_headers()

    def check_special_wtml(self):
        """
        Check whether this request is for a special synthetic WTML path, and if
        so, prep to respond to either a GET or a HEAD request. Returns a bytes
        of the response to write.

        If this request does not match a special synthetic WTML, returns None.
        """
        path = self.translate_path(self.path)

        if not path.endswith(".wtml"):
            return None

        local_wtml_path = path[:-5] + "_rel.wtml"
        if not os.path.exists(local_wtml_path):
            return None

        host = self.headers.get("Host")
        if host is None:
            host = f"{self.server.server_name}:{self.server.server_port}"
        baseurl = f"http://{host}{self.path}"
        self.log_message("special WTML: local %s, baseurl %s", local_wtml_path, baseurl)
        f = Folder.from_file(local_wtml_path)
        f.mutate_urls(make_absolutizing_url_mutator(baseurl))
        resp = f.to_xml_string().encode("utf-8")

        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", "application/x-wtml")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        return resp

    def do_GET(self):
        maybe_content = self.check_special_wtml()
        if maybe_content is not None:
            self.wfile.write(maybe_content)
            return

        return super(WWTRequestHandler, self).do_GET()

    def do_HEAD(self):
        maybe_content = self.check_special_wtml()
        if maybe_content is not None:
            return

        return super(WWTRequestHandler, self).do_HEAD()

    def log_message(self, _format, *_args):
        pass


def run_server(settings):
    """
    Settings are defined in :func:`wwt_data_formats.cli.serve_getparser`.

    """
    server_address = ("", settings.port)
    handler_factory = partial(WWTRequestHandler, directory=settings.root_dir)

    with HTTPServerClass(server_address, handler_factory) as httpd:
        # Hack: the WWT JS engine special-cases 'localhost' and '127.0.0.1' so
        # that it doesn't start trying to proxy them if URLs result in 404s,
        # which is a common occurrence when working on tiled images. So ignore
        # the auto-detected server name and use one of those.
        server_name = "127.0.0.1"  # httpd.server_name

        print(f"listening at: http://{server_name}:{httpd.server_port}/", flush=True)
        print()
        print("virtual root-directory WTML files with on-the-fly rewriting:")
        print()

        seen_any = False

        for bn in os.listdir(settings.root_dir):
            if bn.endswith("_rel.wtml"):
                virtual = bn[:-9] + ".wtml"
                print(f"    http://{server_name}:{httpd.server_port}/{virtual}")
                seen_any = True

        if not seen_any:
            print("    (none)")

        print(flush=True)

        # If/when the server is launched over SSH, it can be hard to get it to
        # shut down reliably. If it is not launched with a TTY, we don't get
        # SIGHUP, and I had a lot of trouble trying to reliably detect when
        # stdin gets closed. But what *does* seem to work reliably is getting
        # SIGPIPE when writing to stdout. So in the heartbeat mode, we do that.
        # The only documented way to exit serve_forever() is to call the
        # shutdown() method, which must be done from another thread, so that's
        # the approach we take.

        if settings.heartbeat:
            import threading
            import time

            def send_heartbeats(server):
                try:
                    while True:
                        print("heartbeat", flush=True)
                        time.sleep(1)
                except (KeyboardInterrupt, Exception) as e:
                    pass
                finally:
                    server.shutdown()

            hbthread = threading.Thread(
                target=send_heartbeats, args=(httpd,), daemon=True
            )
            hbthread.start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
            print("(interrupted)")


def _setup_preview_webclient(app_url, wtml_url, _image_url):
    if app_url is None:
        app_url = "https://worldwidetelescope.org/webclient/"

    url = app_url + "?wtml=" + urlquote(wtml_url)
    return url, "the WWT webclient"


def _setup_preview_research(app_url, wtml_url, image_url):
    if app_url is None:
        app_url = "https://web.wwtassets.org/research/latest/"

    enc_messages = []

    def msg(**kwargs):
        s = json.dumps(kwargs)
        s = base64.b64encode(s.encode("utf-8")).decode("ascii")
        enc_messages.append(s)

    msg(
        event="load_image_collection",
        url=wtml_url,
    )
    msg(
        event="image_layer_create",
        mode="preloaded",
        id="image",
        url=image_url,
        goto=True,
    )

    url = app_url + "?script=" + urlquote(",".join(enc_messages))
    return url, "the WWT research app"


def launch_app_for_wtml(
    wtml_url, image_url=None, browser=None, app_type="webclient", app_url=None
):
    """
    Launch a WWT data viewer in a new browser window.

    Parameters
    ----------
    wtml_url : str
        The URL of the WTML file to view
    image_url : str
        The URL of the imageset within the WTML file to view. This is currently
        required.
    browser : optional str or None
        The type of web browser to use to open the WTML preview application, as
        understood by the :mod:`webbrowser` module. If unspecified,
        :mod:`webbrowser` will guess a sensible default.
    app_type : optional str
        Which kind or application to use to view the WTML file. Allowed values
        are ``"webclient"`` (the default) for the classic WWT webclient, or
        ``"research"`` for the WWT research application.
    app_url : optional str or None
        The URL to use for the preview app. If ``None`` (the default), the
        default URL for the specified application is used. Note that this does
        not supersede the ``app_type`` argument because the form of the query
        string that is passed to the preview app depends on its type.

    Returns
    -------
    A human-readable description of the app that has been launched.
    """

    if app_type == "webclient":
        setup = _setup_preview_webclient
    elif app_type == "research":
        setup = _setup_preview_research
    else:
        raise ValueError("app_type")

    url, desc = setup(app_url, wtml_url, image_url)
    webbrowser.get(browser).open(url, new=1, autoraise=True)
    return desc


def preview_wtml(wtml_path, browser=None, app_type="webclient", app_url=None):
    """
    Run a server for a local WTML file and open it in a web browser.

    Parameters
    ----------
    wtml_path : str
        The path to a local WTML file
    browser : optional str or None
        The type of web browser to use to open the WTML preview application, as
        understood by the :mod:`webbrowser` module. If unspecified,
        :mod:`webbrowser` will guess a sensible default.
    app_type : optional str
        Which kind or application to use to view the WTML file. Allowed values
        are ``"webclient"`` (the default) for the classic WWT webclient, or
        ``"research"`` for the WWT research application.
    app_url : optional str or None
        The URL to use for the preview app. If ``None`` (the default), the
        default URL for the specified application is used. Note that this does
        not supersede the ``app_type`` argument because the form of the query
        string that is passed to the preview app depends on its type.

    Returns
    -------
    None
    """

    # In some cases (research app preview) we'll need to parse the WTML to
    # figure out the URL of the image to show. (In an ideal world, we might
    # add a "show this WTML and add whatever image layers make sense" message,
    # rather than having to handhold the app here.)
    fld = Folder.from_file(wtml_path)

    root_dir = os.path.dirname(wtml_path)
    server_path = os.path.basename(wtml_path.replace("_rel.wtml", ".wtml"))
    server_address = ("", 0)
    handler_factory = partial(WWTRequestHandler, directory=root_dir)

    with HTTPServerClass(server_address, handler_factory) as httpd:
        # Hack: the WWT JS engine special-cases 'localhost' and '127.0.0.1' so
        # that it doesn't start trying to proxy them if URLs result in 404s,
        # which is a common occurrence when working on tiled images. So ignore
        # the auto-detected server name and use one of those.
        server_name = "127.0.0.1"  # httpd.server_name
        wtml_url = f"http://{server_name}:{httpd.server_port}/{urlquote(server_path)}"

        # Compute the image URL
        image_url = None

        fld.mutate_urls(make_absolutizing_url_mutator(wtml_url.rsplit("/", 1)[0]))

        for _index, _kind, imgset in fld.immediate_imagesets():
            image_url = imgset.url
            break

        if image_url is None:
            raise Exception(f"found no imagesets in WTML preview file `{wtml_path}`")

        # By the time the browser opens and the app loads up, our server
        # *should* be up and running ...
        desc = launch_app_for_wtml(
            wtml_url,
            image_url=image_url,
            browser=browser,
            app_type=app_type,
            app_url=app_url,
        )

        print("file is being served as:", wtml_url)
        print(
            f"opening it in {desc} ... type Control-C to terminate this program when done"
        )

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
            print("(interrupted)")

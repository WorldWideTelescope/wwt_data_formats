# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 the .NET Foundation
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

"""

from __future__ import absolute_import, division, print_function

__all__ = '''
run_server
'''.split()

from functools import partial
import http.server
import os.path

from .folder import Folder, make_absolutizing_url_mutator

try:
    from http.server import ThreadingHTTPServer as HTTPServerClass
except ImportError:
    from http.server import HTTPServer as HTTPServerClass


class WWTRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.command in ('GET', 'HEAD'):
            self.send_header('Access-Control-Allow-Headers', 'Content-Disposition,Content-Encoding,Content-Type')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET,HEAD')
        return super(WWTRequestHandler, self).end_headers()

    def check_special_wtml(self):
        """
        Check whether this request is for a special synthetic WTML path, and if
        so, prep to respond to either a GET or a HEAD request. Returns a bytes
        of the response to write.

        If this request does not match a special synthetic WTML, returns None.
        """
        path = self.translate_path(self.path)

        if not path.endswith('.wtml'):
            return None

        local_wtml_path = path[:-5] + '_rel.wtml'
        if not os.path.exists(local_wtml_path):
            return None

        host = self.headers.get('Host')
        if host is None:
            host = f'{self.server.server_name}:{self.server.server_port}'
        baseurl = f'http://{host}{self.path}'
        self.log_message('special WTML: local %s, baseurl %s', local_wtml_path, baseurl)
        f = Folder.from_file(local_wtml_path)
        f.mutate_urls(make_absolutizing_url_mutator(baseurl))
        resp = f.to_xml_string().encode('utf-8')

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


def run_server(settings):
    """
    Settings are defined in :func:`wwt_data_formats.cli.serve_getparser`.

    """
    server_address = ('', settings.port)
    handler_factory = partial(WWTRequestHandler, directory=settings.root_dir)

    with HTTPServerClass(server_address, handler_factory) as httpd:
        # Hack: the WWT JS engine special-cases 'localhost' and '127.0.0.1' so
        # that it doesn't start trying to proxy them if URLs result in 404s,
        # which is a common occurrence when working on tiled images. So ignore
        # the auto-detected server name and use one of those.
        server_name = '127.0.0.1'  # httpd.server_name

        print(f'listening at: http://{server_name}:{httpd.server_port}/')
        print()
        print('virtual root-directory WTML files with on-the-fly rewriting:')
        print()

        seen_any = False

        for bn in os.listdir(settings.root_dir):
            if bn.endswith('_rel.wtml'):
                virtual = bn[:-9] + '.wtml'
                print(f'    http://{server_name}:{httpd.server_port}/{virtual}')
                seen_any = True

        if not seen_any:
            print('    (none)')

        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
            print('(interrupted)')


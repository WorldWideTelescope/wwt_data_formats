# -*- mode: python; coding: utf-8 -*-
# Copyright 2022 the AAS WorldWide Telescope project
# Licensed under the MIT License.

from .. import cli


class TestMiscCli(object):
    def test_show_concept_doi(self):
        """
        More smoketests.
        """
        cli.entrypoint(["show", "concept-doi"])

    def test_show_version(self):
        """
        More smoketests.
        """
        cli.entrypoint(["show", "version"])

    def test_show_version_doi(self):
        """
        More smoketests.
        """
        cli.entrypoint(["show", "version-doi"])

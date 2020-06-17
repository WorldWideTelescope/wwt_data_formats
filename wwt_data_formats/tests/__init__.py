# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

__all__ = '''
assert_xml_trees_equal
test_path
'''.split()

import os.path


TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_path(*pieces):
    return os.path.join(TESTS_DIR, *pieces)


def _assert_xml_trees_equal(path, e1, e2, care_text_tags):
    "Derived from https://stackoverflow.com/a/24349916/3760486"

    assert e1.tag == e2.tag, \
        'at XML path {0}, tags {1} and {2} differed'.format(path, e1.tag, e2.tag)

    # We only sometimes care about this; often it's just whitespace
    if e1.tag in care_text_tags:
        assert e1.text == e2.text, \
            'at XML path {0}, texts {1!r} and {2!r} differed'.format(path, e1.text, e2.text)

    # We never care about this, right?
    #assert e1.tail == e2.tail, \
    #    'at XML path {0}, tails {1!r} and {2!r} differed'.format(path, e1.tail, e2.tail)

    assert e1.attrib == e2.attrib, \
        'at XML path {0}, attributes {1!r} and {2!r} differed'.format(path, e1.attrib, e2.attrib)
    assert len(e1) == len(e2), \
        'at XML path {0}, number of children {1} and {2} differed'.format(path, len(e1), len(e2))

    subpath = '{0}>{1}'.format(path, e1.tag)

    for c1, c2 in zip (e1, e2):
        _assert_xml_trees_equal(subpath, c1, c2, care_text_tags)


def assert_xml_trees_equal(e1, e2, care_text_tags=()):
    _assert_xml_trees_equal('(root)', e1, e2, care_text_tags)

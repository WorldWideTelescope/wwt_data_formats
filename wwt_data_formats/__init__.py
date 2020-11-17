# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Licensed under the MIT License.

from __future__ import absolute_import, division, print_function

__all__ = '''
indent_xml
LockedDownTraits
LockedXmlTraits
MetaLockedDownTraits
stringify_xml_doc
write_xml_doc
XmlSer
'''.split()

from abc import ABCMeta
from argparse import Namespace
from enum import Enum
from traitlets import (Bool, Float, HasTraits, Instance, Int, List, MetaHasTraits,
                       TraitType, Unicode, Union, UseEnum)
from xml.etree import ElementTree as etree


class MetaLockedDownTraits(ABCMeta, MetaHasTraits):
    """A metaclass to help with the LockedDownTraits class. When a class using
    this metaclass is created, a frozenset of all of the traitlets attached to
    the class definition (including those defined by its base classes) is
    created for fast checks during __setattr__ calls. The other setup done by
    traitlet's MetaHasTraits metaclass is also performed.

    """
    def __init__(cls, name, bases, classdict):
        super(MetaLockedDownTraits, cls).__init__(name, bases, classdict)

        # This list hardcode attributes that are manipulated by the traitlets
        # machinery.
        settable_attr_names = set((
            '_cross_validation_lock',
            '_trait_notifiers',
            '_trait_validators',
            '_trait_values',
            'notify_change',
        ))

        for c in cls.mro():
            for attr_name, attr_value in c.__dict__.items():
                if isinstance(attr_value, TraitType):
                    settable_attr_names.add(attr_name)

        cls._settable_attr_names = frozenset(settable_attr_names)


class LockedDownTraits(HasTraits, metaclass=MetaLockedDownTraits):
    """A base class for HasTraits objects where we do not allow callers to add
    additional attributes to class instances. We do not allow them to delete
    attributes either.

    The general motivation is that there are some kinds of classes that
    contain a pretty fixed set of fields where it's much more likely that
    someone is going to make a typo in a variable assignment than it will be
    legitimately useful for them to add new attributes.

    There's an escape hatch, however, the ``rmeta`` attribute (for "runtime
    metadata") is a namespace object to which one can attach whichever
    metadata one wants.

    """
    rmeta = Instance(
        Namespace,
        args = (),
        help = 'Runtime metadata - a namespace object for attaching arbitrary extra information',
    )

    def __setattr__(self, name, value):
        if name not in self._settable_attr_names:
            raise AttributeError(f'not allowed to set attribute {name!r} on this instance (typo?)')
        super(LockedDownTraits, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name != 'notify_change':  # sigh, traitlets
            raise AttributeError(f'not allowed to delete attribute {name!r} from this instance')
        super(LockedDownTraits, self).__delattr__(name)

    def __repr__(self):
        # This gets a bit beyond the nominal bailiwick of this class, but it's
        # pretty universally useful.
        s = ', '.join('{}={!r}'.format(a, getattr(self, a)) for a in self.trait_names())
        return f'{self.__class__.__name__}({s})'


class XmlSer(Enum):
    """Ways that a traitlet can get serialized to XML in this framework.

    """
    ATTRIBUTE = 'attr'
    TEXT_ELEM = 'text_elem'
    INNER = 'inner'
    WRAPPED_INNER = 'wrapped_inner'
    NS_TO_ATTR = 'ns_to_attr'
    INNER_LIST = 'inner_list'
    WRAPPED_INNER_LIST = 'wrapped_inner_list'

    @classmethod
    def attr(cls, attr):
        return (cls.ATTRIBUTE, attr)

    @classmethod
    def text_elem(cls, tag):
        return (cls.TEXT_ELEM, tag)

    @classmethod
    def inner(cls, tag):
        # todo: I'd like to avoid the `tag` argument, but right now we need it
        # to search for a pre-existing element when applying to an existing
        # XML tree.
        return (cls.INNER, tag)

    @classmethod
    def wrapped_inner(cls, tag):
        return (cls.WRAPPED_INNER, tag)

    @classmethod
    def ns_to_attr(cls, prefix):
        return (cls.NS_TO_ATTR, prefix)

    @classmethod
    def inner_list(cls):
        return (cls.INNER_LIST,)

    @classmethod
    def wrapped_inner_list(cls, tag):
        return (cls.WRAPPED_INNER_LIST, tag)


def _stringify_trait(trait_spec, value):
    if isinstance(trait_spec, UseEnum):
        return str(value.value)

    return str(value)


def _parse_trait(trait_spec, text):
    if isinstance(trait_spec, Float):
        return float(text)

    if isinstance(trait_spec, Int):
        return int(text)

    if isinstance(trait_spec, Unicode):
        return text

    if isinstance(trait_spec, Bool):
        try:
            return bool(int(text))
        except ValueError:
            pass

        if text.lower() == 'false':
            return False

        if text.lower() == 'true':
            return True

        raise ValueError(f'cannot interpret text {text!r} as a boolean')

    if isinstance(trait_spec, UseEnum):
        if text is None:
            text = ''
        return trait_spec.enum_class.from_text(text)

    raise ValueError(f'internal error: unimplemented parse for trait type {trait_spec}')


class LockedXmlTraits(LockedDownTraits):
    """A base class for LockedDownTraits objects that can also be serialized to
    and from XML.

    This is not a fully general XML serialization framework; it is tuned to
    the needs of the WWT XML serialization formats.

    """
    def _tag_name(self):
        """Return the XML tag name associated with the serialization of this object."""
        raise NotImplementedError()

    def _check_elem_is_this_type(self, elem):
        """Return whether the XML element represents an instance of this class.

        By default, this function returns True if the elem tag name matches
        this classes ``_tag_name()``. This filter can be overridden. This
        function is used by ``_maybe_from_xml()`` when deserializing
        containers with contents that have flexible types.

        """

        return elem.tag == self._tag_name()

    @classmethod
    def _maybe_from_xml(cls, elem):
        """Possibly deserialize an instance of this class from an XML fragment.

        Parameters
        ----------
        elem : :class:`xml.etree.ElementTree.Element`
          An XML element.

        Returns
        -------
        If the XML element appears to contain a serialized version of this class,
        returns a new instance, initialized with data from the XML. Otherwise,
        returns None.

        Notes
        -----
        This method is architected to enable deserialization of
        :class:`wwt_data_formats.folder.Folder` items. It also helps with the
        implementation of some of the "inner" XML deserialization
        implementations.

        """
        inst = cls()

        if not inst._check_elem_is_this_type(elem):
            return None

        for tname, tspec in inst.traits(xml = lambda a: a is not None).items():
            xml_spec, *xml_data = tspec.metadata['xml']
            value = None

            if xml_spec == XmlSer.ATTRIBUTE:
                text = elem.attrib.get(xml_data[0])
                if text is not None:
                    value = _parse_trait(tspec, text)
            elif xml_spec == XmlSer.TEXT_ELEM:
                sub = elem.find(xml_data[0])
                if sub is not None:
                    value = _parse_trait(tspec, sub.text)
            elif xml_spec == XmlSer.INNER:
                if not isinstance(tspec, Instance):
                    raise RuntimeError('an XML element serialized as INNER must be of Instance type')

                for sub in elem:
                    value = tspec.klass._maybe_from_xml(sub)
                    if value is not None:
                        break
            elif xml_spec == XmlSer.WRAPPED_INNER:
                if not isinstance(tspec, Instance):
                    raise RuntimeError('an XML element serialized as WRAPPED_INNER must be of Instance type')

                wrapper = elem.find(xml_data[0])
                if wrapper is not None:
                    for sub in wrapper:
                        value = tspec.klass._maybe_from_xml(sub)
                        if value is not None:
                            break
            elif xml_spec == XmlSer.NS_TO_ATTR:
                if not isinstance(tspec, Instance):
                    raise RuntimeError('an XML element serialized as NS_TO_ATTR must be of Instance type')

                value = tspec.klass()
                for aname, avalue in elem.attrib.items():
                    if aname.startswith(xml_data[0]):
                        setattr(value, aname[len(xml_data[0]):], avalue)
            elif xml_spec == XmlSer.INNER_LIST:
                if not isinstance(tspec, List):
                    raise RuntimeError('XML elements serialized as INNER_LIST must be of List type')

                # total hackiness specific for the Folder use case, plus encapsulation breakage:
                un_spec = tspec._trait
                if not isinstance(un_spec, Union):
                    raise RuntimeError('XML elements serialized as INNER_LIST must be of List(Union) type')

                klasses = [t.klass for t in un_spec.trait_types]
                # end hackiness, maybe.

                value = []

                for sub in elem:
                    for klass in klasses:
                        v = klass._maybe_from_xml(sub)
                        if v is not None:
                            value.append(v)
                            break
            elif xml_spec == XmlSer.WRAPPED_INNER_LIST:
                # Repeat the INNER_LIST hackiness
                if not isinstance(tspec, List):
                    raise RuntimeError('XML elements serialized as WRAPPED_INNER_LIST must be of List type')

                un_spec = tspec._trait
                if not isinstance(un_spec, Union):
                    raise RuntimeError('XML elements serialized as WRAPPED_INNER_LIST must be of List(Union) type')

                klasses = [t.klass for t in un_spec.trait_types]
                # end hackiness, maybe.

                value = []

                wrapper = elem.find(xml_data[0])
                if wrapper is not None:
                    for sub in wrapper:
                        for klass in klasses:
                            v = klass._maybe_from_xml(sub)
                            if v is not None:
                                value.append(v)
                                break
            else:
                raise RuntimeError(f'unhandled XML serialization mode {xml_spec}')

            if value is not None:
                setattr(inst, tname, value)

        return inst


    @classmethod
    def from_xml(cls, elem):
        """Deserialize an instance of this class from XML.

        Parameters
        ----------
        elem : xml.etree.ElementTree.Element
          An XML element serializing the object.

        Returns
        -------
        An instance of the class, initialized with data from the XML.

        """
        inst = cls._maybe_from_xml(elem)
        if inst is None:
            raise ValueError(f'expected to get a {cls} instance from <{elem.tag}>, but didn\'t')
        return inst


    @classmethod
    def from_text(cls, text):
        """Deserialize an instance of this class from XML-formatted text.

        Parameters
        ----------
        text : string
          The XML text.

        Returns
        -------
        An instance of the class, initialized with data from the XML.

        """
        elem = etree.fromstring(text)
        return cls.from_xml(elem)


    @classmethod
    def from_file(cls, path, encoding='utf-8-sig'):
        """Deserialize an instance of this class from an XML file on local disk.

        Parameters
        ----------
        path : string
            The path of the XML file.
        encoding : optional string, default "utf-8-sig"
            The encoding of the file text. The default value is basically UTF-8 but
            will ignore Windows Byte Order Markers (BOMs) if present.

        Returns
        -------
        An instance of the class, initialized with data from the XML.

        """
        with open(path, 'rt', encoding=encoding) as f:
            text = f.read()

        return cls.from_text(text)


    @classmethod
    def from_url(cls, url, session=None, **kwargs):
        """Deserialize an instance of this class from XML downloaded from the
        specified URL.

        Parameters
        ----------
        url : string
            The URL from which to download the XML.
        session : ``requests`` session or None (the default)
            The HTTP communications session to use.
        kwargs
            Extra arguments to pass to ``requests.get``.

        Returns
        -------
        An instance of the class, initialized with data from the XML.

        """
        if session is None:
            import requests
            session = requests

        resp = session.get(url, **kwargs)

        # We have to set this to get requests/Python to ignore the Unicode
        # Byte Order Marker (BOM) that is present in some WWT data files due
        # to their Windows origin, when we decode the response into text.
        resp.encoding = 'utf-8-sig'

        elem = etree.fromstring(resp.text)
        return cls.from_xml(elem)


    def _serialize_xml(self, elem):
        """Do the work of serializing this thing to XML.

        Parameters
        ----------
        elem : :class:`xml.etree.ElementTree.Element` or None
          An XML subtree that will be filled in with data values associated with this
          instance. If None, a new element will be created and populated with the
          instance data.

        Returns
        -------
        The serialized XML element. If it was not None, this is the parameter *elem*.

        Notes
        -----
        This method is intended to allow two modes of operation. It can either
        create XML trees from scratch, or it can modify existing trees. The
        latter mode makes it possible to work with input data that may have
        additional contents not defined in the WWT specification -- by
        modifying the existing tree, we can preserve those data.

        A trait whose value is None is omitted from the XML serialization.

        A trait that is represented textually (either as an attribute or a
        text element) whose textualization is empty is also ommitted from the
        XML serialization.

        """
        if elem is None:
            elem = etree.Element(self._tag_name())

        # Note that self.traits() generates the traits in alphabetical order,
        # which is helpful because that means when we serialize to XML the
        # child elements are created in a deterministic order, which makes it
        # easier to test the output.

        for tname, tspec in self.traits(xml = lambda a: a is not None).items():
            xml_spec, *xml_data = tspec.metadata['xml']
            value = getattr(self, tname)

            if value is None:
                continue

            if xml_spec == XmlSer.ATTRIBUTE:
                text = _stringify_trait(tspec, value)
                if not text:
                    continue

                elem.set(xml_data[0], text)
            elif xml_spec == XmlSer.TEXT_ELEM:
                text = _stringify_trait(tspec, value)
                if not text:
                    continue

                sub = elem.find(xml_data[0])
                if sub is None:
                    sub = etree.SubElement(elem, xml_data[0])

                sub.text = text
            elif xml_spec == XmlSer.INNER:
                cur_sub = elem.find(xml_data[0])
                new_sub = value._serialize_xml(cur_sub)
                if cur_sub is None:
                    elem.append(new_sub)
            elif xml_spec == XmlSer.WRAPPED_INNER:
                wrapper = elem.find(xml_data[0])
                if wrapper is None:
                    wrapper = etree.SubElement(elem, xml_data[0])

                if len(wrapper):
                    value._serialize_xml(wrapper[0])
                else:
                    new_sub = value._serialize_xml(None)
                    wrapper.append(new_sub)
            elif xml_spec == XmlSer.NS_TO_ATTR:
                for ns_name, ns_value in value.__dict__.items():
                    elem.set(xml_data[0] + ns_name, str(ns_value))
            elif xml_spec == XmlSer.INNER_LIST:
                # This is gross. If the list of children gets mutated, in the
                # current framework we basically have no way to know what
                # pre-existing XML elements map to our children. The best I
                # can come up with is that we try to enforce the invariant
                # that the list of children cannot get mutated.
                preexisting = bool(len(elem))

                if preexisting and len(elem) != len(value):
                    raise RuntimeError('serializing flexible list to existing XML data, '
                                       'but it looks like something changed beneath us')

                for idx, child in enumerate(value):
                    if preexisting:
                        if elem[idx].tag != child._tag_name():
                            raise RuntimeError('serializing flexible list to existing XML data, '
                                               f'but it looks like child #{i} changed')
                        child._serialize_xml(elem[idx])
                    else:
                        new_sub = child._serialize_xml(None)
                        elem.append(new_sub)
            elif xml_spec == XmlSer.WRAPPED_INNER_LIST:
                wrapper = elem.find(xml_data[0])

                if wrapper is None:
                    preexisting = False
                    wrapper = etree.SubElement(elem, xml_data[0])
                else:
                    preexisting = True

                    if len(wrapper) != len(value):
                        raise RuntimeError('serializing flexible list to existing XML data, '
                                           'but it looks like something changed beneath us')

                for idx, child in enumerate(value):
                    if preexisting:
                        if wrapper[idx].tag != child._tag_name():
                            raise RuntimeError('serializing flexible list to existing XML data, '
                                               f'but it looks like child #{i} changed')
                        child._serialize_xml(wrapper[idx])
                    else:
                        new_sub = child._serialize_xml(None)
                        wrapper.append(new_sub)
            else:
                raise RuntimeError(f'unhandled XML serialization mode {xml_spec}')

        return elem


    def apply_to_xml(self, elem):
        """Serialize the data of this object to an existing XML tree

        Parameters
        ----------
        elem : :class:`xml.etree.ElementTree.Element`
          An XML subtree that will be filled in with data values associated with this
          instance.

        Returns
        -------
        *self*

        Notes
        -----
        This method makes it possible to work with input data that may have
        additional contents not defined in the WWT specification -- by
        modifying the existing tree, we can preserve those data.

        """
        self._serialize_xml(elem)
        return self


    def to_xml(self):
        """Serialize this object to XML.

        Returns
        -------
        elem : :class:`xml.etree.ElementTree.Element`
          An XML element serializing the object.

        """
        return self._serialize_xml(None)


    def write_xml(self, dest_stream, dest_wants_bytes=False, indent=True):
        """Serialize this object to XML, writing the data to a stream.

        Parameters
        ----------
        dest_stream : writeable file-like object or None
          The destination to which the XML data will be written. If None,
          standard output is used.
        dest_wants_bytes : optional bool, default False
          Whether the destination stream expects to be fed bytes data rather
          than Unicode. If so, the XML text is encoded into UTF-8 before
          being written.
        indent : bool, default True
          Whether the returned XML text will have user-friendly indentation or not.

        Returns
        -------
        None

        """
        write_xml_doc(
            self.to_xml(),
            dest_stream = dest_stream,
            dest_wants_bytes = dest_wants_bytes,
            indent = indent,
        )


    def to_xml_string(self, indent=True):
        """Serialize this object to XML text.

        Parameters
        ----------
        indent : optional bool, default True
          Whether the returned XML text will have user-friendly indentation or not.

        Returns
        -------
        xml_text : string
          A textual serialization of the object as XML.

        """
        return stringify_xml_doc(self.to_xml(), indent=indent)


def indent_xml(elem, level=0):
    """A dumb XML indenter.

    We create XML files using xml.etree.ElementTree, which is careful about
    spacing and so by default creates ugly files with no linewraps or
    indentation. This function is copied from `ElementLib
    <http://effbot.org/zone/element-lib.htm#prettyprint>`_ and implements
    basic, sensible indentation using "tail" text.

    """
    i = "\n" + level * "  "

    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:  # intentionally updating "elem" here!
            indent_xml(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def write_xml_doc(root_element, indent=True, dest_stream=None, dest_wants_bytes=False):
    """
    Write out some XML elements, indenting them by default

    When *indent* is true, the default setting, this function modifies
    *root_element*.

    If *dest_stream* is left unspecified, ``sys.stdout`` is used.

    Due to some subtle cross-platform issues with proper text encoding, do not
    use this function with a StringIO argument. Instead, use
    :func:`stringify_xml_doc`.
    """

    if dest_stream is None:
        import sys
        dest_stream = sys.stdout

    if indent:
        indent_xml(root_element)

    doc = etree.ElementTree(root_element)

    # If the dest stream accepts text, one can serialize XML into it using
    # `encoding = "Unicode"`. But it turns out that in this mode, ETree sets the
    # XML encoding declaration to what `locale.getpreferredencoding()` returns,
    # which in Windows is CP-1252, which makes WWT unhappy. To ensure proper
    # UTF-8 output, we need to get at the underlying byte stream.

    if not dest_wants_bytes:
        try:
            dest_stream = dest_stream.buffer
        except Exception as e:
            raise Exception('XML output into text I/O requires a destination whose '
                'underlying bytes I/O can be retrieved') from e

    doc.write(dest_stream, encoding='UTF-8', xml_declaration=True)


def stringify_xml_doc(root_element, indent=True):
    """Stringify some XML elements, indenting them by default.

    When *indent* is true, the default setting, this function modifies *root_element*.

    """
    # We have to serialize into a BytesIO to ensure that we can force the XML
    # encoding to be UTF-8 even when running on Windows, when the locale
    # encoding may default to CP-1252.
    from io import BytesIO
    with BytesIO() as dest:
        write_xml_doc(root_element, indent, dest, dest_wants_bytes=True)
        bytes_result = dest.getvalue()
    return bytes_result.decode('utf-8')

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

from argparse import Namespace
from enum import Enum
from traitlets import Bool, Float, HasTraits, Instance, Int, MetaHasTraits, TraitType, Unicode, UseEnum
from xml.etree import ElementTree as etree


class MetaLockedDownTraits(MetaHasTraits):
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

    @classmethod
    def attr(cls, attr):
        return (cls.ATTRIBUTE, attr)

    @classmethod
    def text_elem(cls, tag):
        return (cls.TEXT_ELEM, tag)

    @classmethod
    def inner(cls, tag):
        return (cls.INNER, tag)

    @classmethod
    def wrapped_inner(cls, tag):
        return (cls.WRAPPED_INNER, tag)


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
        # We could do better than a linear search here, but meh.
        for enum_value in trait_spec.enum_class:
            if text == enum_value.value:
                return enum_value
        raise ValueError(f'unrecognized value {text!r} for enumeration {trait_spec.enum_class}')

    raise ValueError(f'internal error: unimplemented parse for trait type {trait_spec}')


class LockedXmlTraits(LockedDownTraits):
    """A base class for LockedDownTraits objects that can also be serialized to
    and from XML.

    """
    def _tag_name(self):
        raise NotImplementedError()

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
        inst = cls()

        if elem.tag != inst._tag_name():
            raise ValueError('expected <{}> tag but got <{}>'.format(inst._tag_name(), elem.tag))

        for tname, tspec in inst.traits(xml = lambda a: a is not None).items():
            xml_spec, *xml_data = tspec.metadata['xml']
            value = None

            if xml_spec == XmlSer.ATTRIBUTE:
                text = elem.attrib.get(xml_data[0])
                value = _parse_trait(tspec, text)
            elif xml_spec == XmlSer.TEXT_ELEM:
                sub = elem.find(xml_data[0])
                if sub is not None:
                    value = _parse_trait(tspec, sub.text)
            elif xml_spec == XmlSer.INNER:
                if not isinstance(tspec, Instance):
                    raise RuntimeError('an XML element serialized as INNER must be of Instance type')

                sub = elem.find(xml_data[0])
                if sub is not None:
                    value = tspec.klass.from_xml(sub)
            elif xml_spec == XmlSer.WRAPPED_INNER:
                if not isinstance(tspec, Instance):
                    raise RuntimeError('an XML element serialized as WRAPPED_INNER must be of Instance type')

                wrapper = elem.find(xml_data[0])
                if wrapper is not None:
                    value = tspec.klass.from_xml(wrapper[0])
            else:
                raise RuntimeError(f'unhandled XML serialization mode {xml_spec}')

            if value is not None:
                setattr(inst, tname, value)

        return inst


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

        Remarks
        -------
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

        Remarks
        -------
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
    """Write out some XML elements, indenting them by default

    When *indent* is true, the default setting, this function modifies *root_element*.

    If *dest_stream* is left unspecified, ``sys.stdout`` is used.

    """
    if dest_stream is None:
        import sys
        dest_stream = sys.stdout

    if indent:
        indent_xml(root_element)

    doc = etree.ElementTree(root_element)

    # We could in principle auto-detect this with a 0-byte write(), I guess?
    if dest_wants_bytes:
        encoding = 'UTF-8'
    else:
        encoding = 'Unicode'

    doc.write(dest_stream, encoding=encoding, xml_declaration=True)


def stringify_xml_doc(root_element, indent=True):
    """Stringify some XML elements, indenting them by default.

    When *indent* is true, the default setting, this function modifies *root_element*.

    """
    from io import StringIO
    with StringIO() as dest:
        write_xml_doc(root_element, indent, dest, dest_wants_bytes=False)
        result = dest.getvalue()
    return result

import codecs
from enum import Enum

from functools import singledispatch, update_wrapper

# BOM used to encode in utf-8
BOM = codecs.BOM_UTF8

# Path to the default orosunit.ini (orostk/quantity/orosunit.ini)
OROSUNIT_PATH = '\\orosunit.ini'


def string_to_escaped_utf8(string):
    """

    :param string: String to quote escape
    :return: A new string quote escaped
    """
    string_utf8 = string.encode('utf-8')
    string_utf8 = string_utf8.replace(b'\\', b'\\\\')
    string_utf8 = string_utf8.replace(b'\"', b'\\\"')
    return b'"' + string_utf8 + b'"'


def methdispatch(func):
    """
    This is a decorator to to singledispatch on instance method
    :param func:
    :return:
    """
    dispatcher = singledispatch(func)

    def wrapper(*args, **kwargs):
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


class ValueFormat(Enum):
    """
    This class represents the format of a value (real, complex ...)
    """
    REAL = 0
    COMPLEX_REAL_IMAGINARY = 1
    COMPLEX_MODULE_PHASE = 2

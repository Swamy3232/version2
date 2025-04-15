from enum import Enum


class FieldType(Enum):
    # fixed size string
    FSTRING = 1
    STRING = 2
    SHORT = 3
    LONG = 4
    USHORT = 5
    FLOAT = 6
    DATE = 7
    UINT = 8
    # Array of float
    V_FLOAT = 9
    # Array of (float, float,...)
    V_TUPLE_FLOAT = 10

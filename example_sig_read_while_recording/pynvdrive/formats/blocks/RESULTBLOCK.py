import struct
import json
from ...quantity.quantity_provider import QuantityProvider
from datetime import datetime
import copy
from ...client import ENCODING_MBCS


b_str_EOL = b'\x00'


class ResultBlock(object):
    """This class represent a result block
    It's a generic class to construct all classes
    defined below
    fields:

        :param block_id: Key identifying the type of block that follows
        :type block_id: str
        :param version: Version number allowing structure.txt evolution (the first version is numbered 0)
        :type version: int
        :block_size: Size of rest of block, automatically calculated
        :return:
    """

    def __init__(self, block_id=None, version=None):
        """Constructor method
        """

        self.id = block_id
        self.version = version
        self.block_size = None

        self.binary_header = None
        self.binary_body = None

        self.quantity_provider = None

    def get_binary_header(self):
        """Generate block binary header
        """
        if self.binary_body:
            self.block_size = len(self.binary_body)

            self.binary_header = bytes(self.id, ENCODING_MBCS, errors='replace')

            b_version = struct.pack('h', self.version)
            self.binary_header += b_version
            b_block_size = struct.pack('l', self.block_size)
            self.binary_header += b_block_size

        else:
            self.block_size = None

    def parse_header(self):
        """Retrieve header data from binary
        """
        self.version = struct.unpack('h', self.binary_header[0:2])[0]
        self.block_size = struct.unpack('l', self.binary_body[2:6])[0]


    def json_default(self, value):
        """Default JSON conversion for unserializable value
        :param value: object to serialize
        :return: object json
        """
        if hasattr(value, '__dict__'):
            return value.__dict__
        if isinstance(value, datetime):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

    def to_json(self):
        """Get RESULTBLOCK as JSON
        :return: json resultblock
        """
        return json.dumps(self, default=self.json_default,sort_keys=True, indent=4, ensure_ascii=False) #default=lambda o: o.__dict__

    def to_dict(self):
        """Get RESULTBLOCK as dict
        :return: dict resultblock
        """
        dict = vars(copy.copy(self))
        # Remove undesired attributes
        dict.pop('binary_header', None)
        dict.pop('binary_body', None)
        dict.pop('quantity_provider', None)
        dict.pop('block_size', None)

        if self.__class__.__name__ == 'XREF':
            dict['list_references'] = [reference.to_dict() for reference in self.list_references]

        return dict

    @staticmethod
    def check_unit_exist(quantity_provider:QuantityProvider, physical_quantity=None, magnitude_key=None, unit_name=None, unit_label=None):
        """Check if provided units is valid, unit_name OR unit_label is mandatory + physical_quantity
        """
        unit = quantity_provider.get_unit(magnitude_key=magnitude_key, magnitude_name=physical_quantity, unit_name=unit_name, unit_label=unit_label)
        return unit


class BlockException(Exception):
    pass


class BlockUnconsistent(BlockException):
    """
    Something's missing into the block ...
    """
    pass


class BlockUnitError(BlockException):
    """
    Error with the unit
    """
    pass

from ..blocks.RESULTBLOCK import ResultBlock, b_str_EOL
from pynvdrive import ENCODING_MBCS
from ...quantity.quantity_utils import convert_unit
import struct
import copy
from pynvdrive.command import Command


class XREG(ResultBlock):
    """
    This class represent a XREG block
    fields:

    - id.
    - version (actual version is 3).
    - block_size.
    - start.
    - stop.
    - n_octave. : 0,1,2,3 (1, 1/3, 1/12, 1/24)
    - quantity_key.
    - unit_name.
    - unit_label.
    - rel_precision, version >= 1.
    - abs_precision, version >= 1.
    - magnitude_key, version >= 3.

    Example::

        xreg = XREG(start=0, stop=100, n_octave=1, quantity_key='Time',
                         rel_precision=1, abs_precision=1)

    """
    def __init__(self, version=3,
                 start=None, stop=None, n_octave=None, physical_quantity=None,
                 unit_name=None, unit_label=None, rel_precision=None,
                 abs_precision=None, magnitude_key=None):
        """

        :param version:
        :type version: int
        :param start:
        :type start: float
        :param stop:
        :type stop: float
        :param n_octave:
        :type n_octave: float
        :param physical_quantity:
        :type physical_quantity: str
        :param unit_name:
        :type unit_name: str
        :param unit_label:
        :type unit_label: str
        :param rel_precision:
        :type rel_precision: float
        :param abs_precision:
        :type abs_precision: float
        :return:
        """
        super().__init__('XREG', version)

        self.version = version

        self.start = start
        self.stop = stop
        self.n_octave = n_octave
        self.physical_quantity = physical_quantity
        self.unit_name = unit_name
        self.unit_label = unit_label

        # version >= 1
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision

        # version >= 2
        self.magnitude_key = magnitude_key

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        b_start = struct.pack('f', self.start)
        self.binary_body += b_start
        b_stop = struct.pack('f', self.stop)
        self.binary_body += b_stop
        b_n_octave = struct.pack('h', self.n_octave)
        self.binary_body += b_n_octave

        b_physical_quantity = bytes(self.physical_quantity, ENCODING_MBCS, errors='replace') + b_str_EOL
        self.binary_body += b_physical_quantity
        b_unit_name = bytes(self.unit_name, ENCODING_MBCS, errors='replace') + b_str_EOL
        self.binary_body += b_unit_name
        b_unit_label = bytes(self.unit_label, ENCODING_MBCS, errors='replace') + b_str_EOL
        self.binary_body += b_unit_label

        if self.version >= 1:
            b_rel_precision = struct.pack('f', self.rel_precision)
            self.binary_body += b_rel_precision
            b_abs_precision = struct.pack('f', self.abs_precision)
            self.binary_body += b_abs_precision
        if self.version >= 3:
            b_magnitude_key = bytes(self.magnitude_key, ENCODING_MBCS, errors='replace') + b_str_EOL
            self.binary_body += b_magnitude_key

        self.get_binary_header()

        return self.binary_header + self.binary_body

    def from_binary(self, contents):
        """Parse binary block
        """
        self.binary_header = contents[:6]
        self.binary_body = contents[6:]

        self.parse_header()
        self.parse_body()

    def parse_body(self):
        """Parse binary body to individuals attributes
        """
        self.start = struct.unpack('f', self.binary_body[:4])[0]
        self.stop = struct.unpack('f', self.binary_body[4:8])[0]
        self.n_octave = struct.unpack('h', self.binary_body[8:10])[0]

        reste = self.binary_body[10:]
        reste = reste.split(b'\0', 3)

        self.physical_quantity = Command.parse_response_string(reste[0])
        self.unit_name = Command.parse_response_string(reste[2])
        self.unit_label = Command.parse_response_string(reste[1])

        if self.version >= 1:
            reste = reste[-1]
            self.rel_precision = struct.unpack('f', reste[0:4])[0]
            self.abs_precision = struct.unpack('f', reste[4:8])[0]
        if self.version >= 3:
            reste = reste.split(b'\0')
            self.magnitude_key = Command.parse_response_string(reste[-1])

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        self.start = block_dict.get('start', self.start)
        self.stop = block_dict.get('stop', self.stop)
        self.n_octave = block_dict.get('n_octave', self.n_octave)
        self.physical_quantity = block_dict.get('physical_quantity', self.physical_quantity)
        self.unit_name = block_dict.get('unit_name', self.unit_name)
        self.unit_label = block_dict.get('unit_label', self.unit_label)
        self.rel_precision = block_dict.get('rel_precision', self.rel_precision)
        self.abs_precision = block_dict.get('abs_precision', self.abs_precision)
        self.magnitude_key = block_dict.get('magnitude_key', self.magnitude_key)

        return self

    def convert_to_SI(self, quantity_provider):
        """Convert xreg to SI if needed
        """
        xreg = copy.deepcopy(self)

        user_unit = self.check_unit_exist(quantity_provider=quantity_provider, magnitude_key=xreg.magnitude_key, physical_quantity=xreg.physical_quantity, unit_name=xreg.unit_name, unit_label=xreg.unit_label)
        xreg.physical_quantity = user_unit.magnitude_name
        xreg.magnitude_key = user_unit.magnitude_key
        xreg.unit_name = user_unit.unit_name
        xreg.unit_label = user_unit.unit_name


        xreg.start = convert_unit(value=xreg.start, src_unit=user_unit)
        xreg.stop = convert_unit(value=xreg.stop, src_unit=user_unit)
        if xreg.rel_precision:
            xreg.rel_precision = convert_unit(value=xreg.rel_precision, src_unit=user_unit)
        if xreg.abs_precision:
            xreg.abs_precision = convert_unit(value=xreg.abs_precision, src_unit=user_unit)

        return xreg
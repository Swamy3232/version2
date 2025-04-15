from ..blocks.RESULTBLOCK import ResultBlock
from ...quantity.quantity_utils import convert_unit
import struct
import copy


class SCAL(ResultBlock):
    """
    This class represent a SCAL block
    fields:

    - id.
    - version (actual version is 2).
    - block_size.
    - min.
    - max.
    - value.
    - complex.
    - rel_precision, version >= 1.
    - abs_precision, version >= 1.
    - imag, version >= 2.

    Example::

        scal = SCAL(min=0, max=100, value=50,
                         rel_precision=0.1, abs_precision=0.1)

    """

    def __init__(self, version=2,
                 min=None, max=None, value=None,
                 rel_precision=None, abs_precision=None, imag=0.0):
        """

        :param version:
        :type version: int
        :param min:
        :type min: float
        :param max:
        :type max: float
        :param value:
        :type value: float
        :param rel_precision: version >= 1
        :type rel_precision: float
        :param abs_precision: version >= 1
        :type abs_precision: float
        :param imag: version >= 2
        :type imag: float
        :return:
        """
        super().__init__('SCAL', version)

        self.version = version

        self.min = min
        self.max = max
        self.value = value

        # version >= 1
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision

        # version >= 2
        self.imag = imag

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''
        b_min = struct.pack('f', self.min)
        self.binary_body = b_min
        b_max = struct.pack('f', self.max)
        self.binary_body += b_max
        b_value = struct.pack('f', self.value)

        self.binary_body += b_value

        if self.version >= 1:
            b_rel_precision = struct.pack('f', self.rel_precision)
            self.binary_body += b_rel_precision
            b_abs_precision = struct.pack('f', self.abs_precision)
            self.binary_body += b_abs_precision

        if self.version >= 2:
            b_imag = struct.pack('f', self.imag)
            self.binary_body += b_imag

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
        self.min = struct.unpack('f', self.binary_body[:4])[0]
        self.max = struct.unpack('f', self.binary_body[4:8])[0]
        self.value = struct.unpack('f', self.binary_body[8:12])[0]
    
        if self.version >= 1:
            self.rel_precision = struct.unpack('f', self.binary_body[12:16])[0]
            self.abs_precision = struct.unpack('f', self.binary_body[16:20])[0]
    
        if self.version >= 2:
            self.imag = struct.unpack('f', self.binary_body[20:24])[0]

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        self.min = block_dict.get('min', self.min)
        self.max = block_dict.get('max', self.max)
        self.value = block_dict.get('value', self.value)
        self.rel_precision = block_dict.get('rel_precision', self.rel_precision)
        self.abs_precision = block_dict.get('abs_precision', self.abs_precision)
        self.imag = block_dict.get('imag', self.imag)

        return self

    def convert_to_SI(self, user_unit):
        """Convert result to SI if needed
        """
        scal = copy.deepcopy(self)

        scal.min = convert_unit(value=scal.min, src_unit=user_unit)
        scal.max = convert_unit(value=scal.max, src_unit=user_unit)
        scal.value = convert_unit(value=scal.value, src_unit=user_unit)
        scal.rel_precision = convert_unit(value=scal.rel_precision, src_unit=user_unit)
        scal.abs_precision = convert_unit(value=scal.abs_precision, src_unit=user_unit)
        scal.imag = convert_unit(value=scal.imag, src_unit=user_unit)

        return scal
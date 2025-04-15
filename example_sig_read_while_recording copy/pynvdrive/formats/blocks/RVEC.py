from ..blocks.RESULTBLOCK import ResultBlock
from ...quantity.quantity_utils import convert_unit
import struct
import copy


class RVEC(ResultBlock):
    """
    This class represent a RVEC block
    fields:

    - id.
    - version (actual version is 1).
    - block_size.
    - real_min.
    - real_max.
    - data.
    - rel_precision, version >= 1.
    - abs_precision, version >= 1.

    Example::

        rvec = RVEC(real_min=0, real_max=100, data=[1,50,99],
                         rel_precision=1, abs_precision=1)

    """
    def __init__(self, version=1,
                 real_min=None, real_max=None, data=None,
                 rel_precision=None, abs_precision=None):
        """

        :param version:
        :type version: int
        :param real_min:
        :type real_min: float
        :param real_max:
        :type real_max: float
        :param data:
        :type data: list(float)
        :param rel_precision:
        :type rel_precision: float
        :param abs_precision:
        :type abs_precision: float
        :return:
        """
        super().__init__('RVEC', version)

        self.version = version

        self.real_min = real_min
        self.real_max = real_max
        self.data = data
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision

        self.size = None

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        b_real_min = struct.pack('f', self.real_min)
        self.binary_body += b_real_min
        b_real_max = struct.pack('f', self.real_max)
        self.binary_body += b_real_max

        # pos = 1
        for value in self.data:
            b_value = struct.pack('f', value)
            # print('Pos : {}, Float : {}, Hex : {}'.format(pos, value, b_value)) // Debug 0x5C issue
            self.binary_body += b_value
            # pos+=1

        if self.version >= 1:
            b_rel_precision = struct.pack('f', self.rel_precision)
            self.binary_body += b_rel_precision
            b_abs_precision = struct.pack('f', self.abs_precision)
            self.binary_body += b_abs_precision

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
        self.data = []
        self.real_min = struct.unpack('f', self.binary_body[:4])[0]
        self.real_max = struct.unpack('f', self.binary_body[4:8])[0]

        reste = self.binary_body[8:]
        self.size = int(len(reste) / 4)
        if self.version >= 1:
            self.size -= 2

        i = 0
        for i in range(0, self.size):
            temp = struct.unpack('f', reste[i * 4:i * 4 + 4])[0]
            self.data.append(temp)

        reste = reste[i * 4 + 4:]

        if self.version >= 1:
            self.rel_precision = struct.unpack('f', reste[0:4])[0]
            self.abs_precision = struct.unpack('f', reste[4:8])[0]

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        self.real_min = block_dict.get('real_min', self.real_min)
        self.real_max = block_dict.get('real_max', self.real_max)
        self.data = block_dict.get('data', self.data)
        self.rel_precision = block_dict.get('rel_precision', self.rel_precision)
        self.abs_precision = block_dict.get('abs_precision', self.abs_precision)

        return self

    def convert_to_SI(self, user_unit):
        """Convert result to SI if needed
        """
        rvec = copy.deepcopy(self)

        rvec.real_min = convert_unit(value=rvec.real_min, src_unit=user_unit)
        rvec.real_max = convert_unit(value=rvec.real_max, src_unit=user_unit)

        rvec.data = convert_unit(value=rvec.data, src_unit=user_unit)

        if rvec.rel_precision:
            rvec.rel_precision = convert_unit(value=rvec.rel_precision, src_unit=user_unit)
        if rvec.abs_precision:
            rvec.abs_precision = convert_unit(value=rvec.abs_precision, src_unit=user_unit)

        return rvec
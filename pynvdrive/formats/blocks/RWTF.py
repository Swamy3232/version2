from ..blocks.RESULTBLOCK import ResultBlock
from ...quantity.quantity_utils import convert_unit
import struct
import copy


class RWTF(ResultBlock):
    """
    This class represent a RWTF block
    fields:

    - id.
    - version (actual version is 1).
    - block_size.
    - real_min.
    - real_max.
    - vector_size.
    - depth.
    - data.
    - rel_precision, version >= 1.
    - abs_precision, version >= 1.


    Example::

        data = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]

        rwtf = RWTF(real_min=0, real_max=10, data=data,
                         rel_precision=1, abs_precision=1)

    """
    def __init__(self, version=1, real_min=None, real_max=None,
                 data=None, rel_precision=None, abs_precision=None):
        """

        :param version:
        :param real_min:
        :param real_max:
        :param data:
        :type data: list of list of floats
        :param rel_precision:
        :param abs_precision:
        :return:
        """
        super().__init__('RWTF', version)

        self.version = version

        self.real_min = real_min
        self.real_max = real_max
        self.vector_size = None
        self.depth = None
        self.data = data

        # version >= 1
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        b_real_min = struct.pack('f', self.real_min)
        self.binary_body += b_real_min
        b_real_max = struct.pack('f', self.real_max)
        self.binary_body += b_real_max
        b_vector_size = struct.pack('l', self.vector_size)
        self.binary_body += b_vector_size
        b_depth = struct.pack('l', self.depth)
        self.binary_body += b_depth

        for current_vector in self.data:
            for value in current_vector:
                b_value = struct.pack('f', value)
                self.binary_body += b_value

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
        self.real_min = struct.unpack('f', self.binary_body[:4])[0]
        self.real_max = struct.unpack('f', self.binary_body[4:8])[0]
        self.vector_size = struct.unpack('l', self.binary_body[8:12])[0]
        self.depth = struct.unpack('l', self.binary_body[12:16])[0]

        reste = self.binary_body[16:]

        size_byte = self.vector_size * self.depth * 4

        data_byte = reste[:size_byte]

        self.data = []

        for start_current_depth in range(0, size_byte, self.vector_size * 4):
            current_vector = []
            # print(start_current_depth)
            for start_current_vector in range(0, self.vector_size * 4, 4):
                value = struct.unpack('f', data_byte[
                                           start_current_depth + start_current_vector:start_current_depth + start_current_vector + 4])[
                    0]
                current_vector.append(value)
            self.data.append(current_vector)

        reste = reste[size_byte:]

        if self.version >= 1:
            self.rel_precision = struct.unpack('f', reste[0:4])[0]
            self.abs_precision = struct.unpack('f', reste[4:8])[0]

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        # TODO : finish from_dict parsing
        return self

    def convert_to_SI(self, user_unit):
        """Convert result to SI if needed
        """
        rwtf = copy.deepcopy(self)

        rwtf.real_min = convert_unit(value=rwtf.real_min, src_unit=user_unit)
        rwtf.real_max = convert_unit(value=rwtf.real_max, src_unit=user_unit)

        rwtf.data = convert_unit(value=rwtf.data, src_unit=user_unit)

        if rwtf.real_rel_precision:
            rwtf.real_rel_precision = convert_unit(value=rwtf.real_rel_precision, src_unit=user_unit)
        if rwtf.real_abs_precision:
            rwtf.real_abs_precision = convert_unit(value=rwtf.real_abs_precision, src_unit=user_unit)

        return rwtf
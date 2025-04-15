from ..blocks.RESULTBLOCK import ResultBlock
from ...quantity.quantity_utils import convert_unit
import struct
import copy


class CWTF(ResultBlock):
    """
    This class represent a CWTF block
    fields:

    - id.
    - version (actual version is 1).
    - block_size.
    - real_min.
    - real_max.
    - im_min.
    - im_max.
    - vector_size.
    - depth.
    - data.
    - real_rel_precision, version >= 1.
    - real_abs_precision, version >= 1.
    - im_rel_precision, version >= 1.
    - im_abs_precision, version >= 1.


    Example::

        data = [[(0, 1), (1, 1), (2, 1)], [(0, 1), (1, 1), (3, 3)]]

        cwtf = CWTF(real_min=0, real_max=10, im_min=0, im_max=0,
                         data=data, real_rel_precision=1, real_abs_precision=1,
                         im_rel_precision=1, im_abs_precision=1)

    """
    def __init__(self, version=1, real_min=None, real_max=None,
                 im_min=None, im_max=None, data=None,
                 real_rel_precision=None, real_abs_precision=None,
                 im_rel_precision=None, im_abs_precision=None):

        super().__init__('CWTF', version)
        """

        :param version:
        :param real_min:
        :param real_max:
        :param im_min:
        :param im_max:
        :param data: list of list of (float, float)
        :param real_rel_precision:
        :param real_abs_precision:
        :param im_rel_precision:
        :param im_abs_precision:
        :return:
        """
        self.version = version

        self.real_min = real_min
        self.real_max = real_max
        self.im_min = im_min
        self.im_max = im_max
        self.vector_size = None
        self.depth = None
        self.data = data

        # version >= 1
        self.real_rel_precision = real_rel_precision
        self.real_abs_precision = real_abs_precision
        self.im_rel_precision = im_rel_precision
        self.im_abs_precision = im_abs_precision

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        b_real_min = struct.pack('f', self.real_min)
        self.binary_body += b_real_min
        b_real_max = struct.pack('f', self.real_max)
        self.binary_body += b_real_max
        b_im_min = struct.pack('f', self.im_min)
        self.binary_body += b_im_min
        b_im_max = struct.pack('f', self.im_max)
        self.binary_body += b_im_max
        b_vector_size = struct.pack('l', self.vector_size)
        self.binary_body += b_vector_size
        b_depth = struct.pack('l', self.depth)
        self.binary_body += b_depth

        for current_vector in self.data:
            for current_couple_value in current_vector:
                for value in current_couple_value:
                    b_value = struct.pack('f', value)
                    self.binary_body += b_value

        if self.version >= 1:
            b_rel_precision = struct.pack('f', self.real_rel_precision)
            self.binary_body += b_rel_precision
            b_abs_precision = struct.pack('f', self.real_abs_precision)
            self.binary_body += b_abs_precision
            b_im_rel_precision = struct.pack('f', self.im_rel_precision)
            self.binary_body += b_im_rel_precision
            b_im_abs_precision = struct.pack('f', self.im_abs_precision)
            self.binary_body += b_im_abs_precision

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
        self.im_min = struct.unpack('f', self.binary_body[8:12])[0]
        self.im_max = struct.unpack('f', self.binary_body[12:16])[0]
        self.vector_size = struct.unpack('l', self.binary_body[16:20])[0]
        self.depth = struct.unpack('l', self.binary_body[20:24])[0]

        reste = self.binary_body[24:]

        size_byte = self.vector_size * self.depth * 4 * 2

        data_byte = reste[:size_byte]

        self.data = []

        for start_current_depth in range(0, size_byte, self.vector_size * 4 * 2):
            current_vector = []
            # print(start_current_depth)
            for start_current_vector in range(0, self.vector_size * 4 * 2, 4 * 2):
                value_real = struct.unpack('f', data_byte[
                                                start_current_depth + start_current_vector:start_current_depth + start_current_vector + 4])[
                    0]
                value_im = struct.unpack('f', data_byte[
                                              start_current_depth + start_current_vector + 4:start_current_depth + start_current_vector + 8])[
                    0]
                current_vector.append([value_real, value_im])

            self.data.append(current_vector)

        reste = reste[size_byte:]

        if self.version >= 1:
            self.real_rel_precision = struct.unpack('f', reste[0:4])[0]
            self.real_abs_precision = struct.unpack('f', reste[4:8])[0]
            self.im_rel_precision = struct.unpack('f', reste[8:12])[0]
            self.im_abs_precision = struct.unpack('f', reste[12:16])[0]

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
        cwtf = copy.deepcopy(self)

        cwtf.real_min = convert_unit(value=cwtf.real_min, src_unit=user_unit)
        cwtf.real_max = convert_unit(value=cwtf.real_max, src_unit=user_unit)
        cwtf.im_min = convert_unit(value=cwtf.im_min, src_unit=user_unit)
        cwtf.im_max = convert_unit(value=cwtf.im_max, src_unit=user_unit)

        cwtf.data = convert_unit(value=cwtf.data, src_unit=user_unit)

        if cwtf.real_rel_precision:
            cwtf.real_rel_precision = convert_unit(value=cwtf.real_rel_precision, src_unit=user_unit)
        if cwtf.real_abs_precision:
            cwtf.real_abs_precision = convert_unit(value=cwtf.real_abs_precision, src_unit=user_unit)
        if cwtf.im_rel_precision:
            cwtf.im_rel_precision = convert_unit(value=cwtf.im_rel_precision, src_unit=user_unit)
        if cwtf.im_abs_precision:
            cwtf.im_abs_precision = convert_unit(value=cwtf.im_abs_precision, src_unit=user_unit)

        return cwtf
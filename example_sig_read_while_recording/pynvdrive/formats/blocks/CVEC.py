from ..blocks.RESULTBLOCK import ResultBlock
from ...quantity.quantity_utils import convert_unit
import struct
import copy


class CVEC(ResultBlock):
    """
    This class represent a CVEC block
    fields:

    - id.
    - version (actual version is 1).
    - block_size.
    - real_min.
    - real_max.
    - im_min.
    - im_max.
    - data.
    - real_rel_precision, version >= 1.
    - real_abs_precision, version >= 1.
    - im_rel_precision, version >= 1.
    - im_abs_precision, version >= 1.


    Example::

        cvec = CVEC(real_min=0, real_max=100, im_min=0, im_max=100,
                         data=[(1,2),(50,30),(99,6)], real_rel_precision=1,
                         real_abs_precision=1,
                         im_rel_precision=1, im_abs_precision=1)

    """
    def __init__(self, version=1,
                 real_min=None, real_max=None, im_min=None, im_max=None,
                 data=None, real_rel_precision=None, real_abs_precision=None,
                 im_rel_precision=None, im_abs_precision=None):
        """

        :param version:
        :type version: int
        :param real_min:
        :type real_min: float
        :param real_max:
        :type real_max: float
        :param im_min:
        :type im_min: float
        :param im_max:
        :type im_max: float
        :param data: list of complex number as tuple (Re, Im)
        :type data: list((float,float))
        :param real_rel_precision:
        :type real_rel_precision: float
        :param real_abs_precision:
        :type real_abs_precision: float
        :param im_rel_precision:
        :type im_rel_precision: float
        :param im_abs_precision:
        :type im_abs_precision: float
        :return:
        """
        super().__init__('CVEC', version)

        self.version = version

        self.real_min = real_min
        self.real_max = real_max
        self.im_min = im_min
        self.im_max = im_max
        self.data = data
        self.data_real = []
        self.data_imag = []

        self.size = None

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

        for value_couple in self.data:
            b_current_couple = b''
            for value in value_couple:
                b_value = struct.pack('f', value)
                b_current_couple += b_value
            self.binary_body += b_current_couple

        if self.version >= 1:
            b_real_rel_precision = struct.pack('f', self.real_rel_precision)
            self.binary_body += b_real_rel_precision
            b_real_abs_precision = struct.pack('f', self.real_abs_precision)
            self.binary_body += b_real_abs_precision
            b_im_rel_precision = struct.pack('f', self.im_rel_precision)
            self.binary_body += b_im_rel_precision
            b_im_abs_precision = struct.pack('f', self.im_abs_precision)
            self.binary_body += b_im_abs_precision

        self.get_binary_header()

        return self.binary_header + self.binary_body

    def from_binary(self, contents, size):
        """Parse binary block
        """
        self.binary_header = contents[:6]
        self.binary_body = contents[6:]

        self.size = size

        self.parse_header()
        self.parse_body()


    def parse_body(self):
        """Parse binary body to individuals attributes
        """
        self.real_min = struct.unpack('f', self.binary_body[:4])[0]
        self.real_max = struct.unpack('f', self.binary_body[4:8])[0]
        self.im_min = struct.unpack('f', self.binary_body[8:12])[0]
        self.im_max = struct.unpack('f', self.binary_body[12:16])[0]

        reste = self.binary_body[16:]
        data_temp = []
        i=0
        for i in range(0, self.size * 2):
            temp = struct.unpack('f', reste[i * 4:i * 4 + 4])[0]
            data_temp.append(temp)
        reste = reste[i * 4 + 4:]

        real_part = True
        data_real = []
        data_imag = []
        for i in data_temp:
            if real_part:
                real_part = False
                data_real.append(i)
            else:
                real_part = True
                data_imag.append(i)

        self.data = None
        if len(data_real) == len(data_imag):
            self.data = []
            for i in range(0, len(data_real)):
                self.data.append([data_real[i], data_imag[i]])

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

        self.real_min = block_dict.get('real_min', self.real_min)
        self.real_max = block_dict.get('real_max', self.real_max)
        self.im_min = block_dict.get('im_min', self.im_min)
        self.im_max = block_dict.get('im_max', self.im_max)

        self.data = block_dict.get('data', self.data)

        self.data_real = []
        self.data_imag = []

        self.size = block_dict.get('size', self.size)

        # version >= 1
        self.real_rel_precision = block_dict.get('real_rel_precision', self.real_rel_precision)
        self.real_abs_precision = block_dict.get('real_abs_precision', self.real_abs_precision)
        self.im_rel_precision = block_dict.get('im_rel_precision', self.im_rel_precision)
        self.im_abs_precision = block_dict.get('im_abs_precision', self.im_abs_precision)

        return self

    def convert_to_SI(self, user_unit):
        """Convert cvec to SI if needed
        """
        cvec = copy.deepcopy(self)
        cvec.real_min = convert_unit(value=cvec.real_min, src_unit=user_unit)
        cvec.real_max = convert_unit(value=cvec.real_max, src_unit=user_unit)
        cvec.im_min = convert_unit(value=cvec.im_min, src_unit=user_unit)
        cvec.im_max = convert_unit(value=cvec.im_max, src_unit=user_unit)

        cvec.data = convert_unit(value=cvec.data, src_unit=user_unit)

        if cvec.real_rel_precision:
            cvec.real_rel_precision = convert_unit(value=cvec.real_rel_precision, src_unit=user_unit)
        if cvec.real_abs_precision:
            cvec.real_abs_precision = convert_unit(value=cvec.real_abs_precision, src_unit=user_unit)
        if cvec.im_rel_precision:
            cvec.im_rel_precision = convert_unit(value=cvec.im_rel_precision, src_unit=user_unit)
        if cvec.im_abs_precision:
            cvec.im_abs_precision = convert_unit(value=cvec.im_abs_precision, src_unit=user_unit)

        return cvec
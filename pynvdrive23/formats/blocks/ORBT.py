from ..blocks.RESULTBLOCK import ResultBlock
import struct


class ORBT(ResultBlock):
    """
    ORBT block contains the array of number of points per revolution.
    Important note: This block is used only for “orbit result” (i.e raw or synthetized orbit).
    This class represent an ORBT block
    fields:

    - id.
    - version (actual version is 1).
    - block_size.
    - array_size.
    - nb_points_per_rev_array.

    Example::

        orbit = ORBIT(array_size=2, nb_points_per_rev_array=[49,51])
        The second element in the NbPointPerRevTab array is the number of points contained in the second revolution of the result.

    """
    def __init__(self, version=1,
                 array_size=None, nb_points_per_rev_array=None):
        """

        :param version:
        :type version: int
        :param array_size:
        :type array_size: float
        :param nb_points_per_rev_array:
        :type nb_points_per_rev_array: list(float)
        :return:
        """
        super().__init__('ORBT', version)

        self.version = version

        if nb_points_per_rev_array is None:
            self.nb_points_per_rev_array = []
        else:
            self.nb_points_per_rev_array = nb_points_per_rev_array

        self.array_size = array_size

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        self.array_size = len(self.nb_points_per_rev_array)
        b_array_size = struct.pack('l', self.array_size)
        self.binary_body += b_array_size

        for value in self.nb_points_per_rev_array:
            b_value = struct.pack('f', value)
            self.binary_body += b_value

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
        self.array_size = struct.unpack('l', self.binary_body[:4])[0]
        reste = self.binary_body[4:]
        for i in range(0, self.array_size):
            temp = struct.unpack('f', reste[i * 4:i * 4 + 4])[0]
            self.nb_points_per_rev_array.append(temp)

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        self.array_size = block_dict.get('array_size', self.array_size)
        self.nb_points_per_rev_array = block_dict.get('nb_points_per_rev_array', self.nb_points_per_rev_array)

        return self

    def convert_to_SI(self):
        """Convert result to SI if needed
        """
        return self
from ..blocks.RESULTBLOCK import ResultBlock, b_str_EOL, BlockUnconsistent
from pynvdrive import ENCODING_MBCS
import struct
from pynvdrive.command import Command


class HEAD(ResultBlock):
    """
    This class represent a HEAD block
    fields:

    - id.
    - version (actual version is 5).
    - block_size (it will be automatically filled at serialization time).
    - result_type.
    - size.
    - dimension.
    - is_complex.
    - measure_status.
    - physical_quantity.
    - unit_name.
    - unit_label.
    - name.
    - overall_level_status, for version = 1 or 2.
    - weighted_ol_status, for version = 1 or 2.
    - weighting_window, for version >= 4.
    - magnitude_key, for version >= 5.

    Example::

        head = HEAD(result_type=1, size=1, dimension=1, complex=False,
                         measure_status=2, quantity_key='Potential_Difference',
                         name='myresult', weighting_window=316)

    """
    def __init__(self, version=5,
                 result_type=None, size=None, dimension=None,
                 is_complex=None, measure_status=None,
                 physical_quantity=None, unit_name=None, unit_label=None,
                 name=None, overall_level_status=None,
                 weighted_ol_status=None, weighting_window=None, magnitude_key=None):
        """

        :param version:
        :type version: int
        :param result_type: 1 Scalar, 2 RegVector, 3 RefVector, 8 Waterfall
        :type result_type: int
        :param size:
        :type size: int
        :param dimension:
        :type dimension: int
        :param is_complex:
        :type is_complex: int
        :param measure_status: 0 if no measurement, 1 if measurement in progress, 2 if measurement finished
        :type measure_status: int
        :param physical_quantity:
        :type physical_quantity: str
        :param unit_name:
        :type unit_name: str
        :param unit_label:
        :type unit_label: str
        :param name:
        :type name: str
        :param overall_level_status: for version = 1 or 2
        :type overall_level_status: short
        :param weighted_ol_status: for version = 1 or 2
        :type weighted_ol_status: short
        :param weighting_window: for version >= 4
        :type weighting_window: int
        :param magnitude_key: for version >=5
        :type magnitude_key: str
        :return:
        """

        super().__init__('HEAD', version)

        self.version = version

        self.result_type = result_type

        self.size = size
        self.dimension = dimension
        self.is_complex = is_complex
        self.measure_status = measure_status
        self.physical_quantity = physical_quantity
        self.unit_name = unit_name
        self.unit_label = unit_label
        self.name = name
        self.overall_level_status = overall_level_status
        self.weighted_ol_status = weighted_ol_status
        self.weighting_window = weighting_window
        self.magnitude_key = magnitude_key
        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        b_result_type = struct.pack('h', self.result_type)
        self.binary_body += b_result_type

        b_size = struct.pack('l', self.size)
        self.binary_body += b_size
        b_dimension = struct.pack('h', self.dimension)
        self.binary_body += b_dimension
        b_complex = struct.pack('h', self.is_complex)
        self.binary_body += b_complex
        b_measure_status = struct.pack('h', self.measure_status)
        self.binary_body += b_measure_status

        b_physical_quantity = bytes(self.physical_quantity, ENCODING_MBCS, errors='replace') + b_str_EOL
        self.binary_body += b_physical_quantity
        b_unit_name = bytes(self.unit_name, ENCODING_MBCS, errors='replace') + b_str_EOL
        self.binary_body += b_unit_name
        b_unit_label = bytes(self.unit_label, ENCODING_MBCS, errors='replace') + b_str_EOL
        self.binary_body += b_unit_label
        b_name = bytes(self.name, ENCODING_MBCS, errors='replace') + b_str_EOL
        self.binary_body += b_name

        if 1 <= self.version < 3:
            b_overall_level_status = struct.pack('h', self.overall_level_status)
            self.binary_body += b_overall_level_status
            b_weighted_ol_status = struct.pack('h', self.weighted_ol_status)
            self.binary_body += b_weighted_ol_status
        if self.version >= 4:
            b_weighting_window = struct.pack('H', self.weighting_window)
            self.binary_body += b_weighting_window
        if self.version >= 5:
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

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)
        self.result_type = block_dict.get('result_type', self.result_type)
        self.size = block_dict.get('size', self.size)
        self.dimension = block_dict.get('dimension', self.dimension)
        self.is_complex = block_dict.get('is_complex', self.is_complex)
        self.measure_status = block_dict.get('measure_status', self.measure_status)
        self.physical_quantity = block_dict.get('physical_quantity', self.physical_quantity)
        self.unit_name = block_dict.get('unit_name', self.unit_name)
        self.unit_label = block_dict.get('unit_label', self.unit_label)
        self.name = block_dict.get('name', self.name)
        self.overall_level_status = block_dict.get('overall_level_status', self.overall_level_status)
        self.weighted_ol_status = block_dict.get('weighted_ol_status', self.weighted_ol_status)
        self.weighting_window = block_dict.get('weighting_window', self.weighting_window)
        self.magnitude_key = block_dict.get('magnitude_key', self.magnitude_key)

        return self

    def parse_body(self):
        """Parse binary body to individuals attributes
        """
        self.result_type = struct.unpack('h', self.binary_body[:2])[0]
        self.size = struct.unpack('l', self.binary_body[2:6])[0]
        self.dimension = struct.unpack('h', self.binary_body[6:8])[0]
        self.is_complex = struct.unpack('h', self.binary_body[8:10])[0]
        self.measure_status = struct.unpack('h', self.binary_body[10:12])[0]
        reste = self.binary_body[12:]
        reste = reste.split(b'\0', 4)

        self.physical_quantity = Command.parse_response_string(reste[0])
        self.unit_name = Command.parse_response_string(reste[2])
        self.unit_label = Command.parse_response_string(reste[1])
        self.name = Command.parse_response_string(reste[3])
        reste = reste[4:][0]

        if 1 <= self.version < 3:
            self.overall_level_status = struct.unpack('h', reste[0:2])[0]
            self.weighted_ol_status = struct.unpack('h', reste[2:4])[0]
        if self.version >= 4:
            self.weighting_window = struct.unpack('H', reste[0:2])[0]
            reste = reste[2:]
        if self.version >= 5:
            reste = reste.split(b'\0')
            self.magnitude_key = Command.parse_response_string(reste[0])

    def convert_to_SI(self):
        """Convert result to SI if needed
        """
        return self

    def check_consistency(self):
        """Check if all attributes are set for parsing
        """
        # Checking minimum attributes are there
        if not isinstance(self.version, int):
            raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'version'))
        if self.result_type not in [1, 2, 3, 8]:
            raise BlockUnconsistent('{} {} must be a valid value'.format(self.__class__.__name__, 'result_type'))
        if not isinstance(self.size, int):
            raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'size'))
        if self.dimension not in [1, 2, 3]:
            raise BlockUnconsistent('{} {} must be a valid value'.format(self.__class__.__name__, 'dimension'))
        if not isinstance(self.is_complex, int):
            raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'is_complex'))
        if self.measure_status not in [0, 1, 2]:
            raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'measure_status'))

        # Units

        # Others
        if 1 <= self.version < 3:
            if not isinstance(self.overall_level_status, int):
                raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'overall_level_status'))
            if not isinstance(self.weighted_ol_status, int):
                raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'weighted_ol_status'))
        if self.version >= 4:
            if not isinstance(self.weighting_window, int):
                raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'weighting_window')) #TODO use a dict for weightingwindows
        if self.version >= 5:
            if not isinstance(self.magnitude_key, str):
                raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'magnitude_key')) #TODO with units
        else:  # If magnitude key, does not matters others units attributes
            if not isinstance(self.physical_quantity, str):
                raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'physical_quantity')) #TODO with units
            if not isinstance(self.unit_name, str):
                raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'unit_name')) #TODO with units
            if not isinstance(self.unit_label, str):
                raise BlockUnconsistent('{} {} missing or not valid type'.format(self.__class__.__name__, 'unit_label')) #TODO with units
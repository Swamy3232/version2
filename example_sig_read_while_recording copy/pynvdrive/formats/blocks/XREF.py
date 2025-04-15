from ..blocks.RESULTBLOCK import ResultBlock, b_str_EOL
from pynvdrive import ENCODING_MBCS
from ...quantity.quantity_utils import convert_unit
import struct
import copy
from pynvdrive.command import Command


class Reference:
    """
    This class represent a reference as described in a XREF block:
        - vec_name (Reference name)
        - physical_quantity
        - unit_name
        - unit_label
        - data
        - rel_precision (version >= 1)
        - abs_precision (version >= 1)
        - min (version >=2)
        - max (version >=2)
        - magnitude_key (version >=3)
    """
    def __init__(self, vec_name, physical_quantity, unit_name, unit_label, data, rel_precision, abs_precision, min=None, max=None, magnitude_key=None):
        """

        :param vec_name:
        :type vec_name: str
        :param physical_quantity:
        :type physical_quantity: str
        :param unit_name: If empty, retrieved from quantity key
        :type unit_name: str
        :param unit_label: If empty, retrieved from quantity key
        :type unit_label: str
        :param data:
        :type data: list(float)
        :param rel_precision:
        :type rel_precision: float
        :param abs_precision:
        :type abs_precision: float
        :param min:
        :type min: float
        :param max:
        :type max: float
        :return:
        """
        self.vec_name = vec_name
        self.physical_quantity = physical_quantity
        self.unit_name = unit_name
        self.unit_label = unit_label
        self.data = data

        # version >= 1
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision

        # version >= 2
        self.min = min
        self.max = max

        # version >= 3
        self.magnitude_key = magnitude_key

    def to_dict(self):
        """
        Convert the reference to a dict
        :return:
        """
        return {
            'vec_name': self.vec_name,
            'physical_quantity': self.physical_quantity,
            'unit_name': self.unit_name,
            'unit_label': self.unit_label,
            'data': self.data,
            'rel_precision': self.rel_precision,
            'abs_precision': self.abs_precision,
            'min': self.min,
            'max': self.max,
            'magnitude_key': self.magnitude_key
        }

    @classmethod
    def from_dict(cls, reference_dict):
        """
        Create a reference from a dict
        :param reference_dict:
        :type reference_dict: dict
        :return:
        """
        return cls(
            vec_name=reference_dict['vec_name'],
            physical_quantity=reference_dict['physical_quantity'],
            unit_name=reference_dict['unit_name'],
            unit_label=reference_dict['unit_label'],
            data=reference_dict['data'],
            rel_precision=reference_dict['rel_precision'],
            abs_precision=reference_dict['abs_precision'],
            min=reference_dict['min'],
            max=reference_dict['max'],
            magnitude_key=reference_dict['magnitude_key']
        )


class XREF(ResultBlock):
    """
    This class represent a XREF block
    fields:

    - id.
    - version (actual version is 3).
    - block_size.
    - nb_ref.
    - nb_ref * references.


    Example:

        xref = XREF(list_references=[my_ref1, my_ref2])

    """
    def __init__(self, version=3, list_references=None):
        """

        :param version:
        :type version: int
        :param list_references:
        :type list_references: list(Reference)
        :return:
        """
        super().__init__('XREF', version)

        if list_references is None:
            self.list_references = []
        else:
            self.list_references = list_references
        self.version = version

        self.size = None

        self.nbRef = None

        return

    def to_binary(self):
        """Generate binary block using attributes
        """
        self.binary_body = b''

        self.nbRef = len(self.list_references)
        b_nbRef = struct.pack('h', self.nbRef)
        self.binary_body += b_nbRef

        for current_ref in self.list_references:
            b_current_ref = b''
            b_vec_name = bytes(current_ref.vec_name, ENCODING_MBCS, errors='replace') + b_str_EOL
            b_current_ref += b_vec_name
            b_physical_quantity = bytes(current_ref.physical_quantity, ENCODING_MBCS, errors='replace') + b_str_EOL
            b_current_ref += b_physical_quantity
            b_unit_name = bytes(current_ref.unit_name, ENCODING_MBCS, errors='replace') + b_str_EOL
            b_current_ref += b_unit_name
            b_unit_label = bytes(current_ref.unit_label, ENCODING_MBCS, errors='replace') + b_str_EOL
            b_current_ref += b_unit_label

            for value in current_ref.data:
                b_value = struct.pack('f', value)
                b_current_ref += b_value

            if self.version >= 1:
                b_rel_precision = struct.pack('f', current_ref.rel_precision)
                b_current_ref += b_rel_precision
                b_abs_precision = struct.pack('f', current_ref.abs_precision)
                b_current_ref += b_abs_precision

            if self.version >= 2:
                b_min = struct.pack('f', current_ref.min)
                b_current_ref += b_min
                b_max = struct.pack('f', current_ref.max)
                b_current_ref += b_max

            if self.version >= 3:
                b_magnitude_key = bytes(current_ref.magnitude_key, ENCODING_MBCS, errors='replace') + b_str_EOL
                b_current_ref += b_magnitude_key

            self.binary_body += b_current_ref

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
        self.nbRef = struct.unpack('h', self.binary_body[:2])[0]

        reste = self.binary_body[2:]

        # data
        self.list_references = []
        for i in range(0, self.nbRef):
            ref = Reference(vec_name='', physical_quantity='', unit_name='', unit_label='', data=[], rel_precision=0.0, abs_precision=0.0)

            reste = reste.split(b'\0', 4)

            ref.vec_name = Command.parse_response_string(reste[0])
            ref.physical_quantity = Command.parse_response_string(reste[1])
            ref.unit_name = Command.parse_response_string(reste[3])
            ref.unit_label = Command.parse_response_string(reste[2])

            reste = reste[-1]
            ref.data = []
            it=0
            for it in range(0, self.size):
                temp = struct.unpack('f', reste[it * 4:it * 4 + 4])[0]
                ref.data.append(temp)

            reste = reste[it * 4 + 4:]

            if self.version >= 1:
                ref.rel_precision = struct.unpack('f', reste[0:4])[0]
                ref.abs_precision = struct.unpack('f', reste[4:8])[0]

                reste = reste[8:]

            if self.version >= 2:
                ref.min = struct.unpack('f', reste[0:4])[0]
                ref.max = struct.unpack('f', reste[4:8])[0]

                reste = reste[8:]

            if self.version >= 3:
                reste = reste.split(b'\0', 1)
                ref.magnitude_key = Command.parse_response_string(reste[0])
                reste = reste[1]

            self.list_references.append(ref)

    def from_dict(self, block_dict: dict):
        """Convert a dictionary to a block
        :param block_dict: block dictionary
        :return:
        """
        self.version = block_dict.get('version', self.version)

        self.size = block_dict.get('size', self.size)
        self.nbRef = block_dict.get('nbRef', self.nbRef)

        self.list_references = []
        for reference in block_dict['list_references']:
            self.list_references.append(Reference.from_dict(reference))

        return self

    def convert_to_SI(self, quantity_provider):
        """Convert result to SI if needed
        """
        xref = copy.deepcopy(self)

        for reference in xref.list_references:
            user_unit = self.check_unit_exist(quantity_provider=quantity_provider, magnitude_key=reference.magnitude_key, physical_quantity=reference.physical_quantity, unit_name=reference.unit_name, unit_label=reference.unit_label)
            reference.magnitude_key = user_unit.magnitude_key
            reference.physical_quantity = user_unit.magnitude_name
            reference.unit_name = user_unit.unit_name
            reference.unit_name = user_unit.unit_label

            reference.data = convert_unit(value=reference.data, src_unit=user_unit)

            if reference.rel_precision:
                reference.rel_precision = convert_unit(value=reference.rel_precision, src_unit=user_unit)
            if reference.abs_precision:
                reference.abs_precision = convert_unit(value=reference.abs_precision, src_unit=user_unit)

            if reference.min:
                reference.min = convert_unit(value=reference.min, src_unit=user_unit)
            if reference.max:
                reference.max = convert_unit(value=reference.max, src_unit=user_unit)

        return xref
import logging
from datetime import datetime

from orostk.nvdrive.result_utils import FieldType
from orostk.nvdrive.nvdrive_exceptions import IncompleteBlockException
from orostk.nvdrive.nvd_utils import extract_byte_size
from orostk.quantity import q_provider

nvdrive_logger = logging.getLogger('NVDriveLogger')


class ResultBlock(object):
    """
    This class represents a result block
    It's a generic class to construct all classes
    defined below
    fields:

    - id.
    - version.
    - block_size.
    """

    def __init__(self, block_id=None, version=None, quantity_provider='local'):
        """

        :param block_id:
        :type block_id: str
        :param version:
        :type version: int
        :return:
        """
        self.id = block_id
        self.version = version
        self.block_size = None
        self.header_size = None
        self._serialized_body = []
        self._serialized_header = []
        if quantity_provider == 'local':
            self._quantity_provider = q_provider
        else:
            self._quantity_provider = None

    def append_serialized_body(self, member, field_type, min_version=0):
        """

        :param member: member to serialize
        :param field_type:  type of the member
        :type field_type: FieldType
        :param min_version: if needed, the minimum version
        :return:
        """
        if self.version >= min_version and member is not None:
            self._serialized_body.append((member, field_type))
            return True
        elif self.version < min_version and member is not None:
            return False
        else:
            raise IncompleteBlockException('Block field missing')

    def serialize_header(self):
        """ Put the header fields of the block in a list
        For each field we put a tuple containing:
         (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_header = []
        if self.id is not None:
            self._serialized_header.append((self.id, FieldType.FSTRING))
        else:
            raise IncompleteBlockException('Block id missing')
        if self.version is not None:
            self._serialized_header.append((self.version, FieldType.SHORT))
        else:
            raise IncompleteBlockException('Block version missing')
        if self.block_size is not None:
            self._serialized_header.append((self.block_size, FieldType.LONG))
        else:
            raise IncompleteBlockException('Block size missing')

        return self._serialized_header

    def serialize_body(self):
        """ Put the body fields of the block in a list
        For each field we put a tuple containing:
         (field, field_type)

        :return: A list of the fields as described above
        """
        return self._serialized_body

    def serialize(self):
        """ Put the fields of the block in a list
        For each field we put a tuple containing:
         (field, field_type)

        :return: A list of the fields as described above
        """
        # body has to be generated before header because it
        # calculate the block_size
        body = self.serialize_body()
        self.block_size = extract_byte_size(self._serialized_body)
        header = self.serialize_header()
        self.header_size = extract_byte_size(self._serialized_header)
        return header + body

    @property
    def total_size(self):
        if self.block_size is not None and self.header_size is not None:
            nvdrive_logger.debug(
                'Total size of the block {} in bytes: {}'
                .format(self.id, self.block_size + self.header_size))
            return self.block_size + self.header_size
        else:
            nvdrive_logger.warning("Can't retrieve the size of block")
            return None


class HeadBlock(ResultBlock):
    """
    This class represents a HEAD block
    fields:

    - id.
    - version (actual version is 5).
    - block_size (it will be automatically filled at serialization time).
    - result_type.
    - size.
    - dimension.
    - complex.
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

        head = HeadBlock(result_type=1, size=1, dimension=1, complex=False,
                         measure_status=2, quantity_key='Potential_Difference',
                         name='myresult', weighting_window=316)

    """

    def __init__(self, version=5,
                 result_type=None, size=None, dimension=None,
                 is_complex=None, measure_status=None,
                 quantity_key=None, unit_name=None, unit_label=None,
                 name=None, overall_level_status=None,
                 weighted_ol_status=None, weighting_window=None):
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
        :type is_complex: bool
        :param measure_status:
        :type measure_status: int
        :param quantity_key:
        :type quantity_key: str
        :param unit_name:
        :type unit_name: str
        :param unit_label:
        :type unit_label: str
        :param name:
        :type name: str
        :param overall_level_status: for version = 1 or 2
        :type overall_level_status: int
        :param weighted_ol_status: for version = 1 or 2
        :type weighted_ol_status: int
        :param weighting_window: for version >= 4
        :type weighting_window: int
        :return:
        """
        super().__init__('HEAD', version)
        self.result_type = result_type
        self.size = size
        self.dimension = dimension
        self.complex = is_complex
        self.measure_status = measure_status
        if quantity_key:
            self._quantity_provider.is_consistent(quantity_key,
                                                  unit_name,
                                                  unit_label)
        self.quantity_key = quantity_key
        if unit_name is None and self.quantity_key:
            self.unit_name = self._quantity_provider.get_si_unit_name(
                self.quantity_key
            )
        else:
            self.unit_name = unit_name
        if unit_label is None and self.quantity_key:
            self.unit_label = self._quantity_provider.get_unit_label(
                self.unit_name
            )
        else:
            self.unit_label = unit_label
        self.name = name
        if self.version and self.version in [1, 2]:
            self.overall_level_status = overall_level_status
            self.weighted_ol_status = weighted_ol_status
        if self.version and self.version >= 4:
            self.weighting_window = weighting_window

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []
        self.append_serialized_body(self.result_type, FieldType.SHORT)
        self.append_serialized_body(self.size, FieldType.LONG)
        self.append_serialized_body(self.dimension, FieldType.SHORT)
        if self.complex:
            self.append_serialized_body(1, FieldType.SHORT)
        else:
            self.append_serialized_body(0, FieldType.SHORT)
        self.append_serialized_body(self.measure_status, FieldType.SHORT)
        self.append_serialized_body(self.quantity_key, FieldType.STRING)
        self.append_serialized_body(self.unit_name, FieldType.STRING)
        self.append_serialized_body(self.unit_label, FieldType.STRING)
        self.append_serialized_body(self.name, FieldType.STRING)
        if self.version is not None and self.version in [1, 2]:
            self.append_serialized_body(
                self.overall_level_status, FieldType.SHORT
            )
            self.append_serialized_body(
                self.weighted_ol_status, FieldType.SHORT
            )
        self.append_serialized_body(
            self.weighting_window, FieldType.USHORT, min_version=4
        )
        # Retro compatibility with magnitude key
        self.append_serialized_body(
            self.quantity_key, FieldType.STRING, min_version=5
        )
        return self._serialized_body

    def is_SI(self):
        """
        Check if the block is SI
        :return: True if is SI, else False
        """
        if self.quantity_key is None or self.unit_name is None:
            raise IncompleteBlockException(
                "Can't check if the block is in SI, missing quantity_key"
                " or unit_name"
            )
        return q_provider.get_si_unit_name(self.quantity_key) == self.unit_name


class InfoBlock(ResultBlock):
    """
    This class represents an INFO block
    fields:

    - id.
    - version (actual version is 1).
    - block_size.
    - info_mask.
    - global_level.
    - weighted_global_level.
    - tacho.
    - date.

    Example::

        info = InfoBlock(version=1, info_mask=1, global_level=1,
                         weighted_global_level=0, tacho=0)

    """

    def __init__(self, version=1,
                 info_mask=0x1, global_level=0,
                 weighted_global_level=0, tacho=0,
                 date=None):
        """

        :param version:
        :type version: int
        :param info_mask: An integer representing an
        InfoMask as described in NVDrive documentation
        :type info_mask: int
        :param global_level:
        :type global_level: float
        :param weighted_global_level:
        :type weighted_global_level: float
        :param tacho:
        :type tacho: float
        :param date: Date in UTC
        :type date: datetime
        :return:
        """
        super().__init__('INFO', version)
        self.info_mask = info_mask
        self.global_level = global_level
        self.weighted_global_level = weighted_global_level
        self.tacho = tacho
        # The date is in UTC
        self.date = date if date is not None else datetime(1601, 1, 1)

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []
        self.append_serialized_body(self.info_mask, FieldType.LONG)
        self.append_serialized_body(self.global_level, FieldType.FLOAT)
        self.append_serialized_body(self.weighted_global_level,
                                    FieldType.FLOAT)
        self.append_serialized_body(self.tacho, FieldType.FLOAT)
        self.append_serialized_body(self.date, FieldType.DATE)
        return self._serialized_body


class ScalBlock(ResultBlock):
    """
    This class represents a SCAL block
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

        scal = ScalBlock(min=0, max=100, value=50,
                         rel_precision=0.1, abs_precision=0.1)

    """

    def __init__(self, version=2,
                 v_min=None, v_max=None, value=None,
                 rel_precision=None, abs_precision=None, imag=0):
        """

        :param version:
        :type version: int
        :param v_min:
        :type v_min: float
        :param v_max:
        :type v_max: float
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
        self.min = v_min
        self.max = v_max
        self.value = value
        if self.version is not None and self.version >= 1:
            self.rel_precision = rel_precision
            self.abs_precision = abs_precision
        if self.version is not None and self.version >= 2:
            self.imag = imag

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []
        self.append_serialized_body(self.min, FieldType.FLOAT)
        self.append_serialized_body(self.max, FieldType.FLOAT)
        self.append_serialized_body(self.value, FieldType.FLOAT)
        self.append_serialized_body(self.rel_precision,
                                    FieldType.FLOAT,
                                    min_version=1)
        self.append_serialized_body(self.abs_precision,
                                    FieldType.FLOAT,
                                    min_version=1)
        self.append_serialized_body(self.imag,
                                    FieldType.FLOAT,
                                    min_version=2)
        return self._serialized_body


class XregBlock(ResultBlock):
    """
    This class represents a XREG block
    fields:

    - id.
    - version (actual version is 3).
    - block_size.
    - start.
    - stop.
    - n_octave.
    - quantity_key.
    - unit_name.
    - unit_label.
    - rel_precision, version >= 1.
    - abs_precision, version >= 1.
    - magnitude_key, version >= 3.

    Example::

        xreg = XregBlock(start=0, stop=100, n_octave=1, quantity_key='Time',
                         rel_precision=1, abs_precision=1)

    """

    def __init__(self, version=3,
                 start=None, stop=None, n_octave=None, quantity_key=None,
                 unit_name=None, unit_label=None, rel_precision=None,
                 abs_precision=None):
        """

        :param version:
        :type version: int
        :param start:
        :type start: float
        :param stop:
        :type stop: float
        :param n_octave:
        :type n_octave: float
        :param quantity_key:
        :type quantity_key: str
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
        self.start = start
        self.stop = stop
        self.n_octave = n_octave
        if quantity_key:
            self._quantity_provider.is_consistent(quantity_key,
                                                  unit_name,
                                                  unit_label)
        self.quantity_key = quantity_key
        if unit_name is None and self.quantity_key:
            self.unit_name = self._quantity_provider.get_si_unit_name(
                self.quantity_key
            )
        else:
            self.unit_name = unit_name
        if unit_label is None and self.quantity_key:
            self.unit_label = self._quantity_provider.get_unit_label(
                self.unit_name
            )
        else:
            self.unit_label = unit_label
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []
        self.append_serialized_body(self.start, FieldType.FLOAT)
        self.append_serialized_body(self.stop, FieldType.FLOAT)
        self.append_serialized_body(self.n_octave, FieldType.SHORT)
        self.append_serialized_body(self.quantity_key, FieldType.STRING)
        self.append_serialized_body(self.unit_name, FieldType.STRING)
        self.append_serialized_body(self.unit_label, FieldType.STRING)
        self.append_serialized_body(self.rel_precision,
                                    FieldType.FLOAT,
                                    min_version=1)
        self.append_serialized_body(self.abs_precision,
                                    FieldType.FLOAT,
                                    min_version=1)
        # Retro compatibility with magnitude key
        self.append_serialized_body(self.quantity_key,
                                    FieldType.STRING,
                                    min_version=3)

        return self._serialized_body

    def is_SI(self):
        """
        Check if the block is SI
        :return: True if is SI, else False
        """
        if self.quantity_key is None or self.unit_name is None:
            raise IncompleteBlockException(
                "Can't check if the block is in SI, missing quantity_key"
                " or unit_name"
            )
        return q_provider.get_si_unit_name(self.quantity_key) == self.unit_name


class RvecBlock(ResultBlock):
    """
    This class represents a RVEC block
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

        rvec = RvecBlock(real_min=0, real_max=100, data=[1,50,99],
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
        self.real_min = real_min
        self.real_max = real_max
        if data is not None:
            # copy the list
            self.data = list(data)
        else:
            self.data = data
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []
        self.append_serialized_body(self.real_min, FieldType.FLOAT)
        self.append_serialized_body(self.real_max, FieldType.FLOAT)
        self.append_serialized_body(self.data, FieldType.V_FLOAT)
        self.append_serialized_body(self.rel_precision,
                                    FieldType.FLOAT,
                                    min_version=1)
        self.append_serialized_body(self.abs_precision,
                                    FieldType.FLOAT,
                                    min_version=1)

        return self._serialized_body


class CvecBlock(ResultBlock):
    """
    This class represents a CVEC block
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

        cvec = CvecBlock(real_min=0, real_max=100, im_min=0, im_max=100,
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
        self.real_min = real_min
        self.real_max = real_max
        self.im_min = im_min
        self.im_max = im_max
        if data is not None:
            # copy the list
            self.data = list(data)
        else:
            self.data = data
        self.real_rel_precision = real_rel_precision
        self.im_rel_precision = im_rel_precision
        self.real_abs_precision = real_abs_precision
        self.im_abs_precision = im_abs_precision

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []
        self.append_serialized_body(self.real_min, FieldType.FLOAT)
        self.append_serialized_body(self.real_max, FieldType.FLOAT)
        self.append_serialized_body(self.im_min, FieldType.FLOAT)
        self.append_serialized_body(self.im_max, FieldType.FLOAT)
        self.append_serialized_body(self.data, FieldType.V_TUPLE_FLOAT)
        self.append_serialized_body(self.real_rel_precision,
                                    FieldType.FLOAT,
                                    min_version=1)
        self.append_serialized_body(self.real_abs_precision,
                                    FieldType.FLOAT,
                                    min_version=1)
        self.append_serialized_body(self.im_rel_precision,
                                    FieldType.FLOAT,
                                    min_version=1)
        self.append_serialized_body(self.im_abs_precision,
                                    FieldType.FLOAT,
                                    min_version=1)

        return self._serialized_body


class XrefBlock(ResultBlock):
    """
    This class represents a XREF block
    fields:

    - id.
    - version (actual version is 3).
    - block_size.
    - nb_ref.
    - nb_ref * references.


    Example:

        xref = XrefBlock(references=[my_ref1, my_ref2])

    """

    def __init__(self, version=3, references=None):
        """

        :param version:
        :type version: int
        :param references:
        :type references: list(Reference)
        :return:
        """
        super().__init__('XREF', version)
        if references is not None:
            # copy the list
            self.references = list(references)
        else:
            self.references = references

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []
        if not self.references:
            raise IncompleteBlockException('XREF block needs references')
        self.append_serialized_body(len(self.references), FieldType.SHORT)
        for ref in self.references:
            self._serialized_body += ref.serialize(self.version)

        return self._serialized_body

    def is_SI(self):
        """
        Check if the block is SI
        :return: True if is SI, else False
        """
        if len(self.references) == 0:
            raise IncompleteBlockException(
                "Can't check if the block is in SI, the block has no reference"
            )
        for ref in self.references:
            if not ref.is_SI():
                return False
        else:
            return True


class DwtfBlock(ResultBlock):
    """
    This class represents a DWTF block
    fields:

    - id.
    - version (actual version is 0).
    - block_size.
    - process_id.
    - first_index.
    - last_index.
    - request_status.


    Example::

        dwtf = DwtfBlock(process_id=187, first_index=0, last_index=100,
                         request_status=0)

    """

    def __init__(self, version=0, process_id=None, first_index=None,
                 last_index=None, request_status=None):
        """

        :param version:
        :param process_id:
        :param first_index:
        :param last_index:
        :param request_status:
        :return:
        """
        super().__init__('DWTF', version)
        self.process_id = process_id
        self.first_index = first_index
        self.last_index = last_index
        self.request_status = request_status

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []

        self.append_serialized_body(self.process_id, FieldType.SHORT)
        self.append_serialized_body(self.first_index, FieldType.LONG)
        self.append_serialized_body(self.last_index, FieldType.LONG)
        self.append_serialized_body(self.request_status, FieldType.SHORT)
        return self._serialized_body


class RwtfBlock(ResultBlock):
    """
    This class represents a RWTF block
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

        rwtf = RwtfBlock(real_min=0, real_max=10, data=data,
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
        self.real_min = real_min
        self.real_max = real_max
        if data is not None:
            # copy the list
            self.data = list()
            for tab in data:
                self.data.append(list(tab))
        else:
            self.data = data
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision

    @property
    def vector_size(self):
        return len(self.data[0]) if self.data else 0

    @property
    def depth(self):
        return len(self.data) if self.data else 0

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []

        self.append_serialized_body(self.real_min, FieldType.FLOAT)
        self.append_serialized_body(self.real_max, FieldType.FLOAT)
        self.append_serialized_body(self.vector_size, FieldType.LONG)
        self.append_serialized_body(self.depth, FieldType.LONG)
        for vector in self.data:
            self.append_serialized_body(vector, FieldType.V_FLOAT)
        self.append_serialized_body(self.rel_precision,
                                    FieldType.FLOAT, min_version=1)
        self.append_serialized_body(self.abs_precision,
                                    FieldType.FLOAT, min_version=1)
        return self._serialized_body


class CwtfBlock(ResultBlock):
    """
    This class represents a CWTF block
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

        cwtf = CwtfBlock(real_min=0, real_max=10, im_min=0, im_max=0,
                         data=data, real_rel_precision=1, real_abs_precision=1,
                         im_rel_precision=1, im_abs_precision=1)

    """

    def __init__(self, version=1, real_min=None, real_max=None,
                 im_min=None, im_max=None, data=None,
                 real_rel_precision=None, real_abs_precision=None,
                 im_rel_precision=None, im_abs_precision=None):
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
        super().__init__('CWTF', version)
        self.real_min = real_min
        self.real_max = real_max
        self.im_min = im_min
        self.im_max = im_max
        if data is not None:
            # copy the list
            self.data = list()
            for tab in data:
                self.data.append(list(tab))
        else:
            self.data = data
        self.real_rel_precision = real_rel_precision
        self.real_abs_precision = real_abs_precision
        self.im_rel_precision = im_rel_precision
        self.im_abs_precision = im_abs_precision

    @property
    def vector_size(self):
        return len(self.data[0]) if self.data else 0

    @property
    def depth(self):
        return len(self.data) if self.data else 0

    def serialize_body(self):
        """ Put the field of the block in a list
        For each field we put a tuple containing:
        (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []

        self.append_serialized_body(self.real_min, FieldType.FLOAT)
        self.append_serialized_body(self.real_max, FieldType.FLOAT)
        self.append_serialized_body(self.im_min, FieldType.FLOAT)
        self.append_serialized_body(self.im_max, FieldType.FLOAT)
        self.append_serialized_body(self.vector_size, FieldType.LONG)
        self.append_serialized_body(self.depth, FieldType.LONG)
        for vector in self.data:
            self.append_serialized_body(vector, FieldType.V_TUPLE_FLOAT)
        self.append_serialized_body(self.real_rel_precision,
                                    FieldType.FLOAT, min_version=1)
        self.append_serialized_body(self.real_abs_precision,
                                    FieldType.FLOAT, min_version=1)
        self.append_serialized_body(self.im_rel_precision,
                                    FieldType.FLOAT, min_version=1)
        self.append_serialized_body(self.im_abs_precision,
                                    FieldType.FLOAT, min_version=1)
        return self._serialized_body

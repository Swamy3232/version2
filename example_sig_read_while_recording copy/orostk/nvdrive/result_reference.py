from orostk.nvdrive.result_utils import FieldType
from orostk.quantity import q_provider


class Reference(object):
    """
    This class represents a reference as described in a XREF block:
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

    def __init__(self, ref_name, quantity_key,
                 data, unit_name=None, unit_label=None,
                 rel_precision=None, abs_precision=None,
                 r_min=None, r_max=None):
        """

        :param ref_name:
        :type ref_name: str
        :param quantity_key:
        :type quantity_key: str
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
        :param r_min:
        :type r_min: float
        :param r_max:
        :type r_max: float
        :return:
        """
        self.ref_name = ref_name
        self.quantity_key = quantity_key
        if unit_name is None:
            self.unit_name = q_provider.get_si_unit_name(
                self.quantity_key
            )
        else:
            self.unit_name = unit_name
        if unit_label is None:
            self.unit_label = q_provider.get_unit_label(
                self.unit_name
            )
        else:
            self.unit_label = unit_label
        if data is not None:
            # copy the list
            self.data = list(data)
        else:
            self.data = data
        self.rel_precision = rel_precision
        self.abs_precision = abs_precision
        self.min = r_min
        self.max = r_max
        self._serialized_body = None

    def append_serialized(self, member, field_type):
        """

        :param member: member to serialize
        :param field_type:  type of the member
        :type field_type: FieldType
        :return:
        """
        if member is not None:
            self._serialized_body.append((member, field_type))
            return True
        else:
            return False

    def serialize(self, version):
        """ Put the field of the reference in a list
        For each field we put a tuple containing:
         (field, field_type)

        :return: A list of the fields as described above
        """
        self._serialized_body = []
        self.append_serialized(self.ref_name, FieldType.STRING)
        self.append_serialized(self.quantity_key, FieldType.STRING)
        self.append_serialized(self.unit_name, FieldType.STRING)
        self.append_serialized(self.unit_label, FieldType.STRING)
        self.append_serialized(self.data, FieldType.V_FLOAT)
        if version >= 1:
            self.append_serialized(self.rel_precision, FieldType.FLOAT)
            self.append_serialized(self.abs_precision, FieldType.FLOAT)
        if version >= 2:
            self.append_serialized(self.min, FieldType.FLOAT)
            self.append_serialized(self.max, FieldType.FLOAT)
        if version >= 3:
            self.append_serialized(self.quantity_key, FieldType.STRING)

        return self._serialized_body

    def is_SI(self):
        """

        :return: True if the unit is SI, else False
        """
        return q_provider.get_si_unit_name(self.quantity_key) == self.unit_name

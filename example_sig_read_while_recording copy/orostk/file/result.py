import datetime

from orostk.utils.orostk_utils import ValueFormat
from orostk.quantity import q_provider
from orostk.file.result_config import (
    ResultConfig, ScalarConfig, RegVectorConfig, RefVectorConfig,
    WaterfallConfig
)


class Result(object):
    """
    This class represents a NVGate result
    as represented in a result file.
    """

    def __init__(self, config: ResultConfig,
                 date=None, result_id=None):
        """

        :param config: A ResultConfig
        :param date: date of the first sample of the result
        :param result_id: Id given by NVGateFile dll, don't fill it by hand
        :param system_id: System Id given by NVGateFile dll, don't fill it by hand
        :param source_idn: Dictionnary of every source idn value, don't fill it by hand
        :param setting_value: Dictionnary of every setting value, don't fill it by hand
        """
        self.config = config
        self.date = date if date is not None else datetime.datetime(1601, 1, 1)
        self.result_id = result_id
        self.system_id = 0
        self.source_idn = {}
        self.setting_value = {}

    def is_SI(self):
        """

        :return: True if the result unit is SI else False
        """
        raise NotImplementedError


class ScalarResult(Result):
    """
    This class represents a NVGate scalar result
    as represented in a result file.

    Example::

        date = datetime.datetime(2017, 1, 1)
        res = ScalarResult(config=config, quantity_key='Angular_Velocity',
                           unit='RPM', data=0.5, date=date)

    """

    def __init__(self, config: ScalarConfig, quantity_key, unit,
                 data, date=None, result_id=None):
        """

        :param config: The ScalarConfig of this result
        :param date: date of the first sample of the result
        :type date: datetime
        :param quantity_key:
        :type quantity_key: str
        :param unit:
        :param data: float
        :param result_id: Id given by NVGateFile dll, don't fill it by hand
        """
        super().__init__(config, date=date, result_id=result_id)
        q_provider.is_consistent(quantity_key, unit_label=unit)
        self.quantity_key = quantity_key
        self.unit = unit
        self.data = data

    def is_SI(self):
        si_unit_name = q_provider.get_si_unit_name(self.quantity_key)
        si_unit_label = q_provider.get_unit_label(si_unit_name)
        return si_unit_label == self.unit


class RegVectorResult(Result):
    """
    This class represents a NVGate regular (real or complex)vector result
    as represented in a result file.

    Example::

        x_data = [25 * i for i in range(100)]
        y_data = [random.randint(0, 10) for i in range(100)]
        date = datetime.datetime(2017, 1, 1)
        RegVectorResult(config=config,
                        x_quantity_key='Potential_Difference', x_unit='V',
                        y_quantity_key='Frequency', y_unit='Hz',
                        x_data=x_data, y_data=y_data, date=date)

    """

    def __init__(self, config: RegVectorConfig,
                 x_quantity_key, x_unit, x_data,
                 y_quantity_key, y_unit, y_data,
                 date=None, result_id=None, y_format=ValueFormat.REAL, n_octave=None):
        """

        :param config: The RegVectorConfig for this result
        :param date: date of the first sample of the result
        :type date: datetime
        :param x_quantity_key: quantity key for X axis
        :type x_quantity_key: str
        :param x_unit: unit label
        :param y_quantity_key: quantity key for Y axis
        :type y_quantity_key: str
        :param y_unit: unit label
        :param x_data: list of float
        :param y_data: list of float or list of (float, float) for complex
        :param result_id: Id given by NVGateFile dll, don't fill it by hand
        :param y_format: The format of the values, ValueFormat enum
        :param n_octave: The n_octave only if result is an octave (0 for 1, 1 for 1/3, 2 for 1/12 ...)
        """
        super().__init__(config, date=date, result_id=result_id)
        q_provider.is_consistent(x_quantity_key, unit_label=x_unit)
        self.x_quantity_key = x_quantity_key
        self.x_unit = x_unit
        q_provider.is_consistent(y_quantity_key, unit_label=y_unit)
        self.y_quantity_key = y_quantity_key
        self.y_unit = y_unit
        self.y_unit = y_unit
        self.x_data = x_data
        self.y_data = y_data
        self.y_format = y_format
        self.n_octave = n_octave

    def is_SI(self):
        si_y_unit_name = q_provider.get_si_unit_name(self.y_quantity_key)
        si_y_unit_label = q_provider.get_unit_label(si_y_unit_name)
        si_x_unit_name = q_provider.get_si_unit_name(self.x_quantity_key)
        si_x_unit_label = q_provider.get_unit_label(si_x_unit_name)
        return (
            si_y_unit_label == self.y_unit and
            si_x_unit_label == self.x_unit
        )

    @property
    def size(self):
        return len(self.y_data)

    @property
    def is_complex(self):
        if self.y_format == ValueFormat.COMPLEX_REAL_IMAGINARY:
            return True
        elif self.y_format == ValueFormat.COMPLEX_MODULE_PHASE:
            return True
        else:
            return False


class RefVectorResult(Result):
    """
    This class represents a NVGate referenced (real or complex)vector result
    as represented in a result file.

    Example::

        date = datetime.datetime(2017, 1, 1)
        ref = Reference('Time', 'Time', 's', [i for i in range(10)])
        res = RefVectorResult(config=config, y_quantity_key='Angular_Velocity',
                              y_unit='rad/s', y_data=[i for i in range(10)],
                              date=date, references=[ref])
    """

    def __init__(self, config: RefVectorConfig, y_quantity_key,
                 y_unit, y_data, references,
                 date=None, result_id=None, y_format=ValueFormat.REAL):
        """

        :param config: The RefVectorConfig for this result
        :param date: date of the first sample of the result
        :type date: datetime
        :param y_quantity_key: quantity key for Y axis
        :type y_quantity_key: str
        :param references: list of references of the result
        :param y_data: list of float or list of (float, float) for complex
        :param result_id: Id given by NVGateFile dll, don't fill it by hand
        :param y_format: The format of the values, ValueFormat enum
        """
        super().__init__(config, date=date, result_id=result_id)
        q_provider.is_consistent(y_quantity_key, unit_label=y_unit)
        self.y_quantity_key = y_quantity_key
        self.y_data = y_data
        self.y_unit = y_unit
        self.references = references
        self.y_format = y_format

    def is_SI(self):
        si_unit_name = q_provider.get_si_unit_name(self.y_quantity_key)
        si_unit_label = q_provider.get_unit_label(si_unit_name)
        for ref in self.references:
            if not ref.is_SI():
                return False
        return si_unit_label == self.y_unit

    @property
    def size(self):
        return len(self.y_data)

    @property
    def is_complex(self):
        if self.y_format == ValueFormat.COMPLEX_REAL_IMAGINARY:
            return True
        elif self.y_format == ValueFormat.COMPLEX_MODULE_PHASE:
            return True
        else:
            return False


class WaterfallResult(Result):
    """
    This class represents a NVGate waterfall(real or complex) result
    as represented in a result file.

    Example::

        date = datetime.datetime(2017, 1, 1)
        size = 10
        depth = 16
        ref = Reference('Time', 'Time', 's', [i for i in range(depth)])
        x_data = [25 * i for i in range(size)]
        y_data = [[0.5*i for i in range(size)] for j in range(depth)]
        res = WaterfallResult(config=config, references=[ref],
                              x_quantity_key='Frequency', x_unit='Hz',
                              y_quantity_key='Potential_Difference',
                              y_unit='V',
                              x_data=x_data, y_data=y_data, date=date)

    """

    def __init__(self, config: WaterfallConfig,
                 x_quantity_key, x_unit, x_data,
                 y_quantity_key, y_unit, y_data,
                 references,
                 date=None, result_id=None, y_format=ValueFormat.REAL):
        """

        :param config: The WaterfallConfig for this result
        :param x_quantity_key: Quantity of the X axis
        :param x_unit: The label of the unit ('V' for 'Volt')
        :param x_data: data of the X axis, a list representing a regular vector
        :param y_quantity_key: Quantity of the Y axis
        :param y_unit: The label of the unit ('V' for 'Volt')
        :param y_data: a list of slices
        :param references:
        :param date: date of the first sample of the result
        :type date: datetime
        :param result_id: Id given by NVGateFile dll, don't fill it by hand
        :param y_format: The format of the values, ValueFormat enum
        """
        super().__init__(config, date=date, result_id=result_id)
        q_provider.is_consistent(x_quantity_key, unit_label=x_unit)
        self.x_quantity_key = x_quantity_key
        self.x_unit = x_unit
        q_provider.is_consistent(y_quantity_key, unit_label=y_unit)
        self.y_quantity_key = y_quantity_key
        self.y_unit = y_unit
        self.x_data = x_data
        self.y_data = y_data
        self.y_format = y_format
        self.references = references

    def is_SI(self):
        si_y_unit_name = q_provider.get_si_unit_name(self.y_quantity_key)
        si_y_unit_label = q_provider.get_unit_label(si_y_unit_name)
        si_x_unit_name = q_provider.get_si_unit_name(self.x_quantity_key)
        si_x_unit_label = q_provider.get_unit_label(si_x_unit_name)
        for ref in self.references:
            if not ref.is_SI():
                return False
        return (
            si_y_unit_label == self.y_unit and
            si_x_unit_label == self.x_unit
        )

    @property
    def depth(self):
        return len(self.y_data)

    @property
    def size(self):
        return len(self.x_data)

    @property
    def is_complex(self):
        if self.y_format == ValueFormat.COMPLEX_REAL_IMAGINARY:
            return True
        elif self.y_format == ValueFormat.COMPLEX_MODULE_PHASE:
            return True
        else:
            return False

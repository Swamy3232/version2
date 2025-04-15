from orostk.quantity import q_provider


class Reference(object):
    """
    This class represents a NVGate reference
    as represented in a result file

        Example ::

            ref = Reference(name='Time', quantity_key='Time',
                            unit='s', data=[i for i in range(20)])

    """

    def __init__(self, name, quantity_key, unit, data,
                 abs_precision=1e-6, rel_precision=1e-6):
        """

        :param name:
        :param quantity_key:
        :param unit: Unit label ('V' for Volts)
        :param data:
        :param abs_precision:
        :param rel_precision:
        :param is_tacho: True if this reference represents a tach reference, False by default
        """
        self.name = name
        q_provider.is_consistent(quantity_key, unit_label=unit)
        self.quantity_key = quantity_key
        self.unit = unit
        self.data = data
        self.abs_precision = abs_precision
        self.rel_precision = rel_precision
        self.is_tacho = False

    def is_SI(self):
        si_unit_name = q_provider.get_si_unit_name(self.quantity_key)
        si_unit_label = q_provider.get_unit_label(si_unit_name)
        return si_unit_label == self.unit

    def get_SI(self):
        """

        Returns a reference containing same data in SI unit

        """
        if self.is_SI():
            return self
        else:
            si_unit_name  = q_provider.get_si_unit_name(self.quantity_key)
            si_unit_label = q_provider.get_unit_label(si_unit_name)
            ref = Reference(self.name, self.quantity_key, si_unit_label, [], self.abs_precision, self.rel_precision)
            ref.is_tacho = self.is_tacho
            coefs = q_provider.get_unit_coef(self.unit)
            for i, val in enumerate(self.data):
                ref.data.append((val - coefs[1])/coefs[0])
            return ref
        
        
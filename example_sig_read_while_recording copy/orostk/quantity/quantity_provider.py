import configparser
import sys, os

from orostk.utils.singleton import Singleton
from orostk.utils.orostk_utils import OROSUNIT_PATH
from orostk.quantity.quantity_exceptions import QuantityError


class QuantityProvider(object):
    """
    This abstract class helps to retrieve NVGate quantities with their
    unit name, label ...
    """
    def __init__(self):
        pass

    def is_consistent(self, quantity, unit_name=None, unit_label=None):
        """ Check if:

                - The quantity exist
                - The unit_name match with the quantity
                - The unit label match with the unit name


        :param quantity:
        :param unit_name:
        :param unit_label:
        :return:
        """
        raise NotImplementedError

    def get_si_unit_name(self, quantity):
        """ Returns the SI (international system)\
         unit name of a quantity

        :param quantity:
        :return: A string of the unit
        """
        raise NotImplementedError

    def get_unit_label(self, unit_name):
        """Return the unit label of a unit

        :return: A string of the label
        """
        raise NotImplementedError

    def get_unit_coef(self, unit_name):
        """Returns the coef of a unit

        :param unit:
        :return: a tuple (coefA, coefB)
        """
        raise NotImplementedError

    def get_unit_dict(self, quantity):
        unit_dict = {}
        unit_dict['unit_name'] = self.get_si_unit_name(quantity)
        unit_dict['unit_label'] = self.get_unit_label(unit_dict['unit_name'])
        unit_dict['coefs'] = self.get_unit_coef(unit_dict['unit_name'])
        return unit_dict

    def get_quantity_units(self, quantity):
        """Returns all unit names of a quantity

        :param quantity:
        :return:
        """
        raise NotImplementedError


class LocalQuantityProvider(QuantityProvider, metaclass=Singleton):
    """
    This singleton class helps to retrieve NVGate quantities with their
    unit name, label ...

    It uses a local file orosunit.ini to get these informations
    """

    def __init__(self, oros_unit_path=OROSUNIT_PATH):
        super().__init__()
        if oros_unit_path == OROSUNIT_PATH:
            if getattr(sys, 'frozen', False):
                # we are running in a bundle
                oros_unit_path = sys._MEIPASS + "\\orostk\\quantity" + OROSUNIT_PATH
            else:
                # we are running in a normal Python environment
                oros_unit_path = os.path.dirname(os.path.abspath(__file__)) + OROSUNIT_PATH
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(oros_unit_path, encoding='utf-8-sig')
        if not self.config.sections():
            raise QuantityError("Can't load the"
                                " {} file".format(oros_unit_path))

    def change_oros_unit(self, oros_unit_path):
        self.config.read(oros_unit_path, encoding='utf-8')
        if not self.config.sections():
            raise QuantityError("Can't load the"
                                " {} file".format(oros_unit_path))

    def is_consistent(self, quantity, unit_name=None, unit_label=None):
        if quantity is None:
            return True
        if quantity not in self.config['BASE QUANTITY'].values():
            raise QuantityError(
                "Quantity '{}' doesn't exist".format(quantity))
        if unit_name is not None:
            if unit_name not in self.config[quantity].values():
                raise QuantityError(
                    "Unit '{}' is not a unit"
                    " of the quantity '{}'".format(unit_name, quantity))
        if unit_label is not None and unit_name is not None:
            if unit_label != self.config[unit_name]['LabelLin']:
                raise QuantityError("Unit label '{}' "
                                    "does not match with the unit '{}'"
                                    .format(unit_label, unit_name))

        if unit_label is not None and unit_name is None:
            for unit in self.get_quantity_units(quantity):
                if unit_label == self.config[unit]['LabelLin']:
                    break
            else:
                raise QuantityError("Unit label '{}' "
                                    "does not match with the quantity '{}'"
                                    .format(unit_label, quantity))

        return True

    def get_si_unit_name(self, quantity):
        return self.config[quantity]['Unit1']

    def get_unit_label(self, unit_name):
        return self.config[unit_name]['LabelLin']

    def get_unit_coef(self, unit_name):
        coef_a = float(self.config[unit_name]['CoeffA'])
        coef_b = float(self.config[unit_name]['CoeffB'])
        return (coef_a, coef_b)

    def get_quantity_units(self, quantity):
        units = []
        for key, value in self.config[quantity].items():
            if 'unit' in key[:4]:
                units.append(value)
        return units

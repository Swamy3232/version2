from ..client import Client, ENCODING
from ..commands.configuration import GetUnitInfo, GetUnitList, GetMagnitudeList
import configparser
import os


def GetAllUnits():  # TODO : improve it using a quantity class
    """
    Return a dict of magnitude containing a dict of unit containing dict of unit info
    """
    dict_magnitude = {}
    with Client() as client:
        cmd = GetMagnitudeList()
        client.send_command(cmd)
        list_magnitude = cmd.value

        for magnitude_name in list_magnitude:
            dict_magnitude[magnitude_name] = {}

            cmd = GetUnitList(magnitude_name=magnitude_name)
            client.send_command(cmd)

            list_unit = cmd.value

            for unit_name in list_unit:
                cmd = GetUnitInfo(magnitude_name=magnitude_name, unit_name=unit_name)
                client.send_command(cmd)
                unit_info = cmd

                dict_magnitude[magnitude_name][unit_name] = {}
                dict_magnitude[magnitude_name][unit_name]['unit_label'] = unit_info.userunit_name
                dict_magnitude[magnitude_name][unit_name]['unit_name'] = unit_info.userunit_label
                dict_magnitude[magnitude_name][unit_name]['si_unit_label'] = unit_info.si_unit
                dict_magnitude[magnitude_name][unit_name]['coeff_A'] = unit_info.coeffA
                dict_magnitude[magnitude_name][unit_name]['coeff_B'] = unit_info.coeffB

    return dict_magnitude


def GetOrosUnit():
    """
    Parse orosunit.ini, retrieving all magnitude_key
    """
    magnitude_key = {}

    orosunit_path = os.path.join(os.path.dirname(__file__), '..', 'quantity', 'orosunit.ini')
    config = configparser.ConfigParser(interpolation=None)
    config.read(orosunit_path, encoding=ENCODING)

    base_quantity = int(config['BASE QUANTITY']['Number'])
    for qty_nb in range(0, base_quantity):
        current_qty = config['BASE QUANTITY']['Quantity{}'.format(qty_nb+1)]
        magnitude_key[current_qty] = {}


    return magnitude_key


import pynvdrive
# from pynvdrive.commands.settingsstates.getsettingvalue import GetSettingValue
from .get_inputs_enabled import get_inputs_enabled, get_inputs_dc_enabled, GetSettingValue
from collections import OrderedDict
from pynvdrive.commands.settingsstates.getsettingvalues import GetSettingValues
from pynvdrive.quantity.utils.numbers import to_scientific_notation


def get_inputs_list(client: pynvdrive.Client = None, user_unit=True, significant_digits=None) -> list:
    """
    Return a list of inputs as defined in nvgate panel.
    """
    if client is None:
        client = pynvdrive.Client()
        client.connect()
    else:
        client.connect()

    if not client.is_connected():
        return []

    from ..quantity.quantity_provider import QuantityProvider
    quantity_provider = QuantityProvider(client_pynvdrive=client)

    idn_front_end = 'frontEnd'

    # Count the number of inputs
    list_inputs_enabled = get_inputs_enabled()

    if not list_inputs_enabled:
        return []

    # Common used name: idn name
    sampling_dict = OrderedDict({'high': 'inputSampling', 'low': '868', 'dc': 'dcSampling'})
    input_dict = OrderedDict({'label': 'label', 'transducer': 'transducer', 'physical Qty': 'physicalQty', 'sensitivity': 'sensitivity',
                  'range Pk': 'rangePk', 'coupling': 'coupling', 'sampling': '869', 'input type': 'inputType', 'component': 'component',
                  'node': 'node', 'direction': 'direction', 'type': 'nodeType', 'external gain': 'extGain', 'polarity': 'polarity',
                  'offset': 'offset', 'input filter': 'inputFilter', 'auto-range': 'enableAutorange'})

    inputs_list = []
    # Get frontend settings
    sampling = {}
    for key in sampling_dict:
        cmd = GetSettingValue(idn='{}.inputSettings.{}'.format(idn_front_end, sampling_dict[key]))
        client.send_command(cmd)
        sampling[key] = cmd.value

    for input_number in list_inputs_enabled:
        current_input = OrderedDict()
        for key in input_dict:
            try:
                idn = '{}.input{}.{}'.format(idn_front_end, input_number, input_dict[key])
                cmd = GetSettingValue(idn=idn)
                client.send_command(cmd)
                current_input[key] = cmd.value
            except pynvdrive.NVDriveCommandError as e:
                print('error get_inputs_list GetSettingValue input e:{}, idn:{}'.format(e, idn))

        # Convert some number values to understandable string
        list_to_clarify = ['input type', 'coupling', 'polarity', 'physical Qty']
        for key_to_clarify in list_to_clarify:
            value_to_find = input_dict.get(key_to_clarify, None)
            try:
                idn = '{}.input{}.{}'.format(idn_front_end, input_number, value_to_find)
                cmd = GetSettingValues(idn=idn)
                client.send_command(cmd)
                input_type_list = cmd.value
            except Exception:
                input_type_list = []
            for couple in input_type_list:
                if couple[0] == current_input.get(key_to_clarify, None):
                    current_input[key_to_clarify] = couple[1]
                    break

        magnitude_name = current_input.get('physical Qty', None)
        unit = quantity_provider.get_unit_user(magnitude_name=magnitude_name)

        list_to_convert_unit = ['range Pk']
        # Convert value to user unit
        if user_unit:
            # Note : sensitivity is always retrieve in V/UserUnit
            for key_to_convert in list_to_convert_unit:
                value_to_convert = current_input.get(key_to_convert, None)
                if value_to_convert is not None:
                    current_input[key_to_convert] = unit.get_user_value_from_si_value(value_to_convert)

        # Significant digits
        if significant_digits is not None and significant_digits > 0:
            current_input['sensitivity'] = to_scientific_notation(x=current_input['sensitivity'],
                                                                  significant_digits=significant_digits)
            for key_to_convert in list_to_convert_unit:
                value_to_convert = current_input.get(key_to_convert, None)
                if value_to_convert is not None:
                    current_input[key_to_convert] = to_scientific_notation(x=value_to_convert,
                                                                           significant_digits=significant_digits)

        # Add unit to displayed value
        if user_unit:
            unit_label = unit.unit_label
        else:
            unit_label = unit.si_unit_label

        current_input['sensitivity'] = '{} ({})/({})'.format(current_input['sensitivity'], 'V', unit_label)
        current_input['offset'] = '{} {}'.format(current_input['offset'], 'V')
        current_input['range Pk'] = '{} {}'.format(current_input['range Pk'], unit_label)

        inputs_list.append(current_input)

    return inputs_list


def get_inputs_dc_list(client: pynvdrive.Client = None, user_unit=True, significant_digits=None) -> list:
    """
    Return a list of inputs as defined in nvgate panel.
    """
    if client is None:
        client = pynvdrive.Client()
        client.connect()
    else:
        client.connect()

    if not client.is_connected():
        return []

    from ..quantity.quantity_provider import QuantityProvider
    quantity_provider = QuantityProvider(client_pynvdrive=client)

    idn_front_end = 'frontEnd'

    # Count the number of inputs
    list_inputs_dc_enabled = get_inputs_dc_enabled()

    if not list_inputs_dc_enabled:
        return []

    # Common used name: idn name
    input_dict = OrderedDict({'label': 'label', 'input type': 'dcInputType', 'transducer': 'transducer', 'physical Qty': 'physicalQty', 'sensitivity': 'sensitivity',
                  'range Pk': 'rangePk', 'offset': 'offset', 'external gain': 'extGain', 'polarity': 'polarity',
                  'auto-range': 'enableAutorange', 'tach': '182', 'probe': 'probe', 'range': '479', 'current': 'thermoCurrent'})

    input_dict_probe = OrderedDict({'probe': 'probe', 'range': '479', 'current': 'thermoCurrent'})

    inputs_list = []

    for input_number in list_inputs_dc_enabled:
        current_input = OrderedDict()
        for key in input_dict:
            try:
                cmd = GetSettingValue(idn='{}.dcinput{}.{}'.format(idn_front_end, input_number, input_dict[key]))
                client.send_command(cmd)
                current_input[key] = cmd.value
            except pynvdrive.NVDriveCommandError as e:
                print('error GetSettingValue dc input', e)

        # Convert some number values to understandable string
        list_to_clarify = ['input type', 'polarity', 'physical Qty', 'probe', 'current']
        for key_to_clarify in list_to_clarify:
            value_to_find = input_dict.get(key_to_clarify, None)
            try:
                cmd = GetSettingValues(idn='{}.dcinput{}.{}'.format(idn_front_end, input_number, value_to_find))
                client.send_command(cmd)
                input_type_list = cmd.value
            except Exception:
                input_type_list = []
            for couple in input_type_list:
                if couple[0] == current_input.get(key_to_clarify, None):
                    current_input[key_to_clarify] = couple[1]
                    break

        magnitude_name = current_input.get('physical Qty', None)
        unit = quantity_provider.get_unit_user(magnitude_name=magnitude_name)

        list_to_convert_unit = ['range Pk']
        # Convert value to user unit
        if user_unit:
            # Note : sensitivity is always retrieve in V/UserUnit
            for key_to_convert in list_to_convert_unit:
                value_to_convert = current_input.get(key_to_convert, None)
                if value_to_convert is not None:
                    current_input[key_to_convert] = unit.get_user_value_from_si_value(value_to_convert)

        # Significant digits
        if significant_digits is not None and significant_digits > 0:
            current_input['sensitivity'] = to_scientific_notation(x=current_input['sensitivity'],
                                                                  significant_digits=significant_digits)
            current_input['offset'] = to_scientific_notation(x=current_input['offset'],
                                                             significant_digits=significant_digits)
            for key_to_convert in list_to_convert_unit:
                value_to_convert = current_input.get(key_to_convert, None)
                if value_to_convert is not None:
                    current_input[key_to_convert] = to_scientific_notation(x=value_to_convert,
                                                                           significant_digits=significant_digits)

        # Add unit to displayed value
        if user_unit:
            unit_label = unit.unit_label
        else:
            unit_label = unit.si_unit_label

        current_input['sensitivity'] = '{} ({})/({})'.format(current_input['sensitivity'], 'V', unit_label)
        current_input['offset'] = '{} {}'.format(current_input['offset'], 'V')
        current_input['range Pk'] = '{} {}'.format(current_input['range Pk'], unit_label)


        # Clean some fields if its a probe
        if unit_label in current_input['range']:
            # Its a probe, remove offset if exist
            current_input.pop('sensitivity', None)
            current_input.pop('range Pk', None)
            current_input.pop('external gain', None)
            current_input.pop('offset', None)
            current_input.pop('auto-range', None)
            current_input.pop('tach', None)
        else:
            # Standard DC input
            current_input.pop('probe', None)
            current_input.pop('range', None)
            current_input.pop('current', None)

        inputs_list.append(current_input)
    return inputs_list



import pynvdrive
from .get_tachs_enabled import get_tachs_enabled, GetSettingValue
from collections import OrderedDict
from pynvdrive.commands.settingsstates.getsettingvalues import GetSettingValues
from pynvdrive.quantity.utils.numbers import to_scientific_notation


def get_tachs_info_list(client: pynvdrive.Client = None, user_unit=True, significant_digits=None) -> list:
	"""
    Return a list of tach as defined in nvgate panel
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
	list_tachs_enabled = get_tachs_enabled()

	# Common used name: idn name
	tach_dict = OrderedDict({'label': 'label', 'threshold': 'threshold', 'range Pk': 'rangePk', 'coupling': 'coupling',
	                         'pulse rev': '241', 'max speed': '270', 'min speed': '276', 'slope': 'slope',
	                         'hold off': 'holdoff',
	                         'hysteresis': 'hysteresis', 'pre-divider': 'predivider',
	                         'post-multiplier': 'postMultiplier',
	                         'multiplier hold off': 'multiplierHoldoff', 'physical Qty': 'physicalQty',
	                         'sensitivity': 'sensitivity',
	                         'external gain': 'extGain', 'offset': 'offset',
	                         'mode': 'extSyncMode', 'hold off %': '290', 'rotation': '410', 'average size': '242',
	                         'missing teeth': '421'})

	tach_list = []
	# Get tach settings
	for tach_number in list_tachs_enabled:
		current_tach = OrderedDict({'channel_number': tach_number})
		for key in tach_dict:
			try:
				cmd = GetSettingValue(idn='{}.extSync{}.{}'.format(idn_front_end, tach_number, tach_dict[key]))
				client.send_command(cmd)
				current_tach[key] = cmd.value
			except pynvdrive.NVDriveCommandError as e:
				print('error GetSettingValue tach', e)

		# Convert some number values to understandable string
		list_to_clarify = ['mode', 'coupling', 'slope', 'physical Qty', 'rotation']
		for key_to_clarify in list_to_clarify:
			value_to_find = tach_dict.get(key_to_clarify, None)
			try:
				cmd = GetSettingValues(idn='{}.extSync{}.{}'.format(idn_front_end, tach_number, value_to_find))
				client.send_command(cmd)
				input_type_list = cmd.value
			except Exception:
				input_type_list = []
			for couple in input_type_list:
				if couple[0] == current_tach.get(key_to_clarify, None):
					current_tach[key_to_clarify] = couple[1]
					break

		magnitude_name = current_tach.get('physical Qty', None)
		unit = quantity_provider.get_unit_user(magnitude_name=magnitude_name)
		unit_tach = quantity_provider.get_unit_user(magnitude_name='Angular velocity')

		list_to_convert_unit = ['range Pk', 'hysteresis', 'threshold']
		list_to_convert_unit_tach = ['max speed', 'min speed']
		# Convert value to user unit
		if user_unit:
			# Note : sensitivity is always retrieve in V/UserUnit
			for key_to_convert in list_to_convert_unit:
				value_to_convert = current_tach.get(key_to_convert, None)
				if value_to_convert is not None:
					current_tach[key_to_convert] = unit.get_user_value_from_si_value(value_to_convert)
			for key_to_convert in list_to_convert_unit_tach:
				value_to_convert = current_tach.get(key_to_convert, None)
				if value_to_convert is not None:
					current_tach[key_to_convert] = unit_tach.get_user_value_from_si_value(value_to_convert)

		# Significant digits
		if significant_digits is not None and significant_digits > 0:
			current_tach['sensitivity'] = to_scientific_notation(x=current_tach['sensitivity'],
			                                                     significant_digits=significant_digits)
			for key_to_convert in list_to_convert_unit + list_to_convert_unit_tach:
				value_to_convert = current_tach.get(key_to_convert, None)
				if value_to_convert is not None:
					current_tach[key_to_convert] = to_scientific_notation(x=value_to_convert,
					                                                      significant_digits=significant_digits)
		# Add unit to displayed value
		if user_unit:
			unit_label = unit.unit_label
			unit_label_tach = unit_tach.unit_label
		else:
			unit_label = unit.si_unit_label
			unit_label_tach = unit_tach.si_unit_label

		current_tach['sensitivity'] = '{} ({})/({})'.format(current_tach['sensitivity'], 'V', unit_label)
		current_tach['range Pk'] = '{} {}'.format(current_tach['range Pk'], unit_label)
		current_tach['max speed'] = '{} {}'.format(current_tach['max speed'], unit_label_tach)
		current_tach['min speed'] = '{} {}'.format(current_tach['min speed'], unit_label_tach)
		current_tach['hysteresis'] = '{} {}'.format(current_tach['hysteresis'], unit_label)
		current_tach['threshold'] = '{} {}'.format(current_tach['threshold'], unit_label)
		current_tach['offset'] = '{} {}'.format(current_tach['offset'], 'V')

		tach_list.append(current_tach)
	return tach_list

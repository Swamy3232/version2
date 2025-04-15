import pynvdrive
from ...toolbox.get_inputs_list import get_inputs_list
from ...toolbox.get_tachs_list import get_tachs_info_list
from pynvdrive.commands.settingsstates.getsettingvalue import GetSettingValue


def get_magnitude_key_all_inputs(client: pynvdrive.Client = None) -> dict:
	"""
	Retrieve magnitude_key for all inputs
	:return: dict of input_name:magnitude_key
	# TODO : Could be an issue if multiple frontend input have same input_name
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	# Retrieve the unit of each result
	list_inputs = get_inputs_list(client=client)
	list_tachs = get_tachs_info_list(client=client)

	input_magnitude_dict = {}
	for input_ in list_inputs:
		input_magnitude_dict[input_['label']] = input_['physicalQty']
	for input_ in list_tachs:
		input_magnitude_dict[input_['label']] = input_['physicalQty']
	return input_magnitude_dict


def get_magnitude_key_from_input_name(input_name:str, client: pynvdrive.Client = None) -> str:
	"""
	Retrieve magnitude_key from frontend settings
	:return: magnitude_key
	# TODO : Could be an issue if multiple frontend input have same input_name
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	# Retrieve the unit of each result
	input_magnitude_dict = get_magnitude_key_all_inputs(client=client)
	return input_magnitude_dict.get(input_name, None)


def get_magnitude_key_from_input_number(input_nb, client: pynvdrive.Client = None) -> str:
	"""
	Retrieve magnitude_key from frontend settings
	:return: magnitude_key
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	idn_front_end = 'frontEnd'
	input_nb = int(input_nb)
	magnitude_key = None
	try:
		idn = '{}.input{}.{}'.format(idn_front_end, input_nb, 'physicalQty')
		cmd = GetSettingValue(idn=idn)
		client.send_command(cmd)
		magnitude_key = cmd.value
	except pynvdrive.NVDriveCommandError as e:
		print('error get_magnitude_key_from_input_number GetSettingValue input', e)
	# Retrieve the unit of each result
	return magnitude_key

def get_magnitude_key_from_input_idn(input_idn, client: pynvdrive.Client = None) -> str:
	"""
	Retrieve magnitude_key from input_idn settings
	:return: magnitude_key
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	module = input_idn.split('.')[0]
	input_nb = input_idn.split('.')[1]
	idn_magnitude_key = '{}.{}.{}'.format(module, input_nb, '204')
	magnitude_key = None
	try:
		# print('idn_magnitude_key', idn_magnitude_key)
		cmd = GetSettingValue(idn=idn_magnitude_key)
		client.send_command(cmd)
		magnitude_key = cmd.value
	except pynvdrive.NVDriveCommandError as e:
		print('error GetSettingValue input', e)
	# Retrieve the unit of each result
	return magnitude_key
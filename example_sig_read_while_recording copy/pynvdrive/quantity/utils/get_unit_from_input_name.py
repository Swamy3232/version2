import pynvdrive
from ...quantity.unit import Unit
from ...quantity.quantity_provider import QuantityProvider
from .get_magnitude_key_from_input import get_magnitude_key_all_inputs


def get_unit_from_input_name(input_name: str, client: pynvdrive.Client = None, quantity_provider: QuantityProvider = QuantityProvider()) -> Unit():
	"""
	Retrieve unit for input_name
	:return: unit
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	# TODO : Could be an issue if multiple frontend input have same input_name
	input_magnitude_dict = get_magnitude_key_all_inputs(client=client)
	magnitude_key = input_magnitude_dict.get(input_name, None)

	return quantity_provider.get_unit_user(magnitude_key=magnitude_key)


def get_unit_from_input_names(input_names_list: list, client: pynvdrive.Client = None, quantity_provider: QuantityProvider = QuantityProvider()) -> dict:
	"""
	Retrieve unit for multiples inputs names
	:return: dict of input_name:unit
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	input_magnitude_dict = get_magnitude_key_all_inputs(client=client)

	results = {}
	for input_name in input_names_list:
		# Retrieve magnitude_key from frontend settings
		magnitude_key = input_magnitude_dict.get(input_name, None)
		results[input_name] = quantity_provider.get_unit_user(magnitude_key=magnitude_key)
	return results

import pynvdrive
from ..commands.signalresult import GetResultList, ResultFormatAndDescription
from ..quantity.quantity_provider import QuantityProvider
from ..formats.process import processes_scalar, processes_hidden
from .get_layouts_list import get_layouts_list
from ..commands.graphics.setlayout import SetLayout
from .get_tachs_list import get_tachs_info_list


def get_available_results(result_type: str = None, displayed_only: bool = True, client: pynvdrive.Client = None,
                          include_tach=False) -> list[ResultFormatAndDescription]:
	"""
	Returns a list of available results.

	:param result_type: '1D', '2D' or None (all)
	:param displayed_only: If True, only layout displayed results are returned.
	:param include_tach: If True, tachs results are included.
	:return: List of ResultFormatAndDescription of available results
	"""
	# TODO : Improve speed of this function ... take too much time to retrieve the list
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	if not client.is_connected():
		return []

	list_results = []
	if displayed_only:
		list_layouts = get_layouts_list(client=client)
		for layout_name in list_layouts:
			try:
				cmd = SetLayout(layout_name=layout_name)
				client.send_command(cmd)
			except pynvdrive.NVDriveCommandError as e:
				print('error SetLayout ', e.error)
			try:
				cmd = GetResultList()
				client.send_command(cmd)
				list_results += cmd.list_result_format_and_description
			except pynvdrive.NVDriveCommandError as e:
				print('error GetResultList ', e.error)
	else:
		pass

	# Delete double results
	new_list_results = []
	for result in list_results:
		if not include_tach and result.is_tach:
			if result.is_tach:  # If it's a tach but we don't want them then skip it
				continue

		if result.to_dict() not in [r.to_dict() for r in new_list_results]:
			new_list_results.append(result)

	list_results = new_list_results
	if result_type == '1D':
		list_results = [r for r in list_results if (r.process_id in processes_scalar and r.module_id != 16)]
	elif result_type == '2D':
		list_results = [r for r in list_results if (r.process_id not in processes_scalar and r.module_id != 16)]
	else:
		pass

	# Retrieve the unit of each result
	quantity_provider = QuantityProvider()
	for result in list_results:
		result.update_unit(client=client, quantity_provider=quantity_provider)
	# Remove from the list results that are not available
	list_results = [r for r in list_results if r.process_id not in processes_hidden]

	return list_results


def get_available_tachs_results(client=None) -> list[ResultFormatAndDescription]:
	"""
	Returns a list of tachs results
	:return: List of ResultFormatAndDescription of available results
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	if not client.is_connected():
		return []

	list_tachs_results = []

	for tach in get_tachs_info_list(client=client):
		tach_label = '{}{}'.format('[Tach] ', tach.get('label', None))
		tach_mode = tach.get('mode', None)
		if tach_mode is None or str(tach_mode) == '2': # Exclude torsional tach
			continue
		# module_id 6 = tach, process_id 75 = ext sync tach rpm
		result = ResultFormatAndDescription(module_id=6, process_id=75, channel_number=tach.get('channel_number', None),
		                                    input_name=tach_label, reference_channel_number=None,
		                                    input_name_reference_channel_number=None)
		result.update_unit(client=client)
		list_tachs_results.append(result)

	return list_tachs_results

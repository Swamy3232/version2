import pynvdrive
from ..commands.signalresult import GetResultList, ResultFormatAndDescription
from ..quantity.quantity_provider import QuantityProvider
from ..formats.process import processes_scalar, processes_hidden
from .get_layouts_list import get_layouts_list
from ..commands.graphics.setlayout import SetLayout
from .get_tachs_list import get_tachs_info_list
from pynvdrive.formats.marker_description import MarkerDescription
from pynvdrive.toolbox.get_marker_list import get_marker_list
from pynvdrive.toolbox.get_windows_list import get_windows_list
from pynvdrive.toolbox.get_layouts_list import get_layouts_list
from pynvdrive.toolbox.set_layout import set_layout
from pynvdrive.toolbox.get_free_marker_parameters import get_free_marker_parameters
from pynvdrive.toolbox.get_window_traces import get_window_traces
from pynvdrive.toolbox.get_active_trace import get_active_trace


def get_available_markers_as_results_format_and_description(client: pynvdrive.Client = None) -> list[ResultFormatAndDescription]:
	"""
	Returns a list of available markers as ResultFormatAndDescription.
	:return: List of ResultFormatAndDescription of available markers
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	if not client.is_connected():
		return []

	list_available_markers = get_available_markers(split=True, client=client)

	list_results_format_and_description = []
	for marker in list_available_markers:
		results_format_and_description = marker.result_format_and_description
		results_format_and_description.set_marker(marker_name=marker.marker_name, marker_position=marker.marker_position)
		list_results_format_and_description.append(results_format_and_description)

	# Delete double results
	new_list_results = list_results_format_and_description
	for result in list_results_format_and_description:
		if result.to_dict() not in [r.to_dict() for r in new_list_results]:
			new_list_results.append(result)

	# Retrieve the unit of each result
	quantity_provider = QuantityProvider()
	for result in new_list_results:
		result.update_unit(client=client, quantity_provider=quantity_provider)

	return new_list_results


def get_available_markers(split=False, client: pynvdrive.Client = None) -> list[MarkerDescription]:
	"""
	Returns a list of available markers.
	:param split: If True, returns "All traces" markers as different markers for each trace
	:param client: Client to use
	:return: List of MarkerDescription of available markers
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	if not client.is_connected():
		return []

	list_markers = []
	layout_list = get_layouts_list()
	for layout_name in layout_list:
		set_layout(layout_name=layout_name, client=client)
		windows_list = get_windows_list(layout_name=layout_name, client=client)
		for window_name in windows_list:
			marker_list = get_marker_list(window_name=window_name, client=client)
			for marker in marker_list:
				value = get_free_marker_parameters(window_name=window_name, display_zone_type=marker.display_zone_type,
				                                   marker_number=marker.marker_number, client=client)
				if not value:
					continue
				marker.marker_position = value[0]
				marker.marker_name = value[1]
				marker.interpolation_type = value[2]

				if marker.location == 0:  # Apply to all traces
					# Need to create one marker for each trace
					if split:
						result_format_and_description_list = get_window_traces(window_name=window_name, client=client)
						for result_format_and_description in result_format_and_description_list:
							marker_copy = marker.copy()
							marker_copy.set_result_format_and_description(result_format_and_description)
							marker_copy.set_location(2) # Apply to one trace with result_format_and_description
							list_markers.append(marker_copy)
					else:
						list_markers.append(marker)

				elif marker.location == 1:  # Apply to active traces
					active_trace_idx = get_active_trace(layout_name=layout_name, window_name=window_name, client=client)
					if active_trace_idx is not None and active_trace_idx >= 0:
						result_format_and_description_list = get_window_traces(window_name=window_name, client=client)
						if active_trace_idx >= 0 and active_trace_idx < len(result_format_and_description_list):
							marker.set_result_format_and_description(result_format_and_description_list[active_trace_idx])
							list_markers.append(marker)
				elif marker.location == 2:  # Apply to resultsformatanddescription attached to the marker
					# Already one marker with one result format and description
					list_markers.append(marker)
				else:
					continue

	# for marker in list_markers:
	# 	print('Marker retained', marker.to_dict())

	return list_markers
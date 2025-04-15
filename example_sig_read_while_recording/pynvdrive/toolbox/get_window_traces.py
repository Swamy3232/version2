import pynvdrive
from pynvdrive import NVDriveCommandError
from ..client import Client
from ..commands.marker import GetWindowTraces
from pynvdrive.formats.result_format_and_description import ResultFormatAndDescription


def get_window_traces(window_name, client: pynvdrive.Client = None):
	"""
	Return resultformatanddescription list
	:return: list<resultformatanddescription>
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = GetWindowTraces(window_name=window_name)
		client.send_command(cmd)
		results_list = cmd.list_result_format_and_description
	except NVDriveCommandError as e:
		print('error GetWindowTraces ', e)
		return []

	return results_list

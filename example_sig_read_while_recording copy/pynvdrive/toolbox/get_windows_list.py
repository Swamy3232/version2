import pynvdrive
from pynvdrive import NVDriveCommandError
from ..client import Client
from ..commands.graphics import GetWindowNameList


def get_windows_list(layout_name, client: pynvdrive.Client = None):
	"""
	Return layout list
	:return: list<str>
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	windows_list = []

	try:
		cmd = GetWindowNameList(layout=layout_name)
		client.send_command(cmd)
		windows_list = cmd.value
	except NVDriveCommandError as e:
		print('error GetWindowNameList ', e)

	return windows_list

import pynvdrive
from ..commands.actions.waitgui import WaitGUI


def wait_gui(client: pynvdrive.Client = None):
	"""
	Load a model in NVGate
	:param silent: True to set silent mode, False to set normal mode
	:param client: pynvdrive.Client instance
	:return:
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = WaitGUI()
		client.send_command(cmd)
	except pynvdrive.NVDriveCommandError as e:
		print('error WaitGUI input', e)
		return None
	except pynvdrive.NVDriveConnectionError:
		print('error WaitGUI connection')
		return None

	return True

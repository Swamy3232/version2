import pynvdrive
from pynvdrive import NVDriveCommandError, NVDriveConnectionError
from ..client import Client
from ..commands.graphics import GetLayoutList


def get_layouts_list(client: pynvdrive.Client = None):
	"""
	Return layout list
	:return: list<str>
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	layouts_list = []

	try:
		cmd = GetLayoutList()
		client.send_command(cmd)
		layouts_list = cmd.value
	except NVDriveCommandError as e:
		print('error GetLayoutList ', e)
	except NVDriveConnectionError:
		print('error NVDrive is not connected (get_layouts_list)')
	except Exception:
		pass

	return layouts_list

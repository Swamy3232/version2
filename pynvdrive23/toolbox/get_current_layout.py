import pynvdrive
from pynvdrive import NVDriveCommandError, NVDriveConnectionError
from ..commands.graphics.getcurrentlayout import GetCurrentLayout


def get_current_layout(client: pynvdrive.Client = None):
	"""
	Return layout list
	:return: list<str>
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = GetCurrentLayout()
		client.send_command(cmd)
		return cmd.value
	except NVDriveCommandError as e:
		print('error GetCurrentLayout ', e)
	except NVDriveConnectionError:
		print('error NVDrive is not connected (GetCurrentLayout)')
	except Exception:
		pass

	return ''

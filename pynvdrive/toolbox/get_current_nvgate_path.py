import pynvdrive
from pynvdrive import NVDriveCommandError, NVDriveConnectionError
from ..commands.configuration.getcurrentnvgatepath import GetCurrentNVGatePath


def get_current_nvgate_path(client: pynvdrive.Client = None):
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
		cmd = GetCurrentNVGatePath()
		client.send_command(cmd)
		return cmd.value
	except NVDriveCommandError as e:
		print('error GetCurrentNVGatePath ', e)
	except NVDriveConnectionError:
		print('error NVDrive is not connected (GetCurrentNVGatePath)')
	except Exception:
		pass

	return ''

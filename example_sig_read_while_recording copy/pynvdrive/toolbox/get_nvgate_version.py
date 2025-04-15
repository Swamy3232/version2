import pynvdrive
from pynvdrive import NVDriveCommandError, NVDriveConnectionError
from ..commands.analyzers import GetNVGateInfo


def get_nvgate_version(client: pynvdrive.Client = None):
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
		cmd = GetNVGateInfo()
		client.send_command(cmd)
		return cmd.nvgate_major_version, cmd.nvgate_minor_version, cmd.indice
	except NVDriveCommandError as e:
		print('error GetNVGateInfo ', e.error)
	except NVDriveConnectionError:
		print('error NVDrive is not connected (get_nvgate_version)')
	except Exception as e:
		print('error get_nvgate_version', e.error)

	return 0, 0, 0

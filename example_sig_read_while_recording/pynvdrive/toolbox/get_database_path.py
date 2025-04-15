import pynvdrive
from pynvdrive import NVDriveCommandError, NVDriveConnectionError
from ..commands.project.getdatabasepath import GetDatabasePath


def get_database_path(client: pynvdrive.Client = None):
	"""
	Return database path (NVGate data)
	:return: list<str>
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = GetDatabasePath()
		client.send_command(cmd)
		return cmd.value
	except NVDriveCommandError as e:
		print('error GetDatabasePath ', e)
	except NVDriveConnectionError:
		print('error NVDrive is not connected (GetDatabasePath)')
	except Exception:
		pass

	return ''

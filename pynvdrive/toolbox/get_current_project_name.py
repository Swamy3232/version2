import pynvdrive
from pynvdrive import NVDriveCommandError, NVDriveConnectionError
from ..commands.project.getcurrentprojectname import GetCurrentProjectName


def get_current_project_name(client: pynvdrive.Client = None):
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
		cmd = GetCurrentProjectName()
		client.send_command(cmd)
		return cmd.value
	except NVDriveCommandError as e:
		print('error GetCurrentProjectName ', e)
	except NVDriveConnectionError:
		print('error NVDrive is not connected (GetCurrentProjectName)')
	except Exception:
		pass

	return ''

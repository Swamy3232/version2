import pynvdrive
from ..commands.project.refreshpm import RefreshPM


def refresh_pm(client: pynvdrive.Client = None):
	"""
	Run
	:return:
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = RefreshPM()
		client.send_command(cmd)
		return True
	except pynvdrive.NVDriveCommandError as e:
		print('error RefreshPM ', e)
		return False
	except pynvdrive.NVDriveConnectionError as e:
		print('error RefreshPM ', e)
		return False
	except Exception:
		return False

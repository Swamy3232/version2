import pynvdrive
from ..commands.actions.run import Run


def run(client: pynvdrive.Client = None):
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
		cmd = Run()
		client.send_command(cmd)
		return True
	except pynvdrive.NVDriveCommandError as e:
		print('error Run ', e)
		return False
	except pynvdrive.NVDriveConnectionError as e:
		print('error Run ', e)
		return False
	except Exception:
		return False

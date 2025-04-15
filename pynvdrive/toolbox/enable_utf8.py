import pynvdrive
from ..commands.configuration.enableutf8 import EnableUTF8


def enable_utf8(client: pynvdrive.Client = None):
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
		cmd = EnableUTF8()
		client.send_command(cmd)
		return True
	except pynvdrive.NVDriveCommandError as e:
		print('error EnableUTF8 ', e)
		return False
	except pynvdrive.NVDriveConnectionError as e:
		print('error EnableUTF8 ', e)
		return False
	except Exception:
		return False

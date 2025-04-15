import pynvdrive
from ..commands.graphics.getactivetrace import GetActiveTrace


def get_active_trace(layout_name, window_name, client: pynvdrive.Client = None):
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
		cmd = GetActiveTrace(layout_name=layout_name, window_name=window_name)
		client.send_command(cmd)
		return cmd.value
	except pynvdrive.NVDriveCommandError as e:
		print('error GetActiveTrace ', e)
		return False
	except pynvdrive.NVDriveConnectionError as e:
		print('error GetActiveTrace ', e)
		return False
	except Exception:
		return False

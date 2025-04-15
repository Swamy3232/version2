import pynvdrive
from ..commands.actions.stop import Stop


def stop(client: pynvdrive.Client = None):
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
		cmd = Stop()
		client.send_command(cmd)
		return True
	except pynvdrive.NVDriveCommandError as e:
		print('error Stop ', e)
		return False

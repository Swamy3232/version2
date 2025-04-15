import pynvdrive
from ..commands.actions.manualtrigger import ManualTrigger


def manual_trigger(client: pynvdrive.Client = None):
	"""
	ManualTrigger
	:return:
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = ManualTrigger()
		client.send_command(cmd)
		return True
	except pynvdrive.NVDriveCommandError as e:
		print('error ManualTrigger ', e)
		return False

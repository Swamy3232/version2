import pynvdrive
from ..commands.configuration.setsilent import SetSilent


def set_silent(silent=True, client: pynvdrive.Client = None):
	"""
	Load a model in NVGate
	:param silent: True to set silent mode, False to set normal mode
	:param client: pynvdrive.Client instance
	:return:
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	if silent:
		value = 1
	else:
		value = 0

	try:
		cmd = SetSilent(nSilent=value)
		client.send_command(cmd)
	except pynvdrive.NVDriveCommandError as e:
		print('error SetSilent input', e)
		return None
	except pynvdrive.NVDriveConnectionError:
		print('error SetSilent connection')
		return None

	return True

import pynvdrive
from ..commands.signalresult import DeleteAllResultEx


def delete_all_result_ex(client: pynvdrive.Client = None):
	"""
	delete_all_result_ex
	:return: bool success
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = DeleteAllResultEx()
		client.send_command(cmd)
		return True
	except pynvdrive.NVDriveCommandError as e:
		print('error DeleteAllResultEx ', e)
		return False

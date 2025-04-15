import pynvdrive
from pynvdrive.formats.result_format_and_description import ResultFormatAndDescription
from ..commands.signalresult import GetResultEx


def get_result_ex(client: pynvdrive.Client = None, result_format_and_description: ResultFormatAndDescription = None):
	"""
	create_result_ex
	:return: Result or None + err message (binary NVDrive error)
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = GetResultEx(module=result_format_and_description.module_id,
		                  process=result_format_and_description.process_id,
		                  channel=result_format_and_description.channel_number,
		                  reference_channel_number=result_format_and_description.reference_channel_number,
		                  waterfall_flag=0)
		client.send_command(cmd)
		return cmd.result, None
	except pynvdrive.NVDriveCommandError as e:
		# print('error GetResultEx NVDriveCommandError ', e.error)
		return None, e.error
	except pynvdrive.NVDriveConnectionError as e:
		# print('error GetResultEx NVDriveConnectionError ', e.error)
		return None, e.error
	except Exception as e:
		# print('error GetResultEx ', e.error)
		return None, e.error

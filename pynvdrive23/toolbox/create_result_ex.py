import pynvdrive
from pynvdrive.formats.result_format_and_description import ResultFormatAndDescription
from ..commands.signalresult import CreateResultEx


def create_result_ex(client: pynvdrive.Client = None, result_format_and_description: ResultFormatAndDescription = None):
	"""
	create_result_ex
	:return: bool success
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = CreateResultEx(module=result_format_and_description.module_id, process=result_format_and_description.process_id, channel=result_format_and_description.channel_number,
		                     reference_channel_number=result_format_and_description.reference_channel_number, waterfall_flag=0)
		client.send_command(cmd)
		return True
	except pynvdrive.NVDriveCommandError as e:
		if e.error == b'2112010000':  # Result already exists
			return True
		else:
			print('error CreateResultEx module {} process {} channel {} refchannel {} due to command {}'.format(result_format_and_description.module_id, result_format_and_description.process_id, result_format_and_description.channel_number, result_format_and_description.reference_channel_number, e))
			return False
	except pynvdrive.NVDriveConnectionError as e:
		print('error CreateResultEx due to nvdrive connection issue {}'.format(e))
		return False
	except Exception:
		return False


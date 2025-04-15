import pynvdrive
from ..commands.settingsstates.getgeneralanalyzerstate import GetGeneralAnalyzerState, GeneralAnalyzerState


def get_general_analyzer_state(client: pynvdrive.Client = None) -> GeneralAnalyzerState:
	"""
	Returns the general analyzer state
	:return: AnalyzerState
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = GetGeneralAnalyzerState()
		client.send_command(cmd)
		return cmd.state
	except pynvdrive.NVDriveCommandError as e:
		print('error GetGeneralAnalyzerState ', e.error)
	except pynvdrive.NVDriveConnectionError as e:
		print('error GetGeneralAnalyzerState ', e)
		return None
	except Exception:
		return None
	return None

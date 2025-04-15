import pynvdrive
from ..commands.settingsstates.getanalyzerstate import GetAnalyzerState, TriggerState


def get_analyzer_state(module_id, state_name='Trigger state', client: pynvdrive.Client = None):
	"""
	Returns the analyzer state
	:return: float, str or TriggerState depending on the state_name
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	try:
		cmd = GetAnalyzerState(module=module_id, state_name=state_name)
		client.send_command(cmd)
		return cmd.state
	except pynvdrive.NVDriveCommandError as e:
		print('error GetAnalyzerState ', e.error)
	except pynvdrive.NVDriveConnectionError as e:
		print('error GetAnalyzerState ', e)
		return None
	except Exception:
		return None

	return None

import pynvdrive
from ..commands.marker.getfreemarkerparameters import GetFreeMarkerParameters


def get_free_marker_parameters(window_name, display_zone_type, marker_number, client: pynvdrive.Client = None):
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
		cmd = GetFreeMarkerParameters(window=window_name, display_zone=display_zone_type, marker_number=marker_number)
		client.send_command(cmd)
		return cmd.value
	except pynvdrive.NVDriveCommandError as e:
		print('error GetFreeMarkerParameters ', e.error)
	except pynvdrive.NVDriveConnectionError as e:
		print('error GetFreeMarkerParameters ', e)
		return None
	except Exception:
		return None
	return None

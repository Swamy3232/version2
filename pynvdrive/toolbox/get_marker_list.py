import pynvdrive
from pynvdrive import NVDriveCommandError, NVDriveConnectionError
from ..client import Client
from ..commands.marker.getmarkerlist import GetMarkerList
from ..commands.marker.getwindowdisplayzone import GetWindowDisplayZone


def get_marker_list(window_name: str, display_zone_type: str = '0', client: pynvdrive.Client = None) -> list:
	"""
	Return layout list
	:return: list<str>
	"""
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	layouts_list = []


	try:
		cmd = GetWindowDisplayZone(window_name=window_name)
		client.send_command(cmd)
		display_zone_type = cmd.value
	except NVDriveCommandError as e:
		print('error GetWindowDisplayZone ', e)
	except NVDriveConnectionError:
		print('error NVDrive is not connected (get_marker_list)')
	except Exception:
		pass

	if display_zone_type is None:
		print('error GetWindowDisplayZone (get_marker_list) : display_zone_type is {}'.format(display_zone_type))
		display_zone_type = 0

	marker_list = []
	try:
		cmd = GetMarkerList(window_name=window_name, display_zone_type=display_zone_type)
		client.send_command(cmd)
		marker_list = cmd.list_marker_description
	except NVDriveCommandError as e:
		print('error GetMarkerList ', e)
	except NVDriveConnectionError:
		print('error NVDrive is not connected (get_marker_list)')
	except Exception:
		pass

	return marker_list

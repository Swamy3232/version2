from ...client import Client, NVDriveCommandError
from .nvd_cmd import GetMagnitudeList, GetUnitList, GetUnitInfo
import pynvdrive


def get_all_units(client: Client = None) -> dict:
	if client is None:
		client = pynvdrive.Client()
		client.connect()
	else:
		client.connect()

	dict_magnitude = {}
	try:
		cmd = GetMagnitudeList()
		client.send_command(cmd)
		list_magnitude = cmd.value
	except NVDriveCommandError as e:
		print('error GetMagnitudeList ', e.error)
		return False
	else:
		try:
			for magnitude_name in list_magnitude:
				dict_magnitude[magnitude_name] = {}

				cmd = GetUnitList(magnitude_name=magnitude_name)
				client.send_command(cmd)

				list_unit = cmd.value

				for unit_name in list_unit:
					cmd = GetUnitInfo(magnitude_name=magnitude_name, unit_name=unit_name)
					client.send_command(cmd)
					unit_info = cmd

					dict_magnitude[magnitude_name][unit_name] = {}
					dict_magnitude[magnitude_name][unit_name]['unit_label'] = unit_info.userunit_label
					dict_magnitude[magnitude_name][unit_name]['unit_name'] = unit_info.userunit_name
					dict_magnitude[magnitude_name][unit_name]['si_unit_label'] = unit_info.si_unit # Name
					dict_magnitude[magnitude_name][unit_name]['coeff_A'] = unit_info.coeffA
					dict_magnitude[magnitude_name][unit_name]['coeff_B'] = unit_info.coeffB
		except NVDriveCommandError as e:
			print('error GetUnitList ', e.error)
			return False

	return dict_magnitude
